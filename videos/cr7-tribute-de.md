# CR7 — Die Legende

[Télécharger la vidéo verticale MP4](https://raw.githubusercontent.com/mbairamadji007/starter/main/videos/cr7-tribute-de.mp4)

[Télécharger le projet HyperFrames complet](https://raw.githubusercontent.com/mbairamadji007/starter/main/videos/cr7-tribute-de-source.zip)

Hommage à Cristiano Ronaldo : **15 secondes**, **9:16**, **1080 × 1920**, **60 images/s**. Quatre cartes de collection, palette noir-or-émeraude, coins de viseur, code-barres et typographie suisse. Les textes à l’écran et la voix off sont allemands.

Le texte parlé est conservé intégralement. La narration masculine Thorsten accompagne la légende, les cinq Ballons d’Or et cinq titres de Champions League, le titre européen avec le Portugal et les 900+ buts, puis la discipline et la constance. Musique et effets originaux synchronisés, avec baisse du fond sous la voix.

Le visuel de Ronaldo est généré, détouré et cadré en deux plans ; les trophées sont des créations vectorielles avec volumes et reflets métalliques. Les attributions et les repères sonores sont inclus dans l’archive.

Pour modifier et rendre le film, extraire le ZIP puis ouvrir `cr7-tribute`. Avec Node.js 22 ou supérieur, FFmpeg et Chromium :

```bash
npm ci
npm run preview
npm run render
```

Le rendu est créé dans `renders/cr7-tribute-de.mp4`. Les quatre cartes sont dans `compositions/`, l’animation dans `scenes/card-scenes.js` et les prises vocales/stems dans `assets/audio/`. Consulter `README.md` et `SOUND_DESIGN.md` pour le détail.
