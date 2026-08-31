# Go-Live — letzter Schritt (ca. 2 Minuten)

Alle Dateien der neuen Website liegen fertig in diesem Ordner (`website-repo/`).
Es fehlt nur der Push zu GitHub. Zwei Wege — nimm einen:

## Weg A: Terminal (empfohlen)
Öffne Terminal und kopiere Block für Block:

    cd "/Users/michaelschweikhardt/Documents/02 Jobs/00 Schweikhardt/2026_Eigenmarketing/website-repo"
    rm -f .git/index.lock
    git add -A
    git commit -m "Relaunch: seriöses Design, Leistungsseiten, Case-Studies, Referenzen, Werdegang, Impressum/Datenschutz"

Falls noch KEIN Remote gesetzt ist (prüfen mit `git remote -v`):

    git remote add origin https://github.com/<DEIN-GITHUB-USER>/schweikhardt-website.git

Dann veröffentlichen (überschreibt den alten Web-Upload-Stand vollständig):

    git push -u origin master --force

Nach 1–2 Minuten ist der neue Stand unter https://neu.schweikhardt.de live.

## Weg B: GitHub Desktop (ohne Terminal)
1. GitHub Desktop öffnen → File → Add Local Repository → diesen Ordner wählen.
2. Unten links Commit-Nachricht eintippen → "Commit to master".
3. Oben "Push origin" (bzw. "Publish repository", Repo: schweikhardt-website) klicken.

## Danach (separat, wenn du willst)
- Domain-Umzug schweikhardt.de → neue Seite: bei Strato den DNS-Eintrag auf GitHub Pages zeigen lassen (ersetzt die alte WordPress-Seite). Sag Bescheid, dann gehen wir den DNS-Schritt zusammen durch.
- Optional: Google-Fonts lokal einbinden (dann entfällt der Google-Abschnitt im Datenschutz).
