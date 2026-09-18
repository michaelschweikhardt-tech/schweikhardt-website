# Oona Schweikhardt – Portfolio (schweikhardt.de/oona/)

Statischer Nachbau von oonaschweikhardt.cargo.site. Live unter **https://schweikhardt.de/oona/**.

- `../oona/` = fertige Website. Jede Änderung dort → Workflow **„Deploy Oona-Portfolio“** lädt nur diesen Ordner nach Strato (`<Webroot>/oona`).
- `tools/build.py` erzeugt alle Seiten neu aus `content/pages.json` (Cargo-Inhalt) und `content/layout.json` (vermessene Galerie-Layouts). Ausgabe nach `oona-src/site` → danach nach `oona/` kopieren.
- Medien: WebP 640/1280/2000 px, Videos H.264. Schriften lokal (Inter Tight, Inter, Archivo, IBM Plex Mono – OFL), kein Google-Fonts-Abruf, kein Tracking.
- Textänderung: direkt in `oona/<seite>/index.html` (geht auch im GitHub-Webeditor).
