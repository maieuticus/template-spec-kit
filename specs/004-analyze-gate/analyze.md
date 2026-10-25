# Analyse: Analyze-Gate vor Implementierung

**Stand:** 2026-10-25
**Ergebnis:** A001, A002 und A003 sind geklärt. Der Bericht folgt dem
validierten Format; die Gate-Prüfung lässt nur geschlossene wesentliche
Befunde zum manuellen Freigabeschritt durch.

## Wesentliche Befunde

### A001 — P1: Freigabe bei offenen wesentlichen Befunden war widersprüchlich

- **Status:** geklärt
- **Begründung:** Der Nutzer entschied, dass eine Freigabe offene wesentliche
  Befunde nicht übersteuern darf. Spec und Plan schränken Freigabe jetzt auf
  vollständig geklärte oder akzeptierte Befunde ein.
- **Geändertes Artefakt:** `spec.md`, `plan.md`, `tasks.md`

### A002 — P1: Gate ließ offene Befunde trotz `approve` passieren

- **Status:** geklärt
- **Begründung:** Ein vorgeschalteter Prüfer validiert den aktiven Bericht und
  bricht bei offenen oder unvollständig dokumentierten wesentlichen Befunden
  vor dem Gate ab. Die CLI-Smokes belegen offene und fehlende Berichte als
  blockiert sowie einen gültigen Bericht als freigabefähig.
- **Geändertes Artefakt:** `.specify/workflows/project-sdd/workflow.yml`,
  `scripts/check_analyze_gate.py`, `spec.md`, `tests/test_template.py`

### A003 — P2: DV-Anleitungen ließen den Artefaktnachweis bei `geklärt` aus

- **Status:** geklärt
- **Begründung:** Quell-DV-Konzept und Basistemplate verlangen nun bei Status
  `geklärt` einen Artefaktverweis; generierte Projekte und das Analyseprofil
  werden durch Tests gegen diesen Vertrag geprüft.
- **Geändertes Artefakt:** `docs/DV_KONZEPT.md`,
  `templates/base/files/docs/DV_KONZEPT.md.template`,
  `.github/agents/speckit-analyze.agent.md`, `tests/test_template.py`

## Prüfgrenze

- Review-Nacharbeit am 25.10.2026: T013/T014 korrigieren zeilenübergreifend
  gelesene Leerfelder und still übergangene Befundüberschriften. Die neuen
  Parserregressionen bestehen. `python scripts/check.py` erfasst nun 20 Tests:
  19 erfolgreich, ein POSIX-Test zum separaten Post-Create-Fix wird unter
  Windows übersprungen. Die folgenden 17-Test-Nachweise stammen aus dem
  vorherigen Prüfstand.
- Gelesen: README, AGENTS.md, Constitution, DV-Konzept, Spec, Plan, Tasks,
  Workflow, Analyze-/Implement-Agentenprofile, Generator und relevante Tests.
- Spec-Kit CLI: `specify 1.0.7`; `specify workflow info` akzeptiert den
  aktualisierten Workflow.
- CLI-Smokes mit temporärem Projekt und einem Shell-Schritt nach dem Gate:
  - Run `c96b6fe9`: Bericht mit offenem wesentlichem Befund scheiterte in
    `analyze-report-check`; Gate und Folgeschritt wurden nicht erreicht.
  - Run `cb9d907b`: fehlender Bericht scheiterte in `analyze-report-check`;
    Gate und Folgeschritt wurden nicht erreicht.
  - Run `d4f7de80`: `reject` am Gate brach den Lauf ab; der Folgeschritt
    wurde nicht erreicht.
  - Run `c76415dc`: gültiger Bericht erreichte das Gate; `approve` zeigte den
    validierten Bericht an und führte den Folgeschritt aus.
- `python scripts/check.py`: 17 Tests erfolgreich; Dokumentlinks und
  Dateisyntax ebenfalls erfolgreich.
- `python scripts/check.py --static-only`: erfolgreich.
- `specify workflow info .specify/workflows/project-sdd/workflow.yml`:
  Workflow erkannt; `git diff --check`: erfolgreich.
