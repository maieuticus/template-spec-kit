# Feature 004: Analyze-Gate vor Implementierung

## Ziel

Der automatisierte Spec-Kit-Workflow soll vor `implement` explizit anhalten,
wenn aus `analyze` wesentliche offene Befunde vorliegen. Dadurch startet keine
Umsetzung, solange die Befunde nicht nachvollziehbar geklärt oder ausdrücklich
als akzeptiert dokumentiert sind.

## Beobachtbares Verhalten

1. Der Workflow zeigt nach `analyze` einen klaren Prüf-/Entscheidungspunkt.
2. Offene wesentliche Befunde blockieren den direkten Übergang zu `implement`.
3. Erst nach erfolgreicher Prüfung, dass keine wesentlichen Befunde offen sind,
   und ausdrücklicher Freigabe läuft der Workflow mit `implement` weiter.
4. Bei blockiertem Zustand wird die notwendige Folgeaktion konkret benannt.

## Akzeptanzkriterien

1. Für den Workflow-Schritt zwischen `analyze` und `implement` ist ein
   prüfbarer Gate-Mechanismus definiert, der standardmäßig auf „nicht freigegeben“
   steht, solange offene wesentliche Befunde existieren.
2. Ein Lauf mit offenen wesentlichen Befunden endet vor `implement` mit einer
   verständlichen Begründung und einem eindeutigen Hinweis auf die erforderliche
   Klärung.
3. Ein Lauf mit dokumentiert geklärten oder akzeptierten wesentlichen Befunden
   und ausdrücklicher Freigabe durchläuft `implement`, `checks` und `converge`
   unverändert. Ohne wesentliche Befunde muss dies im Bericht ausdrücklich
   vermerkt sein.
4. Die Kriterien für „wesentlicher Befund“ und „dokumentiert geklärt“ sind in
   den Workflow-Artefakten und im DV-Konzept konsistent beschrieben.
5. Der Nachweis umfasst mindestens einen blockierten und einen freigegebenen
   Ablauf; beide Ergebnisse sind reproduzierbar dokumentiert.
6. Ein fehlender Analysebericht, fehlender Feature-Kontext oder ein fehlender
    beziehungsweise unbekannter Befundstatus blockiert vor dem Gate und vor
    `implement`.

## Ausgeschlossener Umfang

- Keine Änderung fachlicher Akzeptanzkriterien einzelner Produktfeatures.
- Keine Ausweitung des Gates auf andere Workflow-Übergänge außerhalb
  `analyze -> implement`.
- Keine automatische Inhaltserzeugung für die Befundklärung; die Klärung bleibt
  eine explizite Projektentscheidung.

## Klärungen

- **Freigabe:** Der Workflow erhält einen Gate-Schritt `analyze-gate` zwischen
  `analyze` und `implement`, dessen Optionen `approve` und `reject` lauten.
  Ohne ausdrückliche Freigabe (`approve`) wird `implement` nicht gestartet.
  Der Standard ist `reject`. Eine Freigabe ist nur zulässig, wenn keine offenen
  wesentlichen Befunde bestehen; `approve` übersteuert offene wesentliche
  Befunde nicht.
- **Befundklärung:** Die Klärung wird in `specs/<nummer>-<name>/analyze.md`
  festgehalten. Jeder wesentliche Befund steht dort mit Status `offen`,
  `geklärt` oder `akzeptiert`, Begründung und, bei `geklärt`, dem geänderten
  Artefakt (`spec.md`, `plan.md` oder `tasks.md`).
- **Berichtsformat:** Der Bericht enthält den Abschnitt `## Wesentliche
  Befunde`. Ein leerer Befundbestand wird exakt mit `Keine wesentlichen
  Befunde.` markiert. Jeder Befund enthält genau einen Status und eine
  Begründung; bei `geklärt` ist zusätzlich das geänderte Artefakt erforderlich.
- **Wesentlich:** Ein Befund ist wesentlich, wenn er Akzeptanzkriterien,
  Schnittstellen, Daten, Sicherheit oder Betrieb betrifft. Rein redaktionelle
  Befunde blockieren den Gate nicht.
- **Dokumentiert geklärt:** Ein Befund gilt als geklärt, wenn sein Status in
  `analyze.md` `geklärt` oder `akzeptiert` ist und die Begründung ausgefüllt
  ist. Fehlt das, bleibt der Gate geschlossen.

## Planentscheidungen

- Der Workflow verwendet den vorhandenen Gate-Typ mit `approve`/`reject` und
  `on_reject: abort`; eine nicht belegte Default-Syntax wird nicht ergänzt.
- Vor dem Gate prüft `scripts/check_analyze_gate.py` den aktiven Featurepfad
  aus `.specify/feature.json` und dessen `analyze.md`. Fehlende oder
  widersprüchliche Angaben sowie offene wesentliche Befunde brechen den
  Workflow ab. Der Gate bleibt danach eine bewusste manuelle Freigabe.
- `approve` ist nur nach erfolgreicher Berichtsprüfung möglich; ein offener
  wesentlicher Befund kann nicht durch die Auswahl übersteuert werden.
- Die Semantik wird mit Spec-Kit CLI 1.0.7 anhand eines reproduzierbaren
  offenen, fehlenden und freigegebenen Bericht geprüft. Details stehen im
  [Plan](plan.md).
