# Feature 005: Portable Specify-Laufzeit

Neue Projekte erhalten eine Repository-eigene, plattformunabhängige Einrichtung
für GitHub Spec Kit. Windows Smart App Control bleibt unverändert.

## Akzeptanzkriterien

1. `.specify-version` legt die CLI-Version zentral auf 1.0.7 fest.
2. Wiederholtes Setup erhält eine passende Installation; `--repair` repariert sie.
3. PowerShell und POSIX-Wrapper verwenden `uv tool dir` und den Python-Entrypoint,
   niemals den Specify-Launcher. Argumente, Arbeitsverzeichnis und Exit-Code bleiben erhalten.
4. Alle Profile und das API-Rezept erhalten sämtliche Laufzeitdateien. Pfade
   werden relativ zum Skript bestimmt; umbenannte Ordner mit Leerzeichen funktionieren.
5. Codespaces installiert die Laufzeit im vorhandenen Post-Create-Schritt.
6. Agentenregeln, Einstieg und DV-Konzept erklären Nutzung, Diagnose und Updates.
7. Tests prüfen Version, Fehlerfälle, Argumente, Generator und Konfiguration.

## Grenzen

Kein automatisches Initialisieren bestehender Integrationen, kein Push und keine
Änderungen an persönlichen Profilen oder Sicherheitsrichtlinien. Erstinstallation
benötigt Python ab 3.11, pip/venv und Netzwerk. Transitive Paketversionen sind
in universellen Constraints festgehalten. Hash-/Offline-Reproduktion und ein
unveränderliches Basisimage sind nicht Teil dieses Features.
