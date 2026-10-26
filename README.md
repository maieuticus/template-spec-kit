# template-spec-kit

**[Aktueller Arbeitsstand →](docs/DV_KONZEPT.md#aktueller-arbeitsstand)**

Zuletzt erledigt · Aktuell in Arbeit · Nächste Schritte · Blockaden

**Vor Weiterarbeit:** Die [priorisierten offenen Entscheidungen zum Codespace-Test](docs/DV_KONZEPT.md#priorisierte-offene-entscheidungen)
zuerst gemeinsam und einzeln behandeln.

Technologieoffenes Projektgrundgerüst für Spec-Driven Development. Ein gemeinsamer
Kern wird mit einem Technologieprofil und den benötigten Diensten kombiniert.

**Projektziel, Architektur, Entwicklung und Betrieb stehen zusammen im
[DV-Konzept](docs/DV_KONZEPT.md).**

## Spec Kit aktivieren: Desktop und Codespaces

Die Agentenprofile und Projektvorlagen sind enthalten. Die Spec-Kit-Integration
wird je Projekt eingerichtet; ein neuer Codespace erfordert keine erneute
Initialisierung einer bereits versionierten Integration.

- **Desktop-VS-Code mit Codex:** Der [Windows-Ablauf](docs/DV_KONZEPT.md#codex-mit-windows-powershell-initialisieren)
  richtet die Skills ein. Danach eine neue Codex-Sitzung im Projekt öffnen und
  beispielsweise `$speckit-specify` mit dem Feature-Auftrag senden.
- **GitHub Codespaces mit Copilot:** Die [Codespace-Einrichtung](docs/DV_KONZEPT.md#copilot-cli-im-codespace)
  und die [Agent-Integration](docs/DV_KONZEPT.md#agent-integration-und-chat-aufrufe)
  durchführen. Das vorhandene Post-Create-Skript installiert die Copilot CLI;
  falls diese Einrichtung scheitert, im Bash-Terminal nachholen:

  ```sh
  curl -fsSL https://gh.io/copilot-install | bash
  ```

  Falls `copilot` danach nicht gefunden wird, das vom Installer ausgegebene
  `export PATH=...` in die Shell-Konfiguration übernehmen und ein neues Terminal
  öffnen. Danach `python scripts/init_speckit.py --integration copilot`
  ausführen und im Copilot-Chat `/speckit-specify` verwenden. In VS Code können
  die mitgelieferten `speckit-*`-Profile auch über die Agentenauswahl im
  Copilot-Chat gewählt werden.

Mit dem Wrapper (`./scripts/specify integration list`, unter Windows
`.\scripts\specify.ps1 integration list`) den vorhandenen Zustand zuerst prüfen. Für eine
zusätzliche Integration die [Integrationsverwaltung](docs/DV_KONZEPT.md#bestehende-integrationen)
verwenden. GitHubs **Use this template** kopiert das Repository; der
[Generator](#2-ein-eigenes-projekt-erzeugen) erstellt daraus das Anwendungsprojekt.

## Neuer Codespace: Copilot oder Codex starten

Dieser Einstieg gilt für neue und bestehende Projekte sowie für jeden neu
angelegten Codespace. **Diesen Abschnitt beim Ausfüllen der Projekt-README
beibehalten.** Installierte Werkzeuge und Anmeldungen gehören zur jeweiligen
Entwicklungsumgebung.

1. Auf GitHub das Repository und den gewünschten Branch öffnen, dann
   **Code → Codespaces → Create codespace** wählen und den Containeraufbau abwarten.
2. Ein Bash-Terminal im Projektverzeichnis öffnen.
3. Den gewünschten Agenten einrichten:
   - **Copilot CLI im Terminal:** [Node.js/nvm, Installation, Anmeldung und Start](docs/DV_KONZEPT.md#copilot-cli-im-codespace).
   - **Codex in VS Code:** [Codespace in VS Code öffnen und Codex einrichten](docs/DV_KONZEPT.md#codex-in-vs-code).
4. Bei einem bestehenden Projekt am
   [aktuellen Arbeitsstand](docs/DV_KONZEPT.md#aktueller-arbeitsstand) weiterarbeiten.
   Spec Kit wegen eines neuen Codespaces nicht erneut initialisieren.

Nach Stoppen und Wiederöffnen desselben Codespaces genügt normalerweise der
Agentenstart. Nach einem neuen Codespace oder Container-Neubau die Installation
und Anmeldung prüfen; fehlende Werkzeuge nach der
[Codespace-Anleitung](docs/DV_KONZEPT.md#neuer-codespace-und-wiedereinstieg) wiederherstellen.

## Einstieg mit Spec Kit und Codex

Der Start erfolgt in dieser Reihenfolge: **Projekt erzeugen → Spec Kit für
Codex initialisieren → Projektziel und Constitution konkretisieren → erstes
Feature spezifizieren und umsetzen.** Die verbindlichen Details stehen im
[DV-Konzept – Einrichtung](docs/DV_KONZEPT.md#einrichtung).

### 1. Voraussetzungen bereitstellen

- Git und Python ab 3.11 für das Template.
- Für die unten gezeigte Codex-Installation: Node.js mit npm und ein Codex-Zugang.
- Für den Devcontainer zusätzlich Docker mit Compose und VS Code Dev Containers.
  Alternativ kannst du direkt unter Windows mit PowerShell arbeiten.

Installiere die Werkzeuge in der Umgebung, in der du Codex ausführen wirst.
Eine Windows-Installation steht im Linux-Devcontainer nicht automatisch bereit.

### 2. Ein eigenes Projekt erzeugen

Öffne dieses Repository lokal und führe im Template-Verzeichnis aus:

```sh
python -m pip install -r scripts/requirements.txt
python scripts/create_project.py --name mein-projekt --stack python --output ../mein-projekt
```

Alternativ ein API-Projekt einschließlich PostgreSQL:

```sh
python scripts/create_project.py --name meine-api --recipe api-service --output ../meine-api
```

Das Ziel muss leer sein oder noch nicht existieren. `--dry-run` zeigt die
vorgesehenen Dateien, ohne ein Projekt anzulegen. Rohmaterialien dieses
Repositories, der Bausteinkatalog, lokale Einstellungen und Secrets werden
nicht in neue Projekte übernommen.

Auch eine über GitHubs **Use this template → Create a new repository** angelegte
und anschließend geklonte Kopie dient zunächst als Generator. Erzeuge daraus
dein Anwendungsprojekt in einem leeren Ziel; siehe
[Projekterzeugung](docs/DV_KONZEPT.md#neues-projekt-erzeugen).

Das Template enthält die Branches `main` und `development`. Beim Erzeugen über
die GitHub-Oberfläche **Include all branches** aktivieren, damit beide Branches
in der neuen Repository-Kopie angelegt werden. Mit der GitHub CLI:

```sh
gh repo create mein-projekt --template maieuticus/template-spec-kit --private --include-all-branches
```

Ohne diese Option übernimmt GitHub nur den Default-Branch `main`.

Wechsle anschließend in das erzeugte Projekt (beim API-Beispiel in `../meine-api`):

```sh
cd ../mein-projekt
git init
git status
```

Der Generator legt kein Git-Repository an. Öffne jetzt den **erzeugten Ordner**
im Editor und installiere die Abhängigkeiten aus dessen DV-Konzept, Abschnitt
„Einrichtung“. Prüfe die erzeugten Dateien und sichere den Ausgangsstand mit
einem lokalen Commit, bevor du Spec Kit initialisierst.

### 3. Codex installieren und Spec Kit initialisieren

Die [portable Specify-Laufzeit](docs/DV_KONZEPT.md#portable-specify-laufzeit)
verwendet die zentrale `.specify-version`. Im Devcontainer/Codespace erfolgt
das Setup automatisch, lokal einmalig:

```sh
python scripts/bootstrap_specify.py
```

Windows PowerShell:

```powershell
.\scripts\specify.ps1 version --features --json
npm.cmd install -g @openai/codex
python scripts/init_speckit.py --integration codex
```

Linux / Codespaces:

```sh
./scripts/specify version --features --json
python scripts/init_speckit.py --integration codex
```

Das Init-Skript erhält die Constitution und wählt automatisch PowerShell oder
Bash. Codex gemäß [Anleitung](docs/DV_KONZEPT.md#codex-installieren) bereitstellen.
Unter Windows verwendet der Wrapper den Python-Entrypoint statt `specify.exe`;
Smart App Control und persönliche Profile bleiben unverändert.

**GitHub Codespaces:** Das Post-Create-Skript richtet Specify und die Copilot CLI
ein. Folge der [Codespace-Einrichtung](docs/DV_KONZEPT.md#copilot-cli-im-codespace);
starte sie danach mit `copilot` und melde dich beim ersten Start über `/login`
an.

Nach erfolgreicher Initialisierung im Projekt-Terminal prüfen:

```sh
./scripts/specify integration list
git status
git diff
```

Codex muss als installiert erscheinen; unter `.agents/skills/` müssen die
`speckit-*`-Skills mit ihren `SKILL.md`-Dateien liegen. Prüfe auch die neuen,
noch unversionierten Dateien, die `git diff` allein nicht zeigt. Bei bereits
initialisierten Projekten gilt die
[Integrationsverwaltung](docs/DV_KONZEPT.md#bestehende-integrationen).

### 4. Codex starten und die Projektgrundlage konkretisieren

Starte nach erfolgreicher Initialisierung im Root-Verzeichnis des erzeugten
Projekts unter Windows:

```powershell
codex.cmd
```

Im Linux-Container lautet der Aufruf `codex`. Folge beim ersten Start dem
Anmeldedialog.

**Die folgenden `$speckit-*`-Aufrufe gehören in den Codex-Chat.** Sende sie
einzeln und prüfe jeweils das Ergebnis. Beginne einmalig mit:

```text
$speckit-constitution
Lies AGENTS.md, README.md, docs/DV_KONZEPT.md und die vorhandene
.specify/memory/constitution.md sowie die Projektstruktur und Tests.
Kläre mit mir Projektziel und offene Grundsatzentscheidungen. Konkretisiere
das DV-Konzept und passe die bestehende Constitution nur begründet und
versioniert an das Projekt an. Erhalte die Template-Prinzipien und benenne
Konflikte. Implementiere in diesem Schritt noch kein Feature.
```

Die mitgelieferte Constitution ist bereits die Grundlage. Eine zusätzliche
Vorlage unter `docs/templates/CONSTITUTION.md` wird hier nicht benötigt.

### 5. Das erste kleine Feature bearbeiten

Beschreibe zunächst Verhalten und Akzeptanzkriterien, zum Beispiel:

```text
$speckit-specify
Benutzer sollen über die Kommandozeile eine kurze Notiz lokal speichern können.
Akzeptanzkriterien: Eine nicht leere Notiz erhält eine ID; nach einem Neustart
kann sie über diese ID wieder gelesen werden; leere Eingaben werden mit einer
verständlichen Meldung abgewiesen.
Berücksichtige das DV-Konzept, vorhandenen Code, Datenmodelle und Tests.
```

Führe anschließend die passenden Schritte einzeln in Codex aus:

```text
$speckit-clarify
$speckit-plan
$speckit-checklist
$speckit-tasks
$speckit-analyze
$speckit-implement
$speckit-converge
```

Für Copilot sind die passenden Profile unter `.github/agents/` verfügbar,
einschließlich des Abschlussprofils `speckit-converge`.

Zweck und Ergebnisse der Schritte beschreibt der
[Feature-Ablauf im DV-Konzept](docs/DV_KONZEPT.md#manueller-ablauf-mit-codex).
Die Artefakte gehören nach `specs/<nummer>-<name>/`. Prüfe das Ergebnis gegen
die Akzeptanzkriterien und führe im Projekt-Terminal `python scripts/check.py`
sowie die relevanten Feature-Tests aus. Offene Aufgaben aus `converge`
nacharbeiten und erneut prüfen; anschließend Diff und neue Dateien durchsehen.

Beim nächsten Arbeitsstart öffnest du dasselbe Projekt, startest Codex und
arbeitest am bestehenden Feature weiter oder beginnst mit `$speckit-specify`
ein neues. Installation, Initialisierung und Constitution sind keine Schritte,
die du bei jedem Feature wiederholst. Wenn Skills fehlen, prüfe
die Wrapper-Ausgabe von `integration list` und `.agents/skills/` und starte Codex neu.

## Orientierung

| Thema | Einstieg |
| --- | --- |
| Einrichtung und täglicher Start | [Quickstart](QUICKSTART.md) |
| Template, Spec Kit und Agent erklärt | [Zusammenspiel](docs/DV_KONZEPT.md#zusammenspiel-von-template-spec-kit-und-agent) |
| Befehle verstehen und Probleme eingrenzen | [Befehle und Aufruforte](docs/DV_KONZEPT.md#befehle-und-aufruforte) |
| Copilot und andere Agenten | [Integrationen und Chat-Aufrufe](docs/DV_KONZEPT.md#agent-integration-und-chat-aufrufe) |
| Verbindliche Projektbeschreibung | [DV-Konzept](docs/DV_KONZEPT.md) |
| Entwicklungsmethodik | [Constitution](.specify/memory/constitution.md) |
| Feature-Spezifikationen | [Feature-Übersicht](specs/README.md) |
| Technologien, Dienste und API-Rezept | [Bausteinkatalog](templates/README.md) |
| Arbeitsregeln für Agenten | [AGENTS.md](AGENTS.md) |
| Referenz-Repositories und Beiträge | [DV-Konzept: Wissensaustausch](docs/DV_KONZEPT.md#wissensaustausch) |

## Prüfen

```sh
python scripts/check.py
```

Dies prüft Dokumentlinks, Dateisyntax und die Template-Tests. Die
[CI](.github/workflows/ci.yml) prüft zusätzlich erzeugte Projekte und Compose.
