---
name: speckit-converge
description: Umsetzung gegen Anforderungen, Aufgaben und tatsächliche Prüfnachweise abgleichen und verbleibende Lücken nachvollziehbar festhalten.
---

Arbeite ausschließlich im SpecKit-Schritt **converge**.

- Lies mindestens `AGENTS.md`, `README.md`, `docs/DV_KONZEPT.md`,
  `.specify/memory/constitution.md` sowie `spec.md`, `plan.md`, `tasks.md` und
  `analyze.md` des aktiven Features.
- Gleiche jedes Akzeptanzkriterium mit der Umsetzung und den relevanten Tests
  ab. Prüfe `git status` und den Diff; verlasse dich nicht allein auf frühere
  Zusammenfassungen oder behauptete Prüfergebnisse.
- Führe vorgesehene Prüfungen aus, soweit die Umgebung es ermöglicht, und
  dokumentiere exakt, was erfolgreich, fehlgeschlagen oder nicht ausführbar war.
- Markiere Aufgaben nur dann als erledigt, wenn Umsetzung und Nachweis
  vorliegen. Überführe verbleibende Lücken als konkrete, prüfbare Aufgaben in
  `tasks.md`; halte den Arbeitsstand im DV-Konzept konsistent.
- Implementiere keine Codeänderungen und ändere keine fachlichen Anforderungen.
  Solche Änderungen gehören in einen abgestimmten Implementierungs- oder
  Spezifikationsschritt.
- Erfinde keine Tests, Prüfergebnisse oder Erledigungsnachweise. Lass
  ungeklärte Kriterien und nicht ausgeführte Prüfungen ausdrücklich offen.

Abschlussausgabe:

- Gib genau eine statusmarkierte Karte aus.
- Wenn keine Lücken offen sind, ist der nächste Schritt der Review-Gate; wenn
  Lücken bestehen, benenne den konkreten Implementierungs- oder Prüf-Schritt.
- **Ausführung:** `speckit-converge` · `gpt-6-luna` · Reasoning hoch.
