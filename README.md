# schweikhardt.de — Onepager

Statische Website: eine HTML-Datei, keine Build-Tools, keine Abhängigkeiten.
Änderungen werden direkt in `index.html` gemacht und mit jedem Push automatisch veröffentlicht.

## Struktur

```
index.html            Die komplette Website (Inhalt + Design in einer Datei)
design-manual.html    Design-System zum Nachschlagen
CHANGELOG.md          Was wann geändert wurde
CNAME                 Die verwendete Domain: neu.schweikhardt.de
assets/
  portrait-teal.jpg   Duotone-Porträt, Hero
  portrait-orange.jpg Duotone-Porträt, Über mich
  favicon.svg
```

## Stand

Terminbuchung (Calendly), WhatsApp, E-Mail, Impressum, Datenschutz und LinkedIn sind verknüpft und funktionsfähig.

Offen: In der Werkschau stehen noch drei Platzhalterflächen. Sobald die Creatives vorliegen, werden sie durch
`<img src="assets/creative-…jpg" alt="…">` ersetzt.

## Veröffentlichen mit GitHub Pages

1. Auf github.com ein neues, **öffentliches** Repository anlegen, z. B. `schweikhardt-website`.
2. Die Dateien dieses Ordners hochladen (im Browser: *Add file → Upload files*, Ordner `assets` mit hineinziehen).
3. Im Repository unter **Settings → Pages**: Source auf `Deploy from a branch`, Branch `main`, Ordner `/ (root)`, speichern.
4. Nach ein bis zwei Minuten ist die Seite unter `https://<benutzername>.github.io/schweikhardt-website/` erreichbar.

### Eigene Domain

Da `schweikhardt.de` weiterhin auf WordPress läuft, bietet sich eine Subdomain an, etwa `neu.schweikhardt.de` oder `michael.schweikhardt.de`:

1. Datei `CNAME` im Repository anlegen, Inhalt: die gewünschte Subdomain (nur die Domain, keine Leerzeichen).
2. Beim Domain-Anbieter einen CNAME-Eintrag setzen: `neu` → `<benutzername>.github.io`
3. In **Settings → Pages** die Domain eintragen und *Enforce HTTPS* aktivieren.

Sobald die neue Seite steht, kann sie später per Weiterleitung auf die Hauptdomain gehoben werden.

## Änderungen machen

Kleinigkeiten (Texte, Zahlen, Links) lassen sich direkt auf github.com bearbeiten: Datei öffnen, Stift-Symbol, ändern, *Commit changes*. Die Seite aktualisiert sich innerhalb einer Minute.

Jede Änderung ist versioniert — unter *Commits* lässt sich jeder frühere Stand ansehen und wiederherstellen. Nichts geht verloren, nichts muss von vorn gebaut werden.

## Tracking

Der Google-Tag-Manager-Container `GTM-WZC6K2B` ist noch **nicht** eingebunden. Falls gewünscht, kann er ergänzt werden — sinnvolle Events wären: Klick auf „Erstgespräch buchen", Klick auf WhatsApp, Klick auf E-Mail.
