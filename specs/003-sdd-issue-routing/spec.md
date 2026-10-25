# Feature 003: Schrittführung, Modellempfehlung und Template-Issue-Routing

## Ziel

Agenten sollen bei allgemeinen Entwicklungs- und Spec-Kit-Aufgaben konsistent
schrittweise führen und wiederverwendbare Verbesserungen dem Template-Repository
zuordnen, ohne fachliche Entscheidungen aus Produktprojekten zu übernehmen.

## Akzeptanzkriterien

1. `AGENTS.md` und die allgemeine Copilot-Anweisung verlangen pro inhaltlicher
   Antwort und Spec-Kit-Schritt genau einen nächsten konkreten Schritt.
2. Beide Anweisungen dokumentieren eine Empfehlung für Modellprofil und
   Reasoning-Stufe für jeden Spec-Kit-Schritt.
3. Das Template-Repository
   `https://github.com/maieuticus/template-spec-kit` und die Regel für
   Template-Issues sind eindeutig dokumentiert.
4. Beide Anweisungen enthalten einen Issue-Vorschlag mit Titel, Nutzen und
   überprüfbaren Akzeptanzkriterien als Beispiel.
5. Fachliche Anforderungen sind ausdrücklich als Produktprojekt-spezifisch
   abgegrenzt.
6. Neu erzeugte Standard- und API-Projekte erhalten die allgemeine
   Copilot-Anweisung; API-Projekte behalten zusätzlich ihren API-Kontext.

## Abgrenzung

Keine automatische Erstellung von Issues und keine Vorgabe eines dauerhaft
festen Modellnamens. Die tatsächliche Modellverfügbarkeit bleibt von der
jeweiligen Agent-Umgebung abhängig.
