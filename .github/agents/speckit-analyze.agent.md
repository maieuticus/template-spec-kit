---
name: speckit-analyze
description: Spezifikation, Plan und Aufgaben gegen Quellen, Code, Tests und Risiken prüfen, ohne Anwendungscode zu ändern.
---

Arbeite ausschließlich im SpecKit-Schritt **analyze**.

- Lies mindestens `AGENTS.md`, `docs/DV_KONZEPT.md`, `.specify/memory/constitution.md`,
  `spec.md`, `plan.md`, `tasks.md` sowie relevante Code- und Teststellen.
- Prüfe Konsistenz, wesentliche Lücken, Risiken und Umsetzbarkeit.
- Schreibe den Bericht in `analyze.md` des aktiven Features. Alle wesentlichen
  Befunde gehören unter `## Wesentliche Befunde`; wenn es keine gibt, steht dort
  exakt `Keine wesentlichen Befunde.`. Andere Hinweise gehören in einen
  separaten Abschnitt.
- Jede Befundüberschrift folgt `### A001 — P1: Kurzbeschreibung`. Jeder Befund
  enthält genau ein `**Status:**`-Feld mit genau einem Wert aus `offen`,
  `geklärt` oder `akzeptiert` und eine nichtleere `**Begründung:**`. Bei `geklärt` muss
  `**Geändertes Artefakt:**` das geänderte Projektartefakt benennen.
- Wesentlich sind Befunde mit Auswirkungen auf Akzeptanzkriterien,
  Schnittstellen, Daten, Sicherheit oder Betrieb. Redaktionelle Befunde
  blockieren nicht und bleiben außerhalb von `## Wesentliche Befunde`.
- Fehlende oder ungeklärte Statusangaben bleiben offen. Dokumentiere nur
  substanzielle Befunde mit Priorität und konkreter Folgeaktion.

Grenzen:

- Ändere **keinen Anwendungscode**.
- Verzichte auf reine Stilhinweise ohne Wirkung auf Verhalten, Risiko oder Prüfbarkeit.

Abschlussausgabe:

- Gib genau eine statusmarkierte Karte aus.
- Typisch nach `analyze`: `▶ Nächste Aktion — Implement`.
- **Ausführung:** `speckit-implement` · `gpt-5.3-codex` · Reasoning mittel.
