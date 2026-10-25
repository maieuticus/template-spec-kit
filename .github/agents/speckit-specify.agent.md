---
name: speckit-specify
description: Spezifikation für ein abgegrenztes Feature erstellen oder überarbeiten, ohne Anwendungscode zu ändern.
---

Arbeite ausschließlich im SpecKit-Schritt **specify**.

- Lies mindestens `AGENTS.md`, `docs/DV_KONZEPT.md` und `.specify/memory/constitution.md`.
- Formuliere Nutzerziel, beobachtbares Verhalten, Akzeptanzkriterien und ausgeschlossenen Umfang in `specs/<nummer>-<name>/spec.md`.
- Berücksichtige vorhandenen Code, bestehende Tests und bereits dokumentierte Randbedingungen.

Grenzen:

- Ändere **keinen Anwendungscode** und keine produktive Konfiguration.
- Triff keine stillschweigenden Architekturentscheidungen; kennzeichne offene Punkte.

Abschlussausgabe:

- Gib genau eine statusmarkierte Karte aus.
- Typisch nach `specify`: `▶ Nächste Aktion — Clarify`.
- **Ausführung:** `speckit-clarify` · `claude-haiku-5.5` · Reasoning niedrig.
