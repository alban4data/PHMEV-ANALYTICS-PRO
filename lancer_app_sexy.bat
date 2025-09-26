@echo off
echo 🚀 Lancement de l'application PHMEV Analytics Pro (Version SEXY)...
echo.

REM Vérification de l'installation de Streamlit
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installation des dépendances...
    pip install -r requirements.txt
)

echo ✨ Démarrage de l'application Streamlit SEXY...
echo 🌐 L'application s'ouvrira automatiquement dans votre navigateur
echo 📍 URL: http://localhost:8501
echo.
echo ⚠️  Pour arrêter l'application, fermez cette fenêtre ou appuyez sur Ctrl+C
echo.

streamlit run app_phmev_sexy.py

pause

