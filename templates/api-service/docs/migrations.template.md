# Datenbankmigrationen: <Projektname>

Dieses Dokument ergänzt das DV-Konzept. Es beschreibt ausschließlich die
Regeln für Schemaänderungen; Setup, Release und Backups bleiben im
verbindlichen Betriebsdokument.

## Regeln

1. Jede Änderung an einem bestehenden Datenbankschema erhält eine neue,
   lexikalisch sortierbare Datei unter `db/migrations/`, zum Beispiel
   `0001_add_widget_status.sql`.
2. Migrationen müssen idempotent sein. Sie dürfen nach einem fehlgeschlagenen
   oder wiederholten Rollout nicht scheitern oder Daten unerwartet verändern.
   Verwende dazu, wo passend, `IF EXISTS`, `IF NOT EXISTS` und eindeutig
   begrenzte Datenkorrekturen.
3. `db/init.sql` dient ausschließlich zum Erstellen einer frischen,
   wegwerfbaren Datenbank. Es darf niemals als Teil eines Produktions-Releases
   ausgeführt werden, wenn es Tabellen oder Daten neu erstellt.
4. Vor einer produktiven Migration wird ein geprüftes Backup außerhalb des
   Git-Arbeitsverzeichnisses erstellt. Die Migration wird anschließend gegen
   die laufende Datenbank ausgeführt und zusammen mit der betroffenen
   Anwendungsfunktion geprüft.
5. Zu jeder Schemaänderung gehören mindestens die Migration, passende Tests,
   die Aktualisierung des Datenmodells/API-Vertrags und ein Release-Hinweis im
   DV-Konzept.

## Ausführen

Kopiere `scripts/run_migrations.sh.template` nach
`scripts/run_migrations.sh`, mache die Datei ausführbar und setze die
Verbindungsvariablen. Das Skript führt standardmäßig **nur** Dateien unter
`db/migrations/` aus:

```bash
POSTGRES_HOST=localhost POSTGRES_PORT=5432 \
POSTGRES_USER=<user> POSTGRES_DB=<database> \
PGPASSWORD=<password> scripts/run_migrations.sh
```

Für eine lokal neu angelegte Testdatenbank darf das Init-Skript explizit
zugeschaltet werden:

```bash
RUN_INIT_FOR_TESTS=1 PGPASSWORD=<test-password> scripts/run_migrations.sh
```

`RUN_INIT_FOR_TESTS=1` ist absichtlich opt-in und darf in Produktions- oder
Release-Befehlen nicht gesetzt werden.
