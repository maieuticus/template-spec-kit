# Allgemeine Copilot-Anweisungen

Lies `AGENTS.md`, `.specify/memory/constitution.md` und
`docs/DV_KONZEPT.md`, bevor du Änderungen planst oder umsetzt.

- Prüfe bei Sitzungsbeginn und vor der Weiterarbeit den aktuellen Arbeitsstand
  im DV-Konzept auf vom Nutzer priorisierte offene Entscheidungen. Bringe dann
  zuerst die erste offene Entscheidung vor und besprich Nutzen, Risiken,
  Maßnahmen und Empfehlung einzeln. Dokumentiere die Antwort, bevor du den
  nächsten Punkt bestimmst. Empfehlungen oder frühere allgemeine
  Fortsetzungsaufträge sind keine Entscheidung; abhängige Aktionen warten
  auf die jeweilige Nutzerentscheidung.
- Nenne in jeder inhaltlichen Antwort und nach jedem Spec-Kit-Schritt genau
  einen nächsten konkreten Schritt.
- Stelle den nächsten Schritt als genau eine kompakte, statusmarkierte Karte
  dar. Wähle `▶ Nächste Aktion`, wenn die Arbeit ohne Rückfrage fortgesetzt
  werden kann; `⏸ Entscheidung benötigt`, wenn eine konkrete Nutzerentscheidung
  erforderlich ist; oder `⛔ Blockiert`, wenn ein Hindernis die Arbeit stoppt.
  Frage nicht nach Bestätigung für sichere, reversible und vom Auftrag gedeckte
  Arbeit. Stelle bei einer Entscheidung nur die notwendige Frage.
- Die Karte `▶ Nächste Aktion — <Schritt>` enthält **Aktion**, **Fertig, wenn**
  und **Ausführung**. `⏸ Entscheidung benötigt — <Thema>` enthält
  **Entscheidung**, **Warum jetzt** und **Danach**. `⛔ Blockiert — <Thema>`
  enthält **Blocker**, **Aufhebung** und **Danach**. `Danach` erscheint nur bei
  Entscheidungen oder Blockaden. Formuliere Aktion und Abschlusskriterium
  konkret; nenne unter Ausführung die konkrete Agentenrolle bzw. das Profil,
  den exakten Modellnamen und die Reasoning-Stufe, kompakt in einer Zeile.
- Empfiehl je Schritt das konkrete, in der aktiven Copilot-Umgebung
  auswählbare Modell samt Reasoning-Stufe; allgemeine Kategorien wie
  „Coding-Modell“ allein reichen nicht. Verwende, sofern auswählbar,
  `claude-haiku-5.5` mit niedriger Stufe für `clarify` und `checklist`,
  `gpt-5.3-codex` mit mittlerer Stufe für `specify`, `tasks` und `implement`
  sowie `gpt-6-luna` mit hoher Stufe für `plan`, `analyze` und `converge`.
  Für Architektur-, Sicherheits- oder Migrationsänderungen bei `implement`
  verwende `gpt-6-luna` mit hoher Stufe. Ist ein empfohlenes Modell nicht
  auswählbar, nenne stattdessen den exakten Namen des verfügbaren
  Plattform-Standardmodells und die empfohlene Stufe; „Standardmodell“ ohne
  Modellnamen genügt nicht.
- Beispiel:
  **▶ Nächste Aktion — Specify**
  **Aktion:** Anforderungen und Akzeptanzkriterien für Feature 004 festlegen.
  **Fertig, wenn:** `specs/004-.../spec.md` prüfbar vorliegt.
  **Ausführung:** `speckit-specify` · `gpt-5.3-codex` · Reasoning mittel.
- Fachliche Entscheidungen bleiben im Projekt, seinem DV-Konzept und den
  Feature-Artefakten. Nur wiederverwendbare Prozess-, Tooling- und
  Template-Erkenntnisse sind Verbesserungskandidaten.
- Formuliere für einen solchen Kandidaten einen Issue-Vorschlag mit Titel,
  Nutzen und überprüfbaren Akzeptanzkriterien. Das kanonische
  Template-Repository ist https://github.com/maieuticus/template-spec-kit;
  Template-Verbesserungen werden dort als Issues angelegt, nicht im
  Produktprojekt. Erstelle ein Issue nur auf ausdrücklichen Auftrag.
- Beispiel: „Die gemeinsame Prüfung sollte fehlende Projektdateien klar
  benennen“ wird zum Vorschlag „Prüfung: Fehlende Projektdateien eindeutig
  melden“ mit dem Nutzen „schnellere Fehlerdiagnose“ und Kriterien für
  fehlende, vorhandene und unlesbare Dateien.

## Portable Specify-Schnittstelle

- Specify ausschließlich über den Repository-Wrapper ausführen: Windows
  `.\scripts\specify.ps1 <Argumente>`, Linux/Codespaces
  `./scripts/specify <Argumente>`. Unter Windows niemals `specify.exe` verwenden.
- Vor der ersten lokalen Nutzung `python scripts/bootstrap_specify.py` ausführen;
  im Devcontainer erfolgt dies automatisch. Die Version steht in `.specify-version`.
- Wrapper und Setup sind die unterstützte portable Schnittstelle. Keine persönlichen
  Profile, PATH-Anpassungen oder Änderungen an Windows-Sicherheitsrichtlinien nötig.
