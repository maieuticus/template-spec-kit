# Allgemeine Copilot-Anweisungen

Lies `AGENTS.md`, `.specify/memory/constitution.md` und
`docs/DV_KONZEPT.md`, bevor du Änderungen planst oder umsetzt.

- Nenne in jeder inhaltlichen Antwort und nach jedem Spec-Kit-Schritt genau
  einen nächsten konkreten Schritt.
- Empfiehl je Schritt ein in der aktiven Copilot-Umgebung auswählbares
  Modellprofil und eine Reasoning-Stufe: für `clarify` und `checklist` ein
  schnelles allgemeines Modell mit niedriger Stufe; für `specify` und `tasks`
  ein Coding-Modell mit mittlerer Stufe; für `plan`, `analyze` und `converge`
  ein reasoning-starkes Coding-Modell mit hoher Stufe; für `implement` ein
  Coding-Modell mit mittlerer Stufe, bei Architektur-, Sicherheits- oder
  Migrationsänderungen mit hoher Stufe. Wenn keine Auswahl verfügbar ist,
  nenne das Plattform-Standardmodell und die empfohlene Stufe.
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
