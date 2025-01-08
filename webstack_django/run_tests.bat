@echo off
echo === Démarrage des tests système ===
python test_system.py
if errorlevel 1 (
    echo Erreur lors des tests
    exit /b 1
)
echo === Tests terminés avec succès ===
