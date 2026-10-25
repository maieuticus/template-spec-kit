---
name: speckit-clarify
description: Offene fachliche oder architektonische Lücken klären, ohne Anwendungscode zu ändern.
---

Arbeite ausschließlich im SpecKit-Schritt **clarify**.

- Lies mindestens `AGENTS.md`, `docs/DV_KONZEPT.md`, `.specify/memory/constitution.md`,
  die betroffene `spec.md` sowie relevante Plan-/Aufgabenartefakte.
- Führe nur echte Unklarheiten auf, die Umsetzung oder Tests beeinflussen.
- Dokumentiere Entscheidungen und verbleibende Annahmen nachvollziehbar im Feature-Artefakt.

Grenzen:

- Ändere **keinen Anwendungscode**.
- Erfinde keine Produktentscheidungen ohne Auftrag; kennzeichne nötige Entscheidungen als offen.

Abschlussausgabe:

- Gib genau eine statusmarkierte Karte aus.
- Typisch nach `clarify`: `▶ Nächste Aktion — Plan`.
- **Ausführung:** `speckit-plan` · `gpt-6-luna` · Reasoning hoch.
