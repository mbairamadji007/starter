# provenance et licences

Ce projet réunit la narration fournie par l’utilisateur, une réalisation
graphique originale et des médias tiers dont la provenance est consignée.
Les licences des médias, des polices et des bibliothèques s’appliquent à leurs
éléments respectifs ; elles ne constituent pas une licence unique du film.

## voix, musique et effets

- **Narration :** dix fichiers MP3 fournis par l’utilisateur, assemblés dans
  l’ordre de leurs noms. La copie préparée a uniquement raccourci des silences
  longs ; elle reste la source du mix et n’a pas été remplacée par une voix
  synthétique. Les droits sur cet enregistrement et sur le texte restent ceux
  de leurs ayants droit.
- **Musique et effets :** synthèse procédurale originale créée pour ce
  documentaire. Les évocations de papier, de grain, de bois et de pierre
  n’utilisent pas d’enregistrements commerciaux ou d’échantillons de bibliothèque.
- Les procédures, les stems et leurs mesures sont dans `SOUND_DESIGN.md`,
  `sound-cues.json` et `audio-metrics.json`.

## photographies et reproductions

Les images gelées ont été récupérées dans le dépôt pédagogique officiel
[OpenStax / Rice University — World History](https://github.com/openstax/osbooks-world-history),
à partir du commit `c0dd82697bc2c7cd355c942e778f215762768c43`. Les crédits des
figures individuelles précisent les auteurs et conditions des photographies
préexistantes. La licence globale du texte du manuel ne remplace pas ces
licences individuelles.

Le catalogue contient des reproductions signalées comme **domaine public**,
**CC0**, ou **CC BY 2.0 / 2.5 / 3.0 / 4.0**. Le montage tablette/jetons combine
une photographie CC0 et une photographie CC BY 2.5 ; le crédit de Marie-Lan
Nguyen est conservé. Les fiches complètes, liens de licence et références
figurent dans `CREDITS.md` et `credits-sources.json`.

Les fichiers téléchargés gardent leur empreinte. Leur utilisation dans le film
peut comprendre sélection de détails, recadrage dans un cadre, déplacement,
agrandissement modéré, combinaison avec du texte ou des formes graphiques et
fondus. Ces interventions de montage sont des adaptations de présentation et
ne modifient pas l’attribution de l’œuvre photographiée ni celle de la photo.

## véritables extraits vidéo

Trois séquences contemporaines illustrent céréales au vent, rivière en forêt
et nuages d’orage. Elles sont attribuées respectivement à **Joshua Woroniecki**,
**Ruvim M** et **James Cheney**, et relèvent de la
[licence Pexels](https://www.pexels.com/license/), une licence d’usage gratuite
personnalisée, **distincte de CC0**.

Les renditions téléchargées sont conservées dans le dépôt
[Golden Hilal Media](https://github.com/Winds7799/golden-hilal-media)
(commit `4b581c7e44d2cf1183706907538d9816af2318b2`), dont le fichier
[LICENSES.md](https://github.com/Winds7799/golden-hilal-media/blob/4b581c7e44d2cf1183706907538d9816af2318b2/LICENSES.md)
relie chaque fichier à sa vidéo Pexels d’origine. Les sources originales et
les adaptations déjà effectuées par ce dépôt sont listées dans `CREDITS.md` et
`assets/media/video-sources.json`. Les séquences sont intégrées au montage,
pas proposées comme une bibliothèque de stock autonome.

## typographie

- **Cormorant Garamond** — Copyright 2015 The Cormorant Project Authors.
  [Projet Cormorant](https://github.com/CatharsisFonts/Cormorant), distribution
  via [Google Fonts](https://github.com/google/fonts/tree/main/ofl/cormorantgaramond).
  Licence **SIL Open Font License 1.1**, incluse dans
  `assets/fonts/Cormorant-OFL.txt`.
- **Manrope** — Copyright 2018 The Manrope Project Authors.
  [Projet Manrope](https://github.com/googlefonts/manrope), distribution via
  [Google Fonts](https://github.com/google/fonts/tree/main/ofl/manrope).
  Licence **SIL Open Font License 1.1**, incluse dans
  `assets/fonts/Manrope-OFL.txt`.

Les fichiers TTF sont livrés localement et chargés par la composition.

## code et graphisme

Les cartes, pictogrammes, diagrammes et règles de mouvement propres au film
sont des créations graphiques du projet. La carte régionale est schématique ;
elle ne représente pas des frontières politiques anciennes établies.

**GSAP 3.14.2** est distribué dans `assets/vendor/gsap.min.js` avec sa notice
d’origine. Voir les [conditions standard de GSAP](https://gsap.com/standard-license/).
**HyperFrames 0.8.145** est installé par npm conformément à la dépendance et au
verrou fournis ; son code et ses notices sont ceux du paquet installé.

## identification documentaire

Les photographies d’objets, les vues actuelles de sites et les images
comparatives gardent leur contexte propre. L’étendard d’Ur utilisé montre le
panneau de la guerre ; le détail de la tablette de Shamash montre la divinité.
La coiffe d’Ur ne permet pas d’attribuer une identité royale certaine à sa
porteuse. La couronne de Silla, les vestiges chinois, les lamas andins et le
protocole américain sont identifiés comme tels dans le catalogue. Ils ne sont
pas des documents d’Uruk vers 3200 avant notre ère.

Les clips de paysage sont des illustrations contemporaines ; la rivière
forestière n’est pas identifiée à l’Euphrate. Les dessins et animations ne sont
pas présentés comme des archives filmées.
