# Plan: Analyze-Gate vor Implementierung

**Branch**: `004-analyze-gate` | **Date**: 2026-10-25 | **Spec**: [spec.md](spec.md)

## Zusammenfassung

Der Spec-Kit-Workflow validiert den Analysebericht vor dem manuellen
Entscheidungspunkt zwischen `analyze` und `implement`. Nur ein vollständiger
Bericht ohne offene wesentliche Befunde erreicht den Gate. Der Gate nutzt den
vorhandenen Typ `gate` mit `approve` und `reject`; die bewusste Freigabe bleibt
erforderlich.

## Technischer Kontext

- **Workflow und Version:** YAML-Workflow `.specify/workflows/project-sdd/workflow.yml`;
  Spec-Kit CLI `1.0.7` gemäß `config/project.yaml`.
- **Prüfwerkzeuge:** Python ab 3.11, PyYAML und `unittest` sind bereits vorhanden.
- **Datenhaltung:** Keine Laufzeitdatenbank. `analyze.md` ist das nachvollziehbare
  Feature-Artefakt für Analysebefunde.
- **Abhängigkeiten und Dienste:** Keine neuen Pakete, Dienste oder externen Zugriffe.
- **Umfang:** Workflow, `scripts/check_analyze_gate.py`, Agentenprofil,
  DV-Konzept samt Basisvorlage, Generator-Kernliste und Regressionstests.

## Architektur und Verträge

1. `analyze-report-check` läuft direkt nach `analyze` und vor dem Gate. Das
   `scripts/check_analyze_gate.py` liest `.specify/feature.json`, löst
   `feature_directory` innerhalb des Repository-Ordners `specs/<feature>/` auf
   und prüft dort `analyze.md`. Fehlender/ungültiger Kontext, fehlender Bericht
   oder ungültiges Format brechen mit Fehler ab.
2. `analyze.md` enthält `## Wesentliche Befunde`. Wenn es keine gibt, steht
   dort exakt `Keine wesentlichen Befunde.`. Jeder Befund ist eine Überschrift
   `### A001 — P1: ...` und enthält genau je eine Zeile `**Status:** offen`,
   `**Status:** geklärt` oder `**Status:** akzeptiert` sowie eine nichtleere
   `**Begründung:**`. `geklärt` erfordert zusätzlich `**Geändertes Artefakt:**`.
   Fehlende, doppelte oder unbekannte Felder brechen fail-closed ab.
3. Jeder als wesentlich eingestufte Befund steht in diesem Abschnitt. Status
   `offen` blockiert; Status `geklärt` oder `akzeptiert` darf zum Gate führen.
   Andere Hinweise gehören in einen separaten Abschnitt. Redaktionelle
   Hinweise blockieren nicht.
4. Bei erfolgreicher Prüfung gibt das Skript den validierten relativen
   Berichtsweg als JSON aus. Der Gate zeigt genau diese geprüfte Datei an und
   verlangt danach weiterhin eine ausdrückliche Freigabe. Damit kann `approve`
   keinen offenen wesentlichen Befund übersteuern.
5. Die Definition „wesentlich“ bleibt konsistent mit `spec.md`: Auswirkungen
   auf Akzeptanzkriterien, Schnittstellen, Daten, Sicherheit oder Betrieb.
   Das Agentenprofil und beide DV-Anleitungen dokumentieren denselben
   Berichtsvertrag.

## Verfassung und Projektkontext

- **Überprüfbare Ergebnisse:** Der Workflow erhält einen strukturellen
  Regressionstest und Laufzeitnachweise für offenen, fehlenden und gültigen
  Bericht. YAML-Validierung allein genügt nicht.
- **Ein verbindliches DV-Konzept:** Die Regeln werden in
  `docs/DV_KONZEPT.md` und der generierten Basisvorlage
  `templates/base/files/docs/DV_KONZEPT.md.template` parallel gepflegt.
- **Technologie nach Bedarf:** Der Validator nutzt die bereits vorhandene
  Python-Laufzeit; neue Pakete oder Dienste werden nicht eingeführt.
- **Verträge und Daten:** Es gibt keine öffentliche API, Datenbankänderung
  oder Migration. Der Vertrag besteht aus dem Gate-Schema und dem
  dokumentierten `analyze.md`-Format.
- **Reproduzierbarkeit:** Die Prüfung verwendet die bereits festgelegte CLI-
  Version 1.0.7 und die vorhandenen Projektprüfungen.
- **Wiederverwendbares Wissen:** Befundregeln werden in den generierten
  Anweisungen dokumentiert, nicht projektspezifisch in eine neue
  Architekturdatei ausgelagert.

## Projektstruktur und betroffene Dateien

- `.specify/workflows/project-sdd/workflow.yml` — Gate-Schritt und
  fail-closed-Prüfschritt ergänzen.
- `scripts/check_analyze_gate.py` — Feature-Kontext, Befundformat und Status
  vor der Freigabe validieren.
- `scripts/create_project.py` — Validator in `CORE_FILES` aufnehmen.
- `.github/agents/speckit-analyze.agent.md` — den Bericht im validierbaren
  Format erzeugen.
- `docs/DV_KONZEPT.md` — manuellen und automatisierten Ablauf,
  `analyze.md`-Vertrag und Ablehnungs-/Freigaberegel beschreiben.
- `templates/base/files/docs/DV_KONZEPT.md.template` — dieselbe
  generische Anleitung für neu erzeugte Projekte pflegen.
- `tests/test_template.py` — Validator, Befundformat, Workflow und generierte
  Anleitungen regressionssichern.
- `specs/004-analyze-gate/tasks.md` — Aufgaben und Abnahmen aus Plan und Spec
  ableiten und nach tatsächlicher Prüfung abhaken.

## Risiken und Gegenmaßnahmen

- **Feature-Kontext fehlt:** Das Skript verlangt `.specify/feature.json` mit
  einem gültigen Pfad unter `specs/`; es gibt keinen stillen Branch- oder
  Dateifallback.
- **Berichtsformat driftet:** Validator, Agentenprofil, DV-Anleitungen und
  Regressionstest teilen denselben expliziten Feldvertrag.
- **Manuelle Befundprüfung:** Ein manueller Gate kann Befunde nicht
  automatisch klassifizieren. Klare Wesentlichkeitskriterien, ein explizites
  `analyze.md`-Format und eine deutliche Gate-Meldung begrenzen das Risiko;
  automatische Analyse oder Freigabe ist ausgeschlossen.
- **Bedienungsänderung:** Ein interaktiver Workflow benötigt nach Analyze
  eine bewusste Auswahl. Dies betrifft nur den lokalen Workflow-Lauf; Generator-
  und Anwendungsprüfungen werden nicht interaktiv verändert.

## Prüfung

1. Unit-Tests prüfen fehlenden Feature-Kontext/Bericht, offenes und unbekanntes
   Statusfeld, unvollständige geklärte Befunde sowie gültige/leere Berichte.
   Der Workflow-Test prüft die Reihenfolge, den geprüften `show_file`-Pfad,
   beide Gate-Optionen, Folgeaktionen und den Vertrag im generierten DV-Konzept.
2. Mit Spec-Kit CLI 1.0.7 werden temporäre Abläufe für offenen Bericht
   (Abbruch vor Gate), fehlenden Bericht (Abbruch vor Gate), gültigen Bericht
   mit `reject` (Abbruch vor dem Folgeschritt) und gültigen Bericht mit
   `approve` (Gate zeigt den Bericht und führt zum Folgeschritt) ausgeführt.
3. `python scripts/check.py --static-only` prüft Dokumentlinks und Syntax.
4. `python scripts/check.py` führt zusätzlich Generator- und Profilprüfungen aus.

## Rollout und Rückweg

Der geänderte Workflow gilt nach dem Update für folgende lokale Läufe; es gibt
keine Datenmigration oder Änderung an generierten Laufzeitdiensten. Bei einem
Fehler kann der Validierungsschritt zusammen mit dem Gate zurückgenommen
werden. Der Status des aktiven Features und die tatsächlichen Prüfungen werden
im DV-Konzept festgehalten.
