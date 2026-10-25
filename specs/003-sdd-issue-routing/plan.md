# Plan: Schrittführung, Modellempfehlung und Template-Issue-Routing

## Umsetzung

- `AGENTS.md` und `.github/copilot-instructions.md` erhalten dieselben
  verbindlichen Regeln für Schrittführung, Modellprofil, Reasoning-Stufe,
  Abgrenzung und Issue-Vorschläge.
- Die allgemeine Copilot-Anweisung wird über `CORE_FILES` in alle Projekte
  übernommen. Beim API-Rezept fügt der Generator den bestehenden API-Kontext
  an, statt die allgemeine Anweisung zu überschreiben.
- Das Basis-DV-Konzept erklärt die Regeln für Folgeprojekte; das
  Template-DV-Konzept verweist auf Feature 003 und pflegt den Arbeitsstand.
- Generator-Tests prüfen die gemeinsame Anweisung für Standardprojekte und
  zusätzlich den erhaltenen API-Kontext für API-Projekte.

## Prüfung

- `python scripts/check.py`
- `tests/test_template.py`: erzeugte Standard- und API-Projekte enthalten die
  allgemeine Anweisung; das API-Projekt enthält weiterhin API-spezifische
  Hinweise.

## Abhängigkeiten

Keine neuen Pakete, Dienste oder externen Zugriffe.
