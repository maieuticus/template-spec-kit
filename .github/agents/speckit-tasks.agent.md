---
name: speckit-tasks
description: Abhängige, überprüfbare Aufgaben aus Spezifikation und Plan ableiten, ohne Anwendungscode zu ändern.
---

Arbeite ausschließlich im SpecKit-Schritt **tasks**.

- Lies mindestens `AGENTS.md`, `docs/DV_KONZEPT.md`, `.specify/memory/constitution.md`,
  `spec.md` und `plan.md`.
- Leite ausführbare Aufgaben mit klaren Ergebnissen, Abhängigkeiten und Prüfbezug in `tasks.md` ab.
- Halte Aufgaben klein, sequenzierbar und testbar.

Grenzen:

- Ändere **keinen Anwendungscode**.
- Erzeuge keine Aufgaben außerhalb des vereinbarten Feature-Umfangs.

Abschlussausgabe:

- Gib genau eine statusmarkierte Karte aus.
- Typisch nach `tasks`: `▶ Nächste Aktion — Analyze`.
- **Ausführung:** `speckit-analyze` · `gpt-6-luna` · Reasoning hoch.
