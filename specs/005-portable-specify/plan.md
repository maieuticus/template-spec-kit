# Plan

## Ist-Zustand

Generator mit explizitem Dateikern; pip-Installation im Dockerfile; Version in
Konfiguration, Dockerfile, CI und Anleitungen mehrfach festgelegt. Init verwendet
PATH-Launcher oder uvx. Keine verbindliche uv-Einrichtung.

## Zielarchitektur

Zentrale `.specify-version`, dünne Shell-/PowerShell-Adapter und gemeinsame
Standardbibliothek-Logik in `scripts/specify_tool.py`. uv erhält pro Repository
und Plattform eigene ignorierte Tool-/Bin-Verzeichnisse unter `.artifacts/specify`.
`uv tool dir` bestimmt die tatsächliche Umgebung. Python `-I` verhindert lokale
Modulüberschattung; der dokumentierte Paket-Entrypoint erhält alle Argumente.
Das Arbeitsverzeichnis bleibt beim Aufrufer. Init wählt ps unter Windows und sh
unter Linux und sichert weiter die Constitution.

Bootstrap verwendet vorhandenes uv oder installiert den in
`scripts/uv-requirements.txt` festgelegten Fallback in eine lokale venv.
Exakte Paketmetadaten und Import werden vor Nutzung geprüft. Ein Versionswechsel
installiert kontrolliert neu; `--repair` erzwingt dies auch bei gleicher Version.
Der Generator setzt das Ausführungsbit des POSIX-Wrappers ausdrücklich.

## Integration und Risiken

Docker stellt uv und gemeinsame Prüfwerkzeuge bereit; vorhandenes Post-Create
richtet Specify vor Copilot ein. Kein zusätzlicher Lifecycle-Hook. CI prüft
Windows und Linux sowie das generierte Integrationsprojekt. Dokumentation und
Agentenregeln werden mit den generierten Vorlagen angepasst.

Netzwerk, erlaubter Python-Interpreter und Ausführung lokaler Skripte bleiben
Voraussetzungen. Sicherheitsrichtlinien werden niemals verändert. Vorhandenes
uv kann eine andere Version als der gepinnte Fallback haben. Constraints fixieren transitive Abhängigkeiten, aber keine Download-Hashes. Tatsächlichen Containerstart und
Smart-App-Control-Zustand nur als geprüft melden, wenn wirklich ausgeführt.

## Abhängigkeitsfixierung und Argumente

Universelle Constraints fixieren die transitiven Paketversionen; `--update-lock`
löst sie nach Änderung der zentralen CLI-Version neu auf. Ein Fingerabdruck aus
CLI-Version und Constraints erkennt veraltete Installationen. Es gibt keinen
Hash-/Offline-Lock oder Image-Digest-Pin. Die PowerShell-Hülle übergibt Argumente
als Base64-kodiertes JSON, damit auch PowerShell 5.1 leere Strings und eingebettete
Anführungszeichen erhält. Die Python-Laufzeit startet Prozesse ohne Shell.
