# Ergänzende Prinzipien für API-Service-Projekte

An `.specify/memory/constitution.md` des Zielprojekts anhängen (Abschnitt
„Principles" o. ä.). Entstanden aus einer Retrospektive, in der genau diese
zwei fehlenden Prinzipien zu unbemerkter Vertrags-Drift und wochenlang
kaputter CI geführt hatten.

## Single Source of Truth Documentation

Es gibt genau ein verbindliches Betriebsdokument (z. B. `docs/DV_KONZEPT.md`),
das Einrichtung, Release, Betrieb und Nutzung beschreibt. Neue
Setup-/Betriebsanleitungen werden in dieses Dokument integriert, nicht als
zusätzliche, parallele Guides angelegt. Abgelöste Dokumente werden nach
`docs/archive/` verschoben und dort explizit als historisch/nicht mehr
maßgeblich markiert — nicht kommentarlos gelöscht und nicht unmarkiert
liegen gelassen.

**Begründung:** Mehrere parallele, mit der Zeit auseinanderdriftende
Anleitungen (z. B. drei widersprüchliche Deployment-Guides) sind schwerer zu
warten als eine einzige Datei und führen dazu, dass Nutzer der falschen,
veralteten Anleitung folgen.

## Contract-Code Parity wird automatisiert getestet

Wenn ein API-Vertrag (OpenAPI o. ä.) existiert, muss ein automatisierter
Test sicherstellen, dass jede im Code registrierte Route im Vertrag
dokumentiert ist und umgekehrt — nicht nur, dass die Vertragsdatei
syntaktisch gültig ist. Ebenso müssen `$ref`-Verweise auf tatsächlich
existierende Schemas/Responses geprüft werden.

**Begründung:** Ein Projekt hatte über längere Zeit eine OpenAPI-Spezifikation
im Einsatz, deren `/daily-plans/*`-Endpunkte komplett von den echten Routen
abwichen. Der einzige vorhandene Test prüfte nur, ob die YAML-Datei
syntaktisch gültig ist — die Abweichung fiel erst bei einem manuellen Audit
auf. Ein Test wie in `templates/api-service/tests/test_openapi_contract.py.template`
hätte das beim ersten abweichenden Commit automatisch gemeldet.

## API-Änderungen werden vor der Umsetzung vollständig geplant

Jedes Feature, das API-Routen, öffentliche Schemas, Datenhaltung,
Authentifizierung oder Infrastruktur verändert, muss vor `/tasks` einen
konkreten Plan für Vertragskompatibilität, Datenmigration, Testfälle, Release,
Rollback sowie externe Verbraucher enthalten. Das zugehörige
`docs/api-feature-planning.md` dient dabei als Checkliste. `db/init.sql` darf
nicht als Produktionsmigrationsweg geplant werden.

**Begründung:** Bei API-Services reichen reine Code-Aufgaben nicht aus: Eine
Änderung kann gleichzeitig den OpenAPI-Vertrag, gespeicherte Daten, Clients
und den Betrieb betreffen. Ein verbindlicher Plan macht diese Abhängigkeiten
vor der Implementierung sichtbar und hält den Feature-Schnitt überprüfbar.
