# Aufgaben

- [x] T001 Bestand, Spezifikation und Architektur abgleichen.
- [x] T002 Zentrale Version, Bootstrap und portable Python-Entrypoint-Wrapper implementieren.
- [x] T003 Generator, Init, Docker/Post-Create und CI integrieren.
- [x] T004 README, DV-Konzept, Projektvorlagen und Agentenregeln angleichen.
- [x] T005 Regressionen und reale Windows-/Linux-Smokes einschließlich neutralem Projekt ausführen.
- [x] T006 Abschlussreview, Prüfstatus und Arbeitsstand aktualisieren.

- [x] T007 Nutzerauftrag zur priorisierten Wiedervorlage dokumentieren:
  Entscheidungsliste im DV-Konzept, Hinweis im README und allgemeine Regeln
  zum Vorrang offener Entscheidungen für Codex und Copilot ergänzen.
- [ ] T008 Die fünf priorisierten Codespace-Entscheidungen mit dem Nutzer einzeln
  abwägen und Antworten im DV-Konzept festhalten. Zuerst ausschließlich
  Entscheidung 1 zum Zugriffsweg behandeln.
- [ ] T009 Den Codespace-Test gemäß den festgehaltenen Entscheidungen durchführen,
  Ergebnisse dokumentieren und ausschließlich vereinbarte Testressourcen bereinigen.

Nachweise und Einschränkungen: [DV-Konzept](../../docs/DV_KONZEPT.md#aktueller-arbeitsstand).

## Prüfgrenzen

PowerShell-Adapter statisch und dessen Transport separat geprüft; direkte
Ausführung hier durch bestehende Execution Policy gesperrt. Gemeinsame Laufzeit
real unter Windows getestet. Windows-CI führt den Adapter-Smoke aus. Codespaces
und Docker nur konfigurationsseitig geprüft, kein tatsächlicher Containerstart.
Details und Ergebnisse stehen im verlinkten DV-Konzept.
