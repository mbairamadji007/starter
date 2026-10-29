# bande son documentaire

Le mix accompagne la narration fournie : fond ambient lent, résonances de bois,
textures de papier, grain et pierre. Les trois impacts graves soulignent des
bascules narratives. Les autres coupes restent majoritairement silencieuses.
La musique ne suit aucune grille publicitaire à 120 BPM.

Le master dure exactement **235,608229 s** : **11 309 195 échantillons à 48 kHz**.
Il contient toute la voix préparée, sans nouvelle coupe, accélération ou
resynthèse. Le niveau de la narration reçoit uniquement le placement au centre
stéréo à puissance constante et un gain final constant de **−0,91 dB**.

## fichiers et mesures

| fichier | rôle |
| --- | --- |
| `assets/audio/documentary-master.wav` | master stéréo 48 kHz / PCM 24 bits |
| `assets/audio/documentary-master.m4a` | copie légère AAC stéréo 48 kHz / 192 kb/s |
| `assets/audio/narration-source.wav` | copie intacte de la voix préparée, mono PCM24 |
| `assets/audio/music-original.flac` | musique originale avant carve et atténuation |
| `assets/audio/sfx-original.flac` | effets originaux avant atténuation |
| `assets/audio/narration-mix.flac` | voix au niveau et au placement du master |
| `assets/audio/background-mix.flac` | musique et effets après traitements et gain final |

Mesures EBU R128 du WAV : **−16,00 LUFS intégrés**, **−4,31 dBTP**,
plage de dynamique **2,9 LU**, aucun écrêtage.
La copie AAC mesure **−16,05 LUFS**, **−3,91 dBTP**.
Les mesures complètes et les empreintes figurent dans `audio-metrics.json`.

Les stems FLAC sont sans perte, à la même fréquence et de la même durée que le
WAV. La somme de `narration-mix.flac` et `background-mix.flac`, à volume 1,
reproduit le master à l'arrondi PCM24 près.

## voix prioritaire

Le fond musical s'atténue jusqu'à **8 dB** pendant la voix ; les effets jusqu'à
**4 dB**. Le contrôle mesure la vraie narration avec 90 ms d'anticipation,
35 ms d'attaque, 200 ms de maintien et 550 ms de retour. Les respirations et les
petites pauses ne provoquent donc pas de remontées brutales de la musique.

Un carve dynamique sur la musique réduit 250 Hz de 2 dB, 850 Hz de 4,5 dB,
1 800 Hz de 5 dB et 3 200 Hz de 3 dB pendant la narration. La voix elle-même
ne reçoit ni égalisation, compression, débruitage, ni fondu qui couperait sa fin.
La musique seule se referme progressivement sur les 3,4 dernières secondes.

## synchronisation

Toutes les positions suivent la narration **préparée**, et non la simple
concaténation des MP3 d'origine. Le fichier `sound-cues.json` contient les
24 repères, leurs types, leurs gains et leur rôle.

| temps | geste sonore principal |
| --- | --- |
| 0,000 s | ouverture : souffle grave et texture |
| 18,832 s | papier, bascule vers les groupes sans roi |
| 45,091 s | pierre et accent grave : agriculture et réserves |
| 66,494 s | grain discret : accumulation des réserves |
| 71,596 s | bois : fixation de la richesse et des lieux |
| 90,980 s | papier / trait : grille des premiers comptes |
| 93,542 s | grain : stockage, coordination et dette |
| 120,840 s | pierre et accent grave : administration et violence |
| 149,784 s | papier : légitimation et ordre religieux |
| 175,906 s | petit mécanisme : continuité de l'institution |
| 184,581 s | mécanisme sec unique : relais personne / institution |
| 202,769 s | pierre et dernier accent grave : héritage du système |
| 231,818 s | bois léger : conclusion et invitation finale |

Des souffles brefs commencent 380 ms avant les huit grandes transitions de
18,832 à 202,769 s. Les trois révélations internes n'ajoutent aucune grosse
percussion. Les repères peuvent être déplacés dans le JSON puis recalculés.

## intégration HyperFrames

Placer le master une seule fois dans la composition principale :

```html
<audio
  id="documentary-sound"
  src="assets/audio/documentary-master.wav"
  data-start="0"
  data-duration="235.60822916666666"
  data-track-index="10"
  data-volume="1"
  data-label="voix · musique · effets"
></audio>
```

La copie M4A peut remplacer le WAV pour une prévisualisation légère.
HyperFrames pilote la lecture et le rendu ; aucune synthèse ou minuterie
JavaScript n'est nécessaire dans la composition.

## recalculer ou modifier

Avec Python 3, NumPy, FFmpeg et FFprobe installés, depuis la racine de production :

```bash
python3 scripts/mix_soundtrack.py
```

Le script utilise la copie locale intacte `narration-source.wav` et les repères
de `sound-cues.json`. Les types disponibles sont `paper`, `grain`, `stone`,
`wood`, `mechanism`, `deep-impact` et `air`. Modifier `time` ou `gain` dans
le JSON permet d'ajuster une transition sans toucher à la narration.

La graine de synthèse est fixe. Les fichiers gelés sont les seuls lus pendant
le montage et l'export, ce qui conserve une lecture déterministe.

## provenance

La voix provient des dix fichiers fournis par l'utilisateur. La préparation
antérieure a retiré 9,473 s de silence et conservé quatre pauses pour protéger
les respirations ; son journal est inclus dans `provenance/audio-preparation-report.json`.
Les chemins absolus de ce journal désignent l’atelier de préparation original ;
les empreintes et la correspondance des échantillons restent les repères portables.
La copie de travail conserve l'empreinte du master préparé :

```text
8ccd68e3f10d20337512caf26e9f03a1f31f7a39cbda6420648ed11a414c7680
```

La musique et les effets ont été composés par synthèse procédurale originale
pour ce documentaire. Les sons de papier, grain et pierre sont des évocations
sonores synthétiques ; aucun enregistrement commercial ou échantillon de
bibliothèque externe n'est utilisé.
