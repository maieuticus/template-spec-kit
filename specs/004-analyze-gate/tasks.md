# Aufgaben

- [x] T001 Workflow-Gate einbauen: In
  `.specify/workflows/project-sdd/workflow.yml` den Schritt `analyze-gate`
  direkt zwischen `analyze` und `implement` ergänzen, mit `options:
  [approve, reject]`, `on_reject: abort` und einer klaren Anweisung zur
  Prüfung von `analyze.md`, dass offene wesentliche Befunde auch bei `approve`
  blockieren.
- [x] T002 Dokumentationsvertrag konsistent machen: In
  `docs/DV_KONZEPT.md` und
  `templates/base/files/docs/DV_KONZEPT.md.template` den manuellen und
  automatisierten Ablauf um dieselben Regeln für „wesentlichen Befund“,
  `analyze.md` und die fail-closed-Freigabegrenze ergänzen.
- [x] T003 Regressionstest ergänzen: In `tests/test_template.py` absichern,
  dass `analyze-gate` im Quell-Workflow und im erzeugten Projekt exakt zwischen
  `analyze` und `implement` steht, `approve/reject` anbietet, bei `reject`
  abbricht und die übrige Folge `implement → checks → converge → review`
  unverändert bleibt.
- [x] T004 Reproduzierbare Gate-Nachweise führen: Mit Spec-Kit CLI 1.0.7 einen
  temporären Workflow-Smoketest mit einem Schritt nach dem Gate ausführen und
  die Ergebnisse für mindestens einen abgelehnten und einen freigegebenen Lauf
  in `specs/004-analyze-gate/analyze.md` dokumentieren.
- [x] T005 Abschlussprüfung und Arbeitsstand pflegen:
  `python scripts/check.py` ausführen, den tatsächlichen Prüfstatus im
  Arbeitsstand des DV-Konzepts aktualisieren und den Feature-Status in
  `specs/README.md` auf den Umsetzungsstand bringen.
- [x] T006 Spezifikation angleichen: unbeschränkte Freigabe in beobachtbarem
  Verhalten und Akzeptanzkriterium 3 ausschließen; fehlenden Bericht und
  Feature-Kontext als blockierend festhalten.
- [x] T007 Fail-closed-Prüfer einbauen: `scripts/check_analyze_gate.py` liest
  den aktiven Featurepfad aus `.specify/feature.json`, validiert
  `analyze.md` und blockiert offene wesentliche oder unvollständig
  dokumentierte Befunde. Den Prüfer in `CORE_FILES` und Workflow einbinden.
- [x] T008 Berichtvertrag angleichen: Analyse-Agent, DV-Konzept und
  Basistemplate auf dasselbe Befundformat bringen; geändertes Artefakt bei
  `geklärt` verlangen und Tests für erzeugte Anleitungen ergänzen.
- [x] T009 Fail-closed-Verhalten regressionssichern: Tests für offenen,
  fehlenden, ungültigen und freigegebenen Bericht ergänzen und die
  Spec-Kit-CLI-Smokes für die drei Pfade dokumentieren.
- [x] T010 Arbeitsstand und Aufgaben nach den Nachweisen aktualisieren;
  `python scripts/check.py` ausführen.
- [x] T011 Wesentlichkeitskriterien im Workflow-Vertrag angleichen: In
  `.github/agents/speckit-analyze.agent.md` und im `analyze`-Schritt von
  `.specify/workflows/project-sdd/workflow.yml` explizit festhalten, dass
  Auswirkungen auf Akzeptanzkriterien, Schnittstellen, Daten, Sicherheit oder
  Betrieb wesentlich sind und redaktionelle Befunde nicht blockieren. Mit
  DV-Konzept und Basistemplate abgleichen; Regressionstests müssen Quell- und
  generierte Workflow-Anweisungen gegen dieselbe Definition prüfen.
- [x] T012 Fehlenden Befundstatus regressionssichern: In
  `tests/test_template.py` einen Bericht ohne `**Status:**` prüfen und
  nachweisen, dass `validate_report` ihn fail-closed mit verständlichem
  Hinweis auf die erforderlichen Statuswerte zurückweist.

Der tatsächliche Stand und die nächsten Schritte stehen im
[DV-Konzept](../../docs/DV_KONZEPT.md#aktueller-arbeitsstand).
