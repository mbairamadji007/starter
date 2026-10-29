#!/usr/bin/env python3
"""Build and verify the portable documentary source ZIP after sources are frozen.

Without --write this command only reports the proposed package. No dependency,
cache, render, transcription model or symbolic link is followed into the ZIP.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PREFIX = "royaute-documentaire"
SKIP_DIRS = {
    "node_modules", ".git", ".hyperframes", "renders", "snapshots", "output",
    ".cache", "__pycache__", ".venv", "venv", "asr", "models", "work",
    "scratch", "coverage", ".pytest_cache", "analysis", "previews", "preview",
}
SKIP_NAMES = {".DS_Store", "Thumbs.db", "catalog-contact-sheet.jpg", "source-manifest.json"}
SKIP_SUFFIXES = {".pyc", ".pyo", ".tmp", ".log", ".onnx", ".bz2", ".zip"}
STORED_SUFFIXES = {".mp4", ".m4a", ".jpg", ".jpeg", ".png", ".webp", ".flac", ".woff2"}
REQUIRED = {
    "index.html", "hyperframes.json", "meta.json", "package.json", "package-lock.json",
    "shot-plan.json", "README.md", "NOTICE.md", "CREDITS.md", "BRIEF.md", "DESIGN.md",
    "SOUND_DESIGN.md", "credits-sources.json", "audio-metrics.json", "sound-cues.json",
    "components/figures.js", "scripts/build_composition.py", "scripts/mix_soundtrack.py",
    "assets/fonts/CormorantGaramond.ttf", "assets/fonts/Cormorant-OFL.txt",
    "assets/fonts/Manrope.ttf", "assets/fonts/Manrope-OFL.txt",
    "assets/audio/documentary-master.wav", "assets/audio/narration-source.wav",
    "assets/audio/narration-mix.flac", "assets/audio/background-mix.flac",
}


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def selected_files() -> tuple[list[Path], list[str]]:
    files: list[Path] = []
    excluded: list[str] = []
    for folder, dirs, names in os.walk(ROOT, followlinks=False):
        current = Path(folder)
        kept_dirs: list[str] = []
        for name in sorted(dirs):
            path = current / name
            if name in SKIP_DIRS or path.is_symlink() or name.startswith(".hf-"):
                excluded.append(str(path.relative_to(ROOT)))
            else:
                kept_dirs.append(name)
        dirs[:] = kept_dirs
        for name in sorted(names):
            path = current / name
            relative = path.relative_to(ROOT).as_posix()
            if (path.is_symlink() or name in SKIP_NAMES or name.endswith("-preview.jpg")
                    or path.suffix.lower() in SKIP_SUFFIXES
                    or name == ".env" or name.startswith(".env.")
                    or name.lower() in {"credentials", "credentials.json", "secrets.json"}):
                excluded.append(relative)
                continue
            if path.is_file():
                files.append(path)
    return sorted(files, key=lambda p: p.relative_to(ROOT).as_posix()), sorted(excluded)


def make_manifest(files: list[Path]) -> dict:
    return {
        "project": PREFIX,
        "format": "HyperFrames source project with local media",
        "hashAlgorithm": "SHA-256",
        "files": [
            {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size,
             "sha256": digest(path)}
            for path in files
        ],
    }


def build(output: Path, files: list[Path], manifest: dict) -> dict:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    expected = {item["path"]: item for item in manifest["files"]}
    try:
        with tempfile.NamedTemporaryFile(prefix="documentary-source-", suffix=".zip", dir=output.parent,
                                         delete=False) as handle:
            temporary = Path(handle.name)
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9, allowZip64=True) as archive:
            for path in files:
                relative = path.relative_to(ROOT).as_posix()
                data = path.read_bytes()
                if hashlib.sha256(data).hexdigest() != expected[relative]["sha256"]:
                    raise RuntimeError(f"Source changed during packaging: {relative}")
                entry = zipfile.ZipInfo(f"{PREFIX}/{relative}", date_time=(2026, 10, 28, 0, 0, 0))
                entry.external_attr = 0o100644 << 16
                entry.compress_type = (zipfile.ZIP_STORED if path.suffix.lower() in STORED_SUFFIXES
                                       else zipfile.ZIP_DEFLATED)
                archive.writestr(entry, data, compresslevel=9)
            entry = zipfile.ZipInfo(f"{PREFIX}/source-manifest.json", date_time=(2026, 10, 28, 0, 0, 0))
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                             compresslevel=9)
        with zipfile.ZipFile(temporary) as archive:
            corrupt = archive.testzip()
            if corrupt:
                raise RuntimeError(f"CRC mismatch: {corrupt}")
            for item in manifest["files"]:
                data = archive.read(f"{PREFIX}/{item['path']}")
                if hashlib.sha256(data).hexdigest() != item["sha256"]:
                    raise RuntimeError(f"Content mismatch: {item['path']}")
        temporary.replace(output)
        temporary = None
        return {"archive": str(output), "archiveBytes": output.stat().st_size,
                "archiveSha256": digest(output), "verifiedCRC": True,
                "verifiedEveryFileSha256": True}
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Create and verify the source ZIP")
    parser.add_argument("--output", type=Path, default=ROOT.parent / "royaute-documentaire-source.zip")
    parser.add_argument("--manifest", type=Path, help="Also save the source manifest as JSON")
    args = parser.parse_args()
    files, excluded = selected_files()
    present = {path.relative_to(ROOT).as_posix() for path in files}
    missing = sorted(REQUIRED - present)
    report = {"mode": "write" if args.write else "inspect", "projectRoot": str(ROOT),
              "fileCount": len(files), "uncompressedBytes": sum(p.stat().st_size for p in files),
              "excluded": excluded, "missingRequired": missing}
    if args.write and missing:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        raise RuntimeError("Required files missing; freeze the completed project before packaging")
    manifest = make_manifest(files)
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.write:
        report.update(build(args.output.resolve(), files, manifest))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
