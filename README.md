# template-spec-kit

Wiederverwendbare Vorlagen für Projekte auf Basis von GitHub Spec Kit.

## Inhalt

- [`QUICKSTART.md`](QUICKSTART.md) — Startablauf für ein neues Spec-Kit-Projekt
  mit vorbereiteten Feature-Specs (am Beispiel eines Boardgame-Prototyps).
- [`templates/api-service/`](templates/api-service/README.md) — Vorlagen für
  containerisierte API-Service-Projekte (z. B. FastAPI + PostgreSQL, optional
  hinter einem Cloudflare Tunnel als Custom-GPT-Action). Enthält ein
  DV-Konzept-Dokument-Template, konsistente Makefile-/CI-/Docker-Compose-
  Vorlagen, einen generischen OpenAPI-Contract-Test und einen neuen
  `speckit.audit`-Agenten. Diese Vorlagen fassen konkrete Lehren aus einer
  Projekt-Retrospektive zusammen (siehe dortiges README für Details).

## Verwendung

1. Neues Projekt gemäß `QUICKSTART.md` aufsetzen.
2. Falls es sich um einen API-Service handelt: passende Dateien aus
   `templates/api-service/` in die entsprechenden Zielpfade kopieren
   (siehe `templates/api-service/README.md`).
