# DV-Konzept: <Projektname>

> Vorlage. Alle `<...>`-Platzhalter vor der Nutzung ausfüllen. Dieses
> Dokument soll die **einzige** verbindliche Anleitung für Einrichtung,
> Release, Betrieb und Nutzung des Projekts sein — nicht mehrere verstreute
> Guides. Historische/veraltete Dokumente gehören nach `docs/archive/`,
> nicht gelöscht, aber klar als nicht mehr maßgeblich markiert.

## 1. Zweck und Geltungsbereich

<Ein bis zwei Sätze: was macht das System, wer nutzt es, worüber
entscheidet dieses Dokument.>

Technische Referenzen, die bei Änderungen maßgeblich sind:

- API-Vertrag: `<pfad/zur/openapi.yaml>` (falls vorhanden)
- Laufzeitkonfiguration: `<pfad/zu/docker-compose.yml>`
- Konfigurationsvorlage: `<pfad/zu/.env.example>`
- Datenbankschema: `<pfad/zu/db/init.sql>` und `<pfad/zu/db/migrations/>`

## 2. Systemübersicht und Verantwortlichkeiten

```text
<Komponente A> -> <Komponente B> -> <Komponente C> -> <Komponente D>
```

| Komponente | Aufgabe | Maßgebliche Dateien |
| --- | --- | --- |
| <Komponente> | <Aufgabe> | <Pfad(e)> |

<Wo liegen Secrets/Datenbank-Volumes wirklich? Ausdrücklich festhalten, dass
sie nie in Git eingecheckt werden dürfen.>

## 3. <Projekt> vollständig neu einrichten

### Voraussetzungen

- <Voraussetzung 1>
- <Voraussetzung 2>

### Schrittfolge

1. Repository klonen.
2. <Externe Dienste einrichten, z. B. Tunnel, DNS, Cloud-Konto — jeden
   Schritt so konkret beschreiben, dass er ohne Rückfragen ausführbar ist,
   und explizit angeben, ob ein Ergebnis (Token, URL) in `.env` benötigt
   wird.>
3. Lokale Konfiguration anlegen (`cp .env.example .env`) und Werte setzen.
4. Dienste bauen und starten.
5. Funktion lokal prüfen (Healthcheck-Kommando angeben).
6. Bei externen Integrationen (z. B. Custom GPT Action, Webhook): Konfiguration
   dort vornehmen und gegen die echte laufende Instanz testen — **nicht**
   nur dokumentieren, sondern tatsächlich einmal durchspielen, bevor der
   Schritt hier als erledigt gilt.

> **Wichtig:** Jeder hier beschriebene Befehl sollte mindestens einmal gegen
> eine echte laufende Instanz verifiziert worden sein. Eine Lektion aus
> früheren Projekten: eine dokumentierte Named-Tunnel-Einrichtung nützt
> nichts, wenn der tatsächliche Start-Befehl in `docker-compose.yml` einen
> Quick Tunnel erzeugt, der das Token stillschweigend ignoriert.

## 4. Release durchführen

1. Änderungen inklusive Tests vorbereiten (`make ci-test` o. ä.).
2. Vor Datenbankänderungen: Backup an einem Pfad **außerhalb** des
   Git-Arbeitsverzeichnisses erstellen.
3. Geprüften Git-Stand ausrollen.
4. Neue Migrationen anwenden (niemals das Init-Skript erneut gegen
   Produktionsdaten laufen lassen, falls es Tabellen droppt/neu anlegt).
5. Dienste neu bauen/starten, Healthcheck und betroffene Fachfunktion
   prüfen.
6. Bei Vertragsänderungen (API/Schema): externe Konfiguration (z. B. GPT
   Builder Action) aktualisieren und erneut testen.
7. Rollback-Vorgehen bei Fehlern festhalten.

## 5. Betrieb, Backup und Störungen

### Routinebefehle

<Liste der Standardbefehle für Status, Logs, Neustart.>

### Störungsbehebung

| Symptom | Prüfen |
| --- | --- |
| <Symptom> | <Prüfschritt> |

<Backup-Pfad und Wiederherstellungs-Vorsichtsmaßnahmen explizit benennen.>

## 6. <Projekt> benutzen

<Typische Nutzungsszenarien/Anfragen, insbesondere bei einem
Conversational-/GPT-Interface. Klarstellen: lesende Aktionen unkritisch,
schreibende Aktionen brauchen Bestätigung.>

Die aktuellen Operationen, Felder und Antwortformate stehen ausschließlich
in `<Vertragsdatei, z. B. OpenAPI>`. Bei Unklarheiten ist diese Datei
maßgeblich, nicht ein kopierter Endpunkt in einer Anleitung.

## 7. Organisation und Weiterentwicklung

| Änderung | Immer gemeinsam aktualisieren |
| --- | --- |
| API-Endpunkt oder Request/Response | Code, Tests, Vertragsdatei (OpenAPI o. ä.), ggf. externe Konfiguration |
| Datenbankschema | idempotente Migration, Tests, Release-Schritt |
| Umgebungsvariable oder Dienst | `.env.example`, `docker-compose.yml`, dieses Konzept |
| Bedienablauf | Dieses Konzept und ggf. externe Anleitungen (z. B. GPT-Instructions) |

Ältere, abgelöste Dokumente bleiben nur zur Nachvollziehbarkeit unter
`docs/archive/` erhalten. Sie sind keine Betriebsanweisung.
