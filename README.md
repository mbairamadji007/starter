# qui a inventé les rois ?

Documentaire en motion graphics, **16:9 — 1920 × 1080 — 30 images/s**. Les dix
voix off françaises fournies sont réunies en une narration de **235,608229 s**,
soit environ **3 min 56 s**. Le découpage alterne 44 plans : objets et sites
historiques photographiés, véritables extraits vidéo contemporains, collages,
carte schématique et diagrammes animés. Les textes visibles sont en minuscules.

## lancer le projet

Prérequis : **Node.js 22 ou supérieur**, npm, **FFmpeg** et FFprobe dans le
`PATH`, ainsi qu’un navigateur Chromium compatible. HyperFrames est fixé à
**0.8.145** ; le verrou npm accompagne le projet.

Extraire l’archive et ouvrir le dossier `royaute-documentaire`, puis lancer :

```bash
npm ci
npm run preview
```

Ouvrir l’URL affichée par HyperFrames. Le projet et ses ressources sont locaux.

```bash
npm run check
npm run render
```

Le fichier de sortie est **`renders/royaute-documentaire.mp4`**, en H.264 avec
audio AAC. La durée exacte de la voix est exprimée sur une horloge de 48 kHz ;
la durée du MP4 est arrondie à la cadence des images. Après export, vérifier les
valeurs réelles avec :

```bash
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels -show_entries format=duration -of json renders/royaute-documentaire.mp4
```

Pour sélectionner un Chromium déjà installé, définir `HYPERFRAMES_BROWSER_PATH`
avec son chemin absolu. Exemple sous Linux, pour un rendu logiciel :

```bash
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium npm run render -- --no-browser-gpu
```

`npm run preview:status` indique l’état de l’aperçu en arrière-plan ;
`npx hyperframes preview --stop` l’arrête. `npm run dev` conserve l’aperçu au premier plan.

## contenu et structure

| élément | rôle |
| --- | --- |
| `index.html` | Composition HyperFrames, calques temporels et audio |
| `compositions/` | 44 sous-compositions temporelles correspondant aux plans |
| `shot-plan.json` | 44 plans, textes, besoins visuels et repères de narration |
| `visual-edit.json` | Sélection effective des images, vidéos, cadrages et figures de chaque plan |
| `french-copy.md` | Titres et paraphrases courtes en français |
| `scripts/build_composition.py` | Reconstruction de la composition à partir des données de réalisation |
| `components/figures.js` | Cartes et schémas SVG originaux |
| `styles/` et `scenes/` | Mise en page, typographie et animation |
| `assets/media/` | Photographies et extraits vidéo gelés localement |
| `assets/fonts/` | Cormorant Garamond, Manrope et leurs licences OFL |
| `assets/audio/` | Master, copie de narration et stems séparés |
| `sound-cues.json` | 24 repères d’effets sonores |
| `audio-metrics.json` | Mesures et empreintes des pistes |
| `provenance/audio-preparation-report.json` | Journal des silences raccourcis et correspondance source/narration |
| `credits-sources.json` et `CREDITS.md` | Provenance, auteurs, licences et contexte des visuels |

Les polices associent la sérif **Cormorant Garamond** aux formes géométriques de
**Manrope**. La direction visuelle utilise papier clair, encre sombre, ocre et
rouge brique. Le mouvement et les calques sont pilotés par des timelines GSAP
déterministes que HyperFrames peut échantillonner à un temps précis.

Les titres sont des formulations éditoriales courtes. La transcription
automatique de travail n’est pas utilisée comme sous-titrage intégral certifié.
Les objets et leurs époques sont identifiés dans les crédits ; une photographie
actuelle, une gravure ancienne ou un extrait de paysage ne deviennent pas une
reconstitution filmée de la Mésopotamie.

## narration et son

La préparation des dix MP3 a retiré **9,473 s** de silence : 19 pauses longues
ont été raccourcies et quatre pauses ont été conservées pour protéger les
respirations. Le master préparatoire d’origine dure 235,608229 s. Le mix sonore
conserve cette voix, son ordre et son débit, avec un placement stéréo central et
un gain constant.

**`assets/audio/documentary-master.wav`** est le mix final gelé : stéréo 48 kHz,
PCM 24 bits, **−16,00 LUFS**, **−4,31 dBTP**. Musique ambient lente et textures
de papier, grain, bois et pierre sont des créations procédurales originales.
Le fond s’atténue et laisse de l’espace fréquentiel à la parole. Le master est
placé une seule fois dans la composition.

Pour modifier ou recalculer le mix, lire **`SOUND_DESIGN.md`**. Avec Python 3,
NumPy, FFmpeg et FFprobe :

```bash
python3 scripts/mix_soundtrack.py
```

Les pistes `narration-mix.flac` et `background-mix.flac`, superposées à volume 1,
reconstituent le master à l’arrondi PCM24 près. Les pistes originales de musique
et d’effets permettent de reprendre le mix. La copie `documentary-master.m4a`
sert de version légère du même programme sonore.

## modifier et contrôler

Conserver la chronologie de la narration lors des changements de plans.
Après une modification du découpage ou des données de réalisation :

```bash
python3 scripts/build_composition.py
npm run check
```

Examiner les captures des plans concernés avant de relancer l’export. Les
mesures audio décrivent les pistes livrées ; les caractéristiques du MP4 se
contrôlent après chaque rendu. Les documents présents ne remplacent pas le
résultat de `npm run check` sur une version modifiée.

La provenance et les conditions des ressources sont détaillées dans
**`NOTICE.md`** et **`CREDITS.md`**. Conserver ces attributions avec le projet.

## produire une archive source

Le script suivant liste d’abord les fichiers et leur volume, sans créer de ZIP :

```bash
python3 scripts/package_source.py
```

Après avoir figé les sources :

```bash
python3 scripts/package_source.py --write --output royaute-documentaire-source.zip
```

L’archive inclut les médias locaux, les polices, les pistes séparées et les
scripts. Les dépendances installées, caches, modèles de transcription, rendus
et captures de travail sont exclus. Un manifeste d’empreintes est intégré au ZIP.
