# Spec Kit Quickstart – Befehle mit Kurz­erklärung

```bash
pwd
```
Zeigt, in welchem Ordner du gerade bist.

```bash
git status
```
Zeigt den aktuellen Git-Zustand: geänderte Dateien, Branch, offene Commits.

```bash
python3 --version
```
Prüft, ob Python installiert ist und welche Version verwendet wird.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Installiert `uv`, einen schnellen Python-Paket- und Projektmanager.

```bash
exec $SHELL -l
```
Lädt die Shell neu, damit der frisch installierte `uv`-Befehl direkt verfügbar ist.

```bash
uv --version
```
Prüft, ob `uv` korrekt installiert wurde.

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```
Installiert das Spec-Kit-CLI-Tool `specify`.

```bash
specify version
```
Prüft, ob Spec Kit korrekt installiert wurde.

```bash
git status
```
Prüft erneut, ob du dich in einem Git-Repository befindest und ob Dateien geändert wurden.

```bash
specify init . --integration copilot --script sh
```
Initialisiert Spec Kit im aktuellen Ordner für GitHub Copilot.

```bash
specify init . --integration cursor-agent --script sh
```
Alternative: Initialisiert Spec Kit für Cursor.

```bash
specify check
```
Prüft, ob die Spec-Kit-Struktur vollständig und konsistent ist.

```bash
uv sync
```
Installiert die Projektabhängigkeiten aus der `uv`-Konfiguration.

```bash
uv run pytest
```
Führt die Tests mit `pytest` in der `uv`-Umgebung aus.

```bash
git status
```
Zeigt, welche Dateien nach Installation, Tests oder Änderungen betroffen sind.

```bash
git diff
```
Zeigt die konkreten Änderungen im Detail.

```bash
git add .
```
Merkt alle aktuellen Änderungen für den nächsten Commit vor.

```bash
git commit -m "Initialize Spec Kit project"
```
Erstellt einen Git-Commit mit der angegebenen Nachricht.

```bash
git push
```
Lädt den Commit in das entfernte GitHub-Repository hoch.
