# API-Service-Templates

Diese Vorlagen entstanden aus einer Retrospektive der `p0003-alfred-api`
(NAS-basierter FastAPI/PostgreSQL/Custom-GPT-Service). Sie fassen zusammen,
welche Fehler und Ineffizienzen dort auftraten, und bieten wiederverwendbare
Bausteine, damit neue Projekte mit ähnlicher Architektur
(Custom GPT → OpenAPI Action → Cloudflare Tunnel → FastAPI → PostgreSQL,
oder allgemein: containerisierter API-Service mit Datenbank) diese Fehler
nicht wiederholen.

## Gelernte Lektionen

| Problem | Ursache | Gegenmaßnahme in diesen Templates |
| --- | --- | --- |
| OpenAPI-Spezifikation driftete unbemerkt von den echten Routen ab | Es gab nur einen YAML-Syntaxtest, keinen Vertragstest | `tests/test_openapi_contract.py.template` |
| Tests, Makefile und CI nutzten unterschiedliche Datenbank-Zugangsdaten | Zugangsdaten waren an drei Stellen hart codiert statt an einer Stelle gepflegt | `.env.test.example` als einzige Quelle, referenziert von `Makefile.template` und `ci.template.yml` |
| CI schlug wochenlang fehl, ohne dass es auffiel | Falsches Quoting bei `--health-cmd` im Docker-Healthcheck; ein kaputter CI-Lauf maskierte weitere Bugs | Korrektes Quoting bereits in `ci.template.yml` vorgegeben |
| Doku-Wildwuchs: mehrere widersprüchliche Deployment-Guides, tote Links | Kein Single-Source-of-Truth-Dokument von Projektbeginn an | `docs/DV_KONZEPT.template.md` |
| Infrastruktur-Doku widersprach dem echten Verhalten (Quick Tunnel statt Named Tunnel) | Niemand hatte die Doku gegen den echten Containerstart verifiziert | Kommentierter Cloudflared-Snippet mit Warnung, siehe unten |
| Stale Artefakte (`.pr_body.txt` u. ä.) sammelten sich an | Keine Aufräum-Routine bei PRs | `.github/PULL_REQUEST_TEMPLATE.md` mit Checkliste |
| Kleine Syntaxfehler (z. B. Docker-Flag-Reihenfolge) blieben lange unbemerkt | `make ci-test` wurde nicht regelmäßig lokal ausgeführt | Empfehlung in diesem README + Makefile-Template mit korrekter Flag-Reihenfolge |

## Enthaltene Dateien

- `docs/DV_KONZEPT.template.md` — Vorlage für ein einziges, verbindliches
  Betriebsdokument (Setup, Release, Betrieb, Nutzung, Organisation). In neues
  Projekt kopieren nach `docs/DV_KONZEPT.md` und Platzhalter (`<...>`)
  ausfüllen. Ersetzt mehrere verstreute Guides.
- `tests/test_openapi_contract.py.template` — generischer Pytest, der die
  tatsächlichen FastAPI-Routen gegen die OpenAPI-Pfade abgleicht und auf
  dangling `$ref`/ungenutzte Schemas prüft. Nach Anpassung der Importpfade in
  `tests/` einfügen und in die reguläre Testsuite aufnehmen.
- `.env.test.example` — einzige Quelle für Test-Datenbank-Zugangsdaten.
  Nach `.env.test.example` im neuen Projekt kopieren; `Makefile` und
  CI-Workflow lesen daraus (siehe Kommentare in den jeweiligen Dateien).
- `Makefile.template` — `start-db`/`wait-db`/`migrate`/`test`/`ci-test`
  mit korrekter Docker-Flag-Reihenfolge und Zugangsdaten aus
  `.env.test.example`.
- `.github/workflows/ci.template.yml` — GitHub-Actions-Workflow mit korrekt
  gequotetem `--health-cmd` und denselben Zugangsdaten wie das Makefile.
- `docker-compose.cloudflared-snippet.yml` — korrekter Cloudflared-Service
  mit `tunnel run` (Named Tunnel, nutzt `TUNNEL_TOKEN`). Enthält einen
  Kommentar, der explizit vor `tunnel --url ...` (Quick Tunnel, ignoriert
  das Token) warnt.
- `.gitignore.snippet` — zusätzliche Muster (Editor-Swap-Dateien u. a.), die
  an die projektspezifische `.gitignore` angehängt werden sollten.
- `.github/PULL_REQUEST_TEMPLATE.md` — Checkliste inkl. „temporäre
  Artefakte entfernt?" und „OpenAPI/Doku aktualisiert?".
- `.github/agents/speckit.audit.agent.md` + `.github/prompts/speckit.audit.prompt.md` —
  neuer Speckit-Agent, der die oben genannten Konsistenzprüfungen
  automatisiert ausführt (Routen-Diff, `$ref`-Scan, tote Doku-Links,
  Stale-File-Scan, Credential-Abgleich). Nach `specify init` in
  `.github/agents/` bzw. `.github/prompts/` des Zielprojekts kopieren.
- `constitution/api-service-principles.md` — zwei Prinzipien
  („Single Source of Truth Documentation", „Contract-Code Parity wird
  automatisiert getestet") zum Anhängen an
  `.specify/memory/constitution.md` des Zielprojekts.

## Verwendung in einem neuen Projekt

1. Projekt wie gewohnt mit `specify init` aufsetzen (siehe `QUICKSTART.md`).
2. Aus diesem Ordner die passenden Dateien in die entsprechenden Zielpfade
   kopieren (siehe Tabelle oben) und Platzhalter ausfüllen.
3. `speckit.audit` in `.github/agents/` und `.github/prompts/` einhängen und
   bei jedem größeren Merge oder vor jedem Release aufrufen.
4. Die zwei Prinzipien aus `constitution/api-service-principles.md` an die
   Projekt-Constitution anhängen, damit sie dauerhaft gelten und nicht nur
   einmalig befolgt werden.
