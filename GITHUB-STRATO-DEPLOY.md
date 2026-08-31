# Auto-Deploy: GitHub → Strato (SFTP)

**Was das macht:** Jeder Push auf `main` lädt die Website automatisch per SFTP zu Strato.
Der Upload ist **rein additiv** (`mirror -R` **ohne** `--delete`): Es werden nur die
Website-Dateien hochgeladen/überschrieben — **nie etwas auf dem Server gelöscht**.
Deine App-Unterverzeichnisse (`reporting/`, `sofaconcerts/`, `bridgeandtunnel/`,
`mickyoye/`, `pampa/`, `oona/`, `fokusnest/`, `meta-poster/`, `audit/` …) werden
technisch gar nicht angefasst.

Die Strato-Zugangsdaten liegen als **GitHub-Secrets** — ich sehe sie nie.

---

## Einmalige Einrichtung (du, ~15 Min.)

### Schritt 1 — Strato: SSH/SFTP-Zugang + Daten
Im STRATO-Kundenlogin unter **Hosting → Zugriff/SFTP** den SSH-/SFTP-Zugang
aktivieren (falls noch nicht aktiv) und notieren:
- **Host:** i. d. R. `ssh.strato.de` — **Port 22**
- **Benutzername** (SFTP-User)
- **Passwort**
- **Webroot-Pfad:** genau der Ordner, in den du zuletzt die Website per SFTP geladen hast
  (dort liegen `index.html` und die App-Ordner). Oft landet der SFTP-Login direkt dort.

### Schritt 2 — GitHub: Secrets + Variable anlegen
Repo → **Settings → Secrets and variables → Actions**.

Unter **Secrets** → „New repository secret" (dreimal):
| Name | Wert |
|---|---|
| `STRATO_SFTP_HOST` | z. B. `ssh.strato.de` |
| `STRATO_SFTP_USER` | dein SFTP-Benutzername |
| `STRATO_SFTP_PASSWORD` | dein SFTP-Passwort |

Unter **Variables** → „New repository variable":
| Name | Wert |
|---|---|
| `STRATO_WEBROOT` | der Webroot-Pfad aus Schritt 1. **Wenn der SFTP-Login direkt im Webroot landet: leer lassen oder `.`** |

### Schritt 3 — Vollstand einmalig zu GitHub pushen
Das Repo hängt noch auf dem alten Onepager-Stand. Einmalig den kompletten
aktuellen Stand (inkl. Blog + Deploy-Action) hochladen. Im Terminal auf deinem Mac:

```bash
cd "/Users/michaelschweikhardt/Documents/02 Jobs/00 Schweikhardt/2026_Eigenmarketing/website-repo"
find .git -name '*.lock' -delete 2>/dev/null
rm -rf .git
git init
git branch -M main
git add -A
git commit -m "Vollstand: Multi-Page-Website + Blog + Strato-Deploy-Action"
git remote add origin https://github.com/michaelschweikhardt-tech/schweikhardt-website.git
git push -u origin main --force
```

> Reihenfolge wichtig: **erst Schritt 2** (Secrets), **dann Schritt 3** (Push).
> Der Push löst die Action sofort aus.

### Schritt 4 — Erste Ausführung prüfen
Repo → **Actions** → den laufenden „Deploy zu Strato"-Job öffnen.
- Log zeigt unter „Zu deployende Dateien" alle Live-Dateien und dann den SFTP-Upload.
- Grün = fertig. Dann testen:
  - `https://schweikhardt.de/blog.html` lädt
  - eine App weiter erreichbar, z. B. `https://schweikhardt.de/reporting/`
- Rot? Meist falscher Host/User/Pass oder Webroot. Der Job **lädt bei Fehler nichts hoch
  und löscht nichts** — einfach Werte korrigieren und „Re-run job".

---

## Danach: laufende Updates
Ab dann übernehme ich Änderungen an der Website direkt: Dateien im Ordner `website-repo`
bearbeiten und über GitHub committen — die Action deployt automatisch zu Strato.
Voraussetzung fürs Committen bleibt eine bei GitHub angemeldete Browser-Sitzung
(wie beim letzten Go-live), da ich keine Git-Zugangsdaten halte.

## Sicherheits-Design (kurz)
- **Kein `--delete`** → nie Löschungen auf dem Server, App-Ordner unantastbar.
- Zugangsdaten nur als GitHub-Secrets, in Logs maskiert.
- Fehlerhafte Läufe sind folgenlos (kein Teil-Zustand): erst verbinden, dann spiegeln.
