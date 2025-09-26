"""
Point d'entrée pour Streamlit Cloud
Lance l'application complète app_phmev_sexy.py avec l'échantillon de 10k lignes
"""

import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="📊 PHMEV Analytics Pro",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import et lancement de l'application principale
try:
    from app_phmev_sexy import main
    
    # Lancer l'application complète
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    st.error(f"❌ Impossible d'importer l'application principale: {e}")
    st.info("🔧 Vérifiez que le fichier app_phmev_sexy.py est présent")
except Exception as e:
    st.error(f"❌ Erreur lors du lancement: {e}")
    st.info("🔄 Essayez de redémarrer l'application")