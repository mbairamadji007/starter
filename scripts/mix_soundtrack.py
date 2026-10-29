#!/usr/bin/env python3
"""Original documentary ambience/foley and transparent mix of supplied narration.

Dependencies: Python 3, NumPy, ffmpeg and ffprobe. No TTS, outside samples,
network calls or speech cuts. Input narration remains byte-for-byte preserved.
All music/SFX generation is deterministic; HyperFrames plays a frozen master.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

SR = 48_000
EXPECTED_FRAMES = 11_309_195
SEED = 280_042_010
CHAPTERS = [0.0, 18.832354167, 45.091291667, 71.596270833, 93.542291667,
            120.839791667, 149.784333333, 175.906416667, 202.769354167, 231.817520833]


def command(args: list[str], capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=True, capture_output=capture)


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for part in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(part)
    return digest.hexdigest()


def read_voice(path: Path) -> np.ndarray:
    with wave.open(str(path)) as wav:
        if (wav.getframerate(), wav.getnchannels(), wav.getsampwidth()) != (SR, 1, 3):
            raise ValueError('Expected the prepared 48 kHz mono PCM24 narration')
        if wav.getnframes() != EXPECTED_FRAMES:
            raise ValueError('Narration length changed: review editorial cue timing before rebuilding')
        data = np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.uint8).reshape(-1, 3).astype(np.int32)
    value = data[:, 0] | (data[:, 1] << 8) | (data[:, 2] << 16)
    value = (value ^ (1 << 23)) - (1 << 23)
    return value.astype(np.float32) / 8388608


def read_stereo(path: Path) -> np.ndarray:
    result = command(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(path),
                      '-ar', str(SR), '-ac', '2', '-f', 'f32le', '-'])
    return np.frombuffer(result.stdout, dtype='<f4').reshape(-1, 2).copy()


def write_wav(path: Path, signal: np.ndarray) -> None:
    if np.max(np.abs(signal), initial=0) >= 1:
        raise ValueError(f'Refuse clipping: {path.name}')
    channels = 1 if signal.ndim == 1 else signal.shape[1]
    with wave.open(str(path), 'wb') as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(3)
        wav.setframerate(SR)
        # Bounded blocks keep the 4-minute PCM24 master inexpensive in memory.
        for start in range(0, len(signal), SR * 4):
            pcm = np.round(signal[start:start + SR * 4].reshape(-1).astype(np.float64) * 8388608).astype(np.int32)
            packed = np.stack((pcm & 255, (pcm >> 8) & 255, (pcm >> 16) & 255), axis=1).astype(np.uint8)
            wav.writeframes(packed.tobytes())


def write_flac(path: Path, signal: np.ndarray, temp: Path) -> None:
    intermediate = temp / f'{path.stem}.wav'
    write_wav(intermediate, signal)
    command(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(intermediate),
             '-c:a', 'flac', '-compression_level', '8', str(path)])
    intermediate.unlink()


def measure(path: Path) -> dict:
    result = command(['ffmpeg', '-hide_banner', '-nostats', '-i', str(path), '-af',
                      'loudnorm=I=-16:TP=-2:LRA=7:print_format=json', '-f', 'null', '-'])
    output = result.stderr.decode()
    info = json.loads(output[output.rfind('{'):output.rfind('}') + 1])
    return {'integratedLUFS': float(info['input_i']), 'truePeakDbTP': float(info['input_tp']),
            'loudnessRangeLU': float(info['input_lra'])}


def timebase(seconds: float) -> np.ndarray:
    return np.arange(round(seconds * SR), dtype=np.float32) / SR


def edge(signal: np.ndarray, attack: float = 0.012, release: float = 0.055) -> np.ndarray:
    signal = signal.copy()
    left = min(len(signal), round(attack * SR))
    right = min(len(signal), round(release * SR))
    signal[:left] *= np.sin(np.linspace(0, np.pi / 2, left)) ** 2
    signal[-right:] *= np.cos(np.linspace(0, np.pi / 2, right)) ** 2
    return signal


def band_noise(rng: np.random.Generator, seconds: float, low: float, high: float) -> np.ndarray:
    n = round(seconds * SR)
    source = rng.standard_normal(n)
    frequencies = np.fft.rfftfreq(n, 1 / SR)
    spectrum = np.fft.rfft(source)
    spectrum *= (1 - np.exp(-(frequencies / low) ** 4)) * np.exp(-(frequencies / high) ** 4)
    signal = np.fft.irfft(spectrum, n=n)
    signal /= max(float(np.sqrt(np.mean(signal**2))), 1e-12)
    return (np.tanh(signal / 1.8) * 1.5).astype(np.float32)


def stereo(signal: np.ndarray, pan: float = 0) -> np.ndarray:
    angle = (pan + 1) * np.pi / 4
    return np.column_stack((signal * np.cos(angle), signal * np.sin(angle))).astype(np.float32)


def place(track: np.ndarray, signal: np.ndarray, at: float, gain: float = 1, pan: float = 0) -> None:
    if signal.ndim == 1:
        signal = stereo(signal, pan)
    position = round(at * SR)
    skip = max(0, -position)
    position = max(0, position)
    length = min(len(signal) - skip, len(track) - position)
    if length > 0:
        track[position:position + length] += signal[skip:skip + length] * gain


def paper(rng: np.random.Generator) -> np.ndarray:
    t = timebase(0.68)
    signal = band_noise(rng, 0.68, 220, 3800)
    envelope = np.sin(np.pi * t / 0.68) ** 1.5
    flutter = 0.72 + 0.28 * np.sin(2 * np.pi * (41 * t + 39 * t**2))
    return edge(signal * envelope * flutter * 0.065)


def grain(rng: np.random.Generator) -> np.ndarray:
    track = np.zeros(round(0.85 * SR), dtype=np.float32)
    for _ in range(26):
        length = float(rng.uniform(0.009, 0.026))
        t = timebase(length)
        y = band_noise(rng, length, 650, 4900) * np.exp(-t / (length * 0.2))
        y = edge(y, 0.001, 0.005) * float(rng.uniform(0.007, 0.022))
        at = round(float(rng.uniform(0.025, 0.73)) * SR)
        track[at:at + len(y)] += y
    return track


def stone(rng: np.random.Generator) -> np.ndarray:
    t = timebase(1.05)
    signal = np.zeros_like(t)
    for frequency, level, decay in [(139.0, 0.045, 0.24), (229.3, 0.027, 0.14), (381.7, 0.012, 0.08)]:
        signal += np.sin(2 * np.pi * frequency * t) * np.exp(-t / decay) * level
    signal += band_noise(rng, 1.05, 90, 1600) * np.exp(-t / 0.075) * 0.025
    return edge(signal, 0.004, 0.10)


def wood() -> np.ndarray:
    t = timebase(0.40)
    signal = (np.sin(2 * np.pi * 183 * t) + 0.4 * np.sin(2 * np.pi * 508 * t)) * np.exp(-t / 0.035)
    return edge(signal * 0.035, 0.0015, 0.040)


def mechanism() -> np.ndarray:
    t = timebase(0.10)
    tick = (np.sin(2 * np.pi * 1350 * t) + 0.45 * np.sin(2 * np.pi * 2490 * t)) * np.exp(-t / 0.010)
    tick = edge(tick * 0.030, 0.0008, 0.016)
    result = np.zeros(round(0.30 * SR), dtype=np.float32)
    result[:len(tick)] += tick
    offset = round(0.083 * SR)
    result[offset:offset + len(tick)] += tick * 0.68
    return result


def deep_impact(rng: np.random.Generator) -> np.ndarray:
    t = timebase(1.65)
    phase = 2 * np.pi * (38 * t + 53 * 0.075 * (1 - np.exp(-t / 0.075)))
    signal = np.sin(phase) * np.exp(-t / 0.34) * 0.105
    signal += band_noise(rng, 1.65, 70, 900) * np.exp(-t / 0.14) * 0.020
    return edge(signal, 0.009, 0.18)


def air(rng: np.random.Generator, direction: int) -> np.ndarray:
    t = timebase(0.82)
    envelope = np.sin(np.pi * t / 0.82) ** 1.7
    signal = edge(band_noise(rng, 0.82, 180, 2400) * envelope * 0.029)
    angle = (1 + direction * (-0.55 + 1.1 * t / 0.82)) * np.pi / 4
    return np.column_stack((signal * np.cos(angle), signal * np.sin(angle))).astype(np.float32)


def default_cues() -> list[dict]:
    kinds = ['air', 'paper', 'stone', 'wood', 'grain', 'stone', 'paper', 'mechanism', 'stone', 'wood']
    result = []
    for i, (at, kind) in enumerate(zip(CHAPTERS, kinds)):
        result.append({'id': f'chapter-{i+1:02d}', 'time': at, 'kind': kind, 'gain': 0.72,
                       'purpose': 'opening' if i == 0 else 'chapter transition'})
        if i in [2, 5, 8]:
            result.append({'id': f'low-accent-{i+1:02d}', 'time': at, 'kind': 'deep-impact',
                           'gain': 0.62, 'purpose': 'three restrained low-frequency narrative accents'})
        if 1 <= i <= 8:
            result.append({'id': f'chapter-air-{i+1:02d}', 'time': max(0, at - 0.38), 'kind': 'air',
                           'gain': 0.68, 'purpose': 'short anticipation into chapter'})
    result += [
        {'id': 'grain-reveal', 'time': 66.494, 'kind': 'grain', 'gain': 0.75, 'purpose': 'grain stock fragments/accumulates'},
        {'id': 'account-grid', 'time': 90.980, 'kind': 'paper', 'gain': 0.70, 'purpose': 'first accounting grid'},
        {'id': 'institution-relay', 'time': 184.581, 'kind': 'mechanism', 'gain': 0.85,
         'purpose': 'person leaves; institution remains, one short mechanical gesture'},
    ]
    return sorted(result, key=lambda x: (x['time'], x['id']))


def synth_music(frames: int, rng: np.random.Generator) -> np.ndarray:
    duration = frames / SR
    score = np.zeros((frames, 2), dtype=np.float32)
    voicings = [[73.4162, 110, 174.6141, 220], [73.4162, 110, 146.8324, 220],
                [58.2705, 116.5409, 174.6141, 233.0819], [73.4162, 110, 146.8324, 195.9977],
                [55, 110, 164.8138, 220], [65.4064, 98, 155.5635, 195.9977],
                [73.4162, 110, 174.6141, 220], [58.2705, 116.5409, 174.6141, 233.0819],
                [73.4162, 110, 146.8324, 220], [73.4162, 110, 146.8324, 220]]
    ends = CHAPTERS[1:] + [duration]
    for chapter, (start, end, notes) in enumerate(zip(CHAPTERS, ends, voicings)):
        a, b = max(0, round((start - 2) * SR)), min(frames, round((end + 2) * SR))
        # Float64 phase precision avoids oscillator jitter late in this 4-minute score.
        t = np.arange(a, b, dtype=np.float64) / SR
        gate = np.minimum(np.clip((t - start + 2) / 4, 0, 1), np.clip((end + 2 - t) / 4, 0, 1))
        if chapter == 0:
            gate *= np.clip(t / 3.2, 0, 1)
        left = np.zeros(len(t), dtype=np.float64)
        right = np.zeros(len(t), dtype=np.float64)
        for index, frequency in enumerate(notes):
            level = [0.018, 0.016, 0.021, 0.016][index]
            motion = 0.83 + 0.17 * np.sin(2 * np.pi * (0.018 + index * 0.004) * t + chapter * 0.6)
            phase = index * 0.63
            left += (np.sin(2 * np.pi * frequency * t + phase) +
                     0.19 * np.sin(2 * np.pi * frequency * 3 * t + phase)) * motion * level
            right += (np.sin(2 * np.pi * frequency * 1.00012 * t + phase + 0.10) +
                      0.19 * np.sin(2 * np.pi * frequency * 3.00015 * t + phase)) * motion * level
        score[a:b, 0] += (left * gate).astype(np.float32)
        score[a:b, 1] += (right * gate).astype(np.float32)
        # Uneven, quiet wooden resonances: deliberately no advertising beat grid.
        pulse = start + 2.6
        count = 0
        while pulse < end - 1.0:
            place(score, wood(), pulse, gain=0.20 if chapter < 4 else 0.28,
                  pan=-0.22 if count % 2 else 0.22)
            pulse += float(rng.uniform(3.8, 6.4))
            count += 1
    # Air is generated in overlapping small blocks to keep synthesis memory bounded.
    for start in np.arange(0, duration, 4.0):
        texture = edge(band_noise(rng, 6.0, 180, 2100), 1.8, 1.8) * 0.0026
        place(score, texture, float(start), pan=0.15 * np.sin(start / 17))
    begin = round(max(0, duration - 3.4) * SR)
    score[begin:] *= (np.cos(np.linspace(0, np.pi / 2, frames - begin)) ** 2)[:, None]
    score[0] = 0
    score[-1] = 0
    return score


def control_envelope(voice: np.ndarray) -> np.ndarray:
    step = 480  # 10 ms control clock, not a render or browser clock.
    count = math.ceil(len(voice) / step)
    padded = np.pad(voice, (0, count * step - len(voice)))
    power = np.mean(padded.reshape(-1, step).astype(np.float64) ** 2, axis=1)
    smooth = np.convolve(power, np.ones(5) / 5, mode='same')
    level = 10 * np.log10(np.maximum(smooth, 1e-15))
    target = np.clip((level + 48) / 13, 0, 1)
    # 90 ms anticipation, then a slow release through breaths and short pauses.
    target[:-9] = target[9:]
    values = np.zeros(count, dtype=np.float32)
    previous = 0.0
    hold = 0
    for i, value in enumerate(target):
        if value >= previous:
            previous = value + (previous - value) * math.exp(-0.01 / 0.035)
            hold = 20
        elif hold > 0:
            hold -= 1
        else:
            previous = value + (previous - value) * math.exp(-0.01 / 0.55)
        values[i] = previous
    return np.repeat(values, step)[:len(voice)]


def main(production: Path, prepared_voice: Path | None) -> None:
    audio = production / 'assets' / 'audio'
    audio.mkdir(parents=True, exist_ok=True)
    voice_path = audio / 'narration-source.wav'
    if not voice_path.exists():
        source = prepared_voice or production.parent / 'prepared' / 'audio' / 'voice-master.wav'
        shutil.copy2(source, voice_path)
    protected_hash = hash_file(voice_path)
    voice = read_voice(voice_path)
    frames = len(voice)
    duration = frames / SR
    cue_path = production / 'sound-cues.json'
    if cue_path.exists():
        cues = json.loads(cue_path.read_text(encoding='utf-8'))['cues']
    else:
        cues = default_cues()
    cue_data = {'durationSeconds': duration, 'sampleRate': SR, 'seed': SEED,
                'timingClock': 'prepared narration, not raw MP3 concatenation', 'cues': cues}
    cue_path.write_text(json.dumps(cue_data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    rng = np.random.default_rng(SEED)
    score = synth_music(frames, rng)
    sfx = np.zeros((frames, 2), dtype=np.float32)
    for index, cue in enumerate(cues):
        kind = cue['kind']
        if kind == 'paper':
            signal = paper(rng)
        elif kind == 'grain':
            signal = grain(rng)
        elif kind == 'stone':
            signal = stone(rng)
        elif kind == 'wood':
            signal = wood()
        elif kind == 'mechanism':
            signal = mechanism()
        elif kind == 'deep-impact':
            signal = deep_impact(rng)
        elif kind == 'air':
            signal = air(rng, -1 if index % 2 else 1)
        else:
            raise ValueError(f'Unknown cue sound: {kind}')
        place(sfx, signal, cue['time'], gain=cue.get('gain', 1),
              pan=0.12 if index % 2 else -0.12)
    sfx[-1] = 0
    envelope = control_envelope(voice)
    master_path = audio / 'documentary-master.wav'
    with tempfile.TemporaryDirectory(prefix='documentary-audio-', dir=str(audio)) as temp_name:
        temp = Path(temp_name)
        write_flac(audio / 'music-original.flac', score, temp)
        write_flac(audio / 'sfx-original.flac', sfx, temp)
        carved_file = temp / 'carved.wav'
        command(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(audio / 'music-original.flac'),
                 '-af', 'equalizer=f=250:t=q:w=0.9:g=-2,equalizer=f=850:t=q:w=0.9:g=-4.5,'
                 'equalizer=f=1800:t=q:w=0.9:g=-5,equalizer=f=3200:t=q:w=1.1:g=-3',
                 '-ar', str(SR), '-ac', '2', '-c:a', 'pcm_s24le', str(carved_file)])
        carved = read_stereo(carved_file)
        background = score * (1 - envelope[:, None]) + carved * envelope[:, None]
        background *= (1 - envelope[:, None] * (1 - 10 ** (-8 / 20)))
        background += sfx * (1 - envelope[:, None] * (1 - 10 ** (-4 / 20)))
        del score, sfx, carved
        # Constant-power centre preserves the loudness of the supplied mono VO.
        centre = np.repeat((voice / np.sqrt(2))[:, None], 2, axis=1)
        mix = centre + background
        premaster = temp / 'premaster.wav'
        write_wav(premaster, mix)
        initial = measure(premaster)
        gain_db = min(-16 - initial['integratedLUFS'], -2.3 - initial['truePeakDbTP'])
        gain = 10 ** (gain_db / 20)
        mix *= gain
        write_wav(master_path, mix)
        write_flac(audio / 'narration-mix.flac', centre * gain, temp)
        write_flac(audio / 'background-mix.flac', background * gain, temp)
        final_metrics = measure(master_path)
        sample_peak = float(np.max(np.abs(mix)))
    if final_metrics['truePeakDbTP'] > -2.0:
        raise ValueError('Master true peak exceeds -2 dBTP')
    command(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(master_path),
             '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-ac', '2',
             '-movflags', '+faststart', str(audio / 'documentary-master.m4a')])
    aac_metrics = measure(audio / 'documentary-master.m4a')
    assert hash_file(voice_path) == protected_hash, 'Narration source changed unexpectedly'
    metrics = {
        'durationSeconds': duration, 'frames': frames, 'sampleRate': SR, 'channels': 2,
        'pcmBits': 24, 'master': str(master_path.relative_to(production)),
        'compressedPreview': 'assets/audio/documentary-master.m4a',
        'masterMetrics': {**final_metrics, 'samplePeakDbFS': round(20 * math.log10(sample_peak), 4),
                          'clippedSampleCount': 0},
        'aacMetrics': aac_metrics, 'constantMasterGainDb': round(gain_db, 4),
        'sourceNarrationSha256': protected_hash,
        'narrationProcessing': 'constant-power stereo centre and one constant mastering gain only',
        'speechCutsInThisMix': 0, 'voiceResynthesized': False,
        'musicDuckDb': -8, 'sfxDuckDb': -4, 'duckLookaheadSeconds': 0.09,
        'duckAttackSeconds': 0.035, 'duckHoldSeconds': 0.20, 'duckReleaseSeconds': 0.55,
        'musicCarve': [{'frequencyHz': 250, 'gainDb': -2}, {'frequencyHz': 850, 'gainDb': -4.5},
                       {'frequencyHz': 1800, 'gainDb': -5}, {'frequencyHz': 3200, 'gainDb': -3}],
        'cueCount': len(cues), 'musicSFXProvenance': 'Original procedural synthesis, no sampled third-party recordings',
        'seed': SEED, 'masterSha256': hash_file(master_path),
        'stems': {'sourceVoice': 'assets/audio/narration-source.wav',
                  'originalMusic': 'assets/audio/music-original.flac', 'originalSFX': 'assets/audio/sfx-original.flac',
                  'postmixVoice': 'assets/audio/narration-mix.flac', 'postmixBackground': 'assets/audio/background-mix.flac'},
        'runtime': 'Frozen assets only; no synthesis, randomness or WebAudio timers in the composition',
    }
    (production / 'audio-metrics.json').write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--production-root', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--prepared-voice', type=Path)
    args = parser.parse_args()
    main(args.production_root, args.prepared_voice)
