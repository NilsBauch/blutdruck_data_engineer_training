@echo off
echo ============================================================
echo DOKUMENTATION AKTUALISIEREN
echo ============================================================
echo.

echo [1/2] Diagramme generieren und synchronisieren...
py scripts/refresh_docs.py

echo.
echo [2/2] Doxygen Dokumentation generieren...
doxygen

echo.
echo ============================================================
echo VORGANG ABGESCHLOSSEN
echo Die Dokumentation ist unter 'docs/doxygen_output/html/index.html' verfügbar.
echo ============================================================
pause
