#!/usr/bin/env python3
"""
🚀 Script de lancement pour l'application PHMEV Analytics Pro
"""

import subprocess
import sys
import os

def main():
    print("🚀 Lancement de l'application PHMEV Analytics Pro...")
    print("✨ Interface ultra moderne avec thème sombre")
    print("📊 Analyse des données pharmaceutiques PHMEV")
    print()
    
    # Vérifier que nous sommes dans le bon répertoire
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Vérifier que le fichier de données existe
    if not os.path.exists('OPEN_PHMEV_2024.CSV'):
        print("❌ Erreur: Fichier de données OPEN_PHMEV_2024.CSV introuvable")
        print("📁 Assurez-vous que le fichier est dans le même répertoire que l'application")
        return
    
    # Vérifier l'installation de Streamlit
    try:
        import streamlit
        print(f"✅ Streamlit installé (version {streamlit.__version__})")
    except ImportError:
        print("📦 Installation de Streamlit...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    
    # Lancer l'application
    print("🌐 Lancement de l'application...")
    print("📍 L'application sera accessible sur: http://localhost:8501")
    print("⚠️  Pour arrêter l'application, appuyez sur Ctrl+C")
    print()
    
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app_phmev_sexy.py',
            '--server.headless', 'false',
            '--server.address', 'localhost',
            '--server.port', '8501'
        ])
    except KeyboardInterrupt:
        print("\n🛑 Application arrêtée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

if __name__ == "__main__":
    main()

