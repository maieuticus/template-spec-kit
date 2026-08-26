## Zusammenfassung

<Was ändert dieser PR und warum?>

## Checkliste

- [ ] `make ci-test` (oder Äquivalent) lokal grün
- [ ] Bei API-Änderungen: OpenAPI-Spezifikation aktualisiert und Pfade/Schemas
      gegen den Code geprüft (`test_openapi_contract.py` grün)
- [ ] Bei Schema-Änderungen: idempotente Migration unter `db/migrations/`
      hinzugefügt
- [ ] Bei Infrastruktur-/Compose-Änderungen: Verhalten tatsächlich gegen
      einen laufenden Container verifiziert, nicht nur dokumentiert
- [ ] Betriebsdokumentation (z. B. DV-Konzept) aktualisiert, falls sich
      Setup-, Release- oder Betriebsschritte geändert haben
- [ ] Keine temporären/Debug-Artefakte im Diff (z. B. `.pr_body.txt`,
      Scratch-Dateien, auskommentierter Code)
- [ ] Keine Secrets, echten Zugangsdaten oder `.env`-Dateien im Diff
