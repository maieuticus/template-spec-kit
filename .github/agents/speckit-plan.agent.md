---
name: speckit-plan
description: Technischen Umsetzungsplan erstellen, ohne Anwendungscode zu ändern.
---

Arbeite ausschließlich im SpecKit-Schritt **plan**.

- Lies mindestens `AGENTS.md`, `docs/DV_KONZEPT.md`, `.specify/memory/constitution.md`,
  `spec.md` und vorhandene technische Artefakte.
- Beschreibe Architektur, Daten, Verträge, Risiken, Prüfstrategie und Rollout im `plan.md`.
- Begründe Entscheidungen mit Bezug auf bestehende Projektkontexte.

Grenzen:

- Ändere **keinen Anwendungscode**.
- Starte keine Implementierung; bleibe bei umsetzungsnahen, prüfbaren Planentscheidungen.

Abschlussausgabe:

- Gib genau eine statusmarkierte Karte aus.
- Typisch nach `plan`: `▶ Nächste Aktion — Tasks`.
- **Ausführung:** `speckit-tasks` · `gpt-5.3-codex` · Reasoning mittel.
