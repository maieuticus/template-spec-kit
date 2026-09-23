# Spec Kit Quickstart (Generisch)

## VS Code öffnen

Projektordner in VS Code öffnen.

---

## Terminal öffnen

```bash
pwd
git status
python3 --version
```

---

## uv installieren (falls nötig)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
exec $SHELL -l
uv --version
```

---

## Spec Kit installieren

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify version
```

---

## Git-Repository initialisieren (falls nötig)

```bash
git init
```

Prüfen:

```bash
git status
```

---

# Spec Kit initialisieren

## Für GitHub Copilot

```bash
specify init . --integration copilot --script sh
```

## Für Cursor

```bash
specify init . --integration cursor-agent --script sh
```

---

# VS Code vorbereiten

- Workspace vertrauen
- Copilot Chat öffnen
- Agent-Modus auswählen

Shortcut:

```text
Ctrl + Alt + I
```

---

# Spec-Driven Workflow

## Constitution erstellen

```text
/speckit.constitution Create simple project principles with minimal complexity, readable code, small scope, and maintainable structure.
```

---

## Fachliche Spezifikation erstellen

```text
/speckit.specify Describe the feature or system you want to build in business terms without implementation details.
```

---

## Anforderungen klären

```text
/speckit.clarify Clarify open questions, constraints, scope, assumptions, and expected behavior.
```

---

## Technischen Plan erzeugen

```text
/speckit.plan Define the technical implementation approach, architecture, technologies, structure, testing strategy, and local development workflow.
```

---

## Tasks erzeugen

```text
/speckit.tasks
```

---

## Optional Analyse

```text
/speckit.analyze
```

---

# Implementierung durch Agent

```text
/speckit.implement
```

---

# Änderungen prüfen

## Geänderte Dateien anzeigen

```bash
git status
```

---

## Änderungen im Detail prüfen

```bash
git diff
```

---

# Abhängigkeiten installieren

```bash
uv sync
```

---

# Tests ausführen

```bash
uv run pytest
```

---

# Git Commit

```bash
git add .
git commit -m "Initialize Spec Kit project"
git push
```

---

# Nützliche Checks

## Spec Kit prüfen

```bash
specify check
```

---

## Projektstruktur prüfen

```bash
find . -maxdepth 4 -type f | sort
```

---

# Typischer Ablauf

```text
1. Repo öffnen
2. Spec Kit initialisieren
3. Constitution erstellen
4. Spezifikation schreiben
5. Anforderungen klären
6. Technischen Plan erzeugen
7. Tasks erzeugen
8. Analyse prüfen
9. Implementieren lassen
10. Änderungen testen und committen
```


