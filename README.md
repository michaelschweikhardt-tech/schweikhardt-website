# schweikhardt.de — Website

Statische Multi-Page-Website (HTML/CSS, keine Build-Tools, keine Abhängigkeiten).
Gemeinsames Stylesheet `style.css`, geteilte Navigation/Footer auf allen Seiten.

## Seitenbestand
- `index.html` — Startseite
- Leistungen: `digital.html` (Beratung) · `paid-social.html` (Marketing) · `retro.html` (Studio)
- `referenzen.html` + 10 Case-Detailseiten `case-*.html`
- `vita.html` (Werdegang) · `impressum.html` · `datenschutz.html` · `404.html`
- **Blog:** `blog.html` (Übersicht + Tag-Filter) und die Artikel
  `blog-reporting-tool.html`, `blog-hook-hold-rate.html`, `blog-deckungsbeitrag-statt-roas.html`
- `.htaccess` — 301-Redirects alter WordPress-URLs + `ErrorDocument 404`
- `assets/` — Bilder, Logos, Case-Bilder (`assets/cases/`)
- `design-manual.html` — Design-System zum Nachschlagen (nicht Teil des Live-Deploys)

## Hosting / Deploy
**Live-Host ist Strato** (statische Dateien im Webroot von `schweikhardt.de`),
**nicht** GitHub Pages. Dieses Repo ist die Quelle/Versionierung.

Deploy erfolgt aktuell **manuell per SFTP**: den Inhalt von `../strato-deploy/`
(sauberer Spiegel dieses Repos ohne Dev-Dateien) in den Strato-Webroot hochladen,
vorhandene Dateien überschreiben. Die App-Unterverzeichnisse (reporting/, sofaconcerts/,
bridgeandtunnel/, mickyoye/ …) bleiben unangetastet.

> Ein Push in dieses Repo veröffentlicht **nichts** automatisch, solange keine
> GitHub-→-Strato-FTP-Action eingerichtet ist. Siehe `../STRATO-UMZUG.md`.

## Änderungen
Editieren, committen, pushen (`main`). Danach Deploy nach Strato (s. o.).
