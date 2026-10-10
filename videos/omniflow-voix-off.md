# OmniFlow — version avec voix off française

[Télécharger la vidéo MP4](https://raw.githubusercontent.com/mbairamadji007/starter/main/videos/omniflow-voix-off.mp4)

[Télécharger le projet HyperFrames complet](https://raw.githubusercontent.com/mbairamadji007/starter/main/videos/omniflow-voix-off-source.zip)

Publicité de 15 secondes, 1920 × 1080, 60 images/s, avec voix féminine française, musique à 120 BPM et effets synchronisés. Le montage reprend les mouvements des références fournies : portail lumineux, interface en perspective, gros plan sur le réseau et clic d’optimisation.

La narration accompagne les quatre séquences :

- « Votre logistique vous échappe ? »
- « OmniFlow. Un seul dashboard. Zéro latence. »
- « Plus cent quarante pour cent d’efficacité. »
- « Démarrez votre essai gratuit. »

Pour modifier et rendre le film, extraire l’archive puis ouvrir le dossier `omniflow`. Avec Node.js 22 ou supérieur, FFmpeg et Chromium :

```bash
npm ci
npm run preview
npm run render
```

Le rendu est créé dans `renders/omniflow-voix-off.mp4`. Les prises vocales et les stems sont fournis dans `assets/audio/` ; les repères, le mixage et les instructions de régénération sont dans `SOUND_DESIGN.md`. La voix est synthétisée avec Siwis/Piper, avec sa provenance et ses attributions dans `NOTICE.md`.
