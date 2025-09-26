"""
🚀 Application Streamlit SEXY pour l'analyse des données PHMEV
💊 Analyse avancée des délivrances pharmaceutiques par établissement
✨ Design moderne et interface intuitive
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page avec thème sombre
st.set_page_config(
    page_title="🚀 PHMEV Analytics Pro",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS ultra moderne et sexy
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Variables CSS */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #f093fb;
        --success-color: #4facfe;
        --warning-color: #f6d55c;
        --danger-color: #ff6b6b;
        --dark-bg: #0e1117;
        --card-bg: #1e2130;
        --text-light: #fafafa;
        --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --shadow: 0 10px 30px rgba(0,0,0,0.3);
        --border-radius: 15px;
    }
    
    /* Global Styles */
    .stApp {
        font-family: 'Poppins', sans-serif;
        background: var(--dark-bg) !important;
        color: var(--text-light);
    }
    
    /* Force dark background on main content area */
    .main .block-container {
        background: var(--dark-bg) !important;
        color: var(--text-light);
    }
    
    /* Ensure all Streamlit containers have dark background */
    .stApp > div {
        background: var(--dark-bg) !important;
    }
    
    /* Main content area */
    section.main > div {
        background: var(--dark-bg) !important;
        color: var(--text-light);
    }
    
    /* Header Styles */
    .main-header {
        background: var(--gradient-1);
        padding: 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
        animation: fadeInDown 0.8s ease-out;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Card Styles */
    .metric-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: var(--shadow);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-1);
    }
    
    /* Info Cards */
    .info-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        padding: 1.5rem;
        border-radius: var(--border-radius);
        border-left: 4px solid var(--primary-color);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.6s ease-out;
    }
    
    .warning-card {
        background: linear-gradient(135deg, rgba(246, 213, 92, 0.1), rgba(255, 107, 107, 0.1));
        padding: 1.5rem;
        border-radius: var(--border-radius);
        border-left: 4px solid var(--warning-color);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar Styles */
    .css-1d391kg, .css-1lcbmhc {
        background: var(--card-bg) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Force dark background on all content containers */
    [data-testid="stAppViewContainer"] {
        background: var(--dark-bg) !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    [data-testid="stToolbar"] {
        background: transparent !important;
    }
    
    /* Main content area - more specific selectors */
    .main .block-container, 
    [data-testid="stMainBlockContainer"] {
        background: var(--dark-bg) !important;
        color: var(--text-light);
        padding-top: 1rem;
    }
    
    /* Metrics and containers */
    [data-testid="metric-container"] {
        background: var(--card-bg) !important;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: var(--border-radius);
        padding: 1rem;
    }
    
    /* Button Styles */
    .stButton > button {
        background: var(--gradient-1);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }
    
    /* Download Button Styles */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3) !important;
        min-height: 2.5rem !important;
        width: auto !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.4) !important;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
    }
    
    .stDownloadButton > button:active {
        transform: translateY(0px) !important;
    }
    
    /* Download Button */
    .download-btn {
        background: var(--gradient-3);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 1rem 2rem;
        font-weight: 600;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
        margin: 0.5rem;
    }
    
    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Loading Animation */
    .loading-spinner {
        animation: pulse 1.5s infinite;
    }
    
    /* Table Styles */
    .dataframe {
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--shadow);
    }
    
    /* Progress Bar */
    .progress-bar {
        background: var(--gradient-1);
        height: 4px;
        border-radius: 2px;
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Emoji Animations */
    .emoji-bounce {
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    /* Glassmorphism Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Gradient Text */
    .gradient-text {
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    }
    
    /* Status Indicators */
    .status-success {
        color: var(--success-color);
        font-weight: 600;
    }
    
    .status-warning {
        color: var(--warning-color);
        font-weight: 600;
    }
    
    /* Hover Effects */
    .hover-glow:hover {
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
        transition: box-shadow 0.3s ease;
    }
    
    /* KPI Cards Ultra Sexy */
    .kpi-container {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.9);
        border: 1px solid rgba(102, 126, 234, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #4facfe);
        border-radius: 20px 20px 0 0;
    }
    
    .kpi-card {
        background: linear-gradient(145deg, #ffffff 0%, #f0f2ff 100%);
        border-radius: 16px;
        padding: 1.8rem;
        margin: 0.5rem;
        box-shadow: 
            0 8px 32px rgba(102, 126, 234, 0.15),
            inset 0 1px 0 rgba(255,255,255,0.9);
        border: 1px solid rgba(102, 126, 234, 0.08);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--gradient-1));
        border-radius: 0 2px 2px 0;
    }
    
    .kpi-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 20px 60px rgba(102, 126, 234, 0.25),
            inset 0 1px 0 rgba(255,255,255,0.9);
        border-color: rgba(102, 126, 234, 0.2);
    }
    
    .kpi-icon {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
        display: block;
        text-align: center;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
        animation: kpi-pulse 2s ease-in-out infinite;
    }
    
    @keyframes kpi-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2d3748;
        margin: 0.5rem 0;
        text-align: center;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        letter-spacing: -0.5px;
    }
    
    .kpi-label {
        font-size: 0.95rem;
        font-weight: 600;
        color: #4a5568;
        text-align: center;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.8;
    }
    
    .kpi-delta {
        font-size: 0.85rem;
        font-weight: 500;
        text-align: center;
        margin-top: 0.5rem;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        background: rgba(79, 172, 254, 0.1);
        color: #4facfe;
        border: 1px solid rgba(79, 172, 254, 0.2);
    }
    
    .kpi-section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2d3748;
        text-align: center;
        margin: 0 0 1.5rem 0;
        position: relative;
        padding-bottom: 0.8rem;
    }
    
    .kpi-section-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
    }
    
    /* Animations spéciales pour les KPIs */
    .kpi-card:nth-child(1) { animation-delay: 0.1s; }
    .kpi-card:nth-child(2) { animation-delay: 0.2s; }
    .kpi-card:nth-child(3) { animation-delay: 0.3s; }
    .kpi-card:nth-child(4) { animation-delay: 0.4s; }
    
    @keyframes kpi-slideIn {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .kpi-card {
        animation: kpi-slideIn 0.8s ease-out forwards;
    }
    
    /* Gradient backgrounds pour différents KPIs */
    .kpi-card.boxes::before { background: linear-gradient(180deg, #667eea, #764ba2); }
    .kpi-card.money::before { background: linear-gradient(180deg, #f093fb, #f5576c); }
    .kpi-card.base::before { background: linear-gradient(180deg, #4facfe, #00f2fe); }
    .kpi-card.count::before { background: linear-gradient(180deg, #f6d55c, #ff9a56); }
</style>
""", unsafe_allow_html=True)

# Cache intelligent avec session_state pour éviter les rechargements
def load_data_background(nrows=None):
    """🚀 Charge les données PHMEV en arrière-plan (cache désactivé pour éviter les erreurs mémoire)"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Priorité 1: Parquet (plus rapide)
    parquet_path = os.path.join(script_dir, 'OPEN_PHMEV_2024.parquet')
    csv_path = os.path.join(script_dir, 'OPEN_PHMEV_2024.CSV')
    
    # Essayer d'abord le format Parquet
    if os.path.exists(parquet_path):
        st.info("🚀 Chargement ultra-rapide depuis le fichier Parquet optimisé")
        try:
            df = pd.read_parquet(parquet_path)
            
            # Vérifier si les colonnes dérivées existent déjà
            if 'etablissement' not in df.columns:
                st.info("🔧 Création des colonnes enrichies...")
                # Création de colonnes enrichies avec gestion sécurisée des NaN
                df['etablissement'] = df['nom_etb'].astype(str).fillna('Non spécifié')
                if 'raison_sociale_etb' in df.columns:
                    df['etablissement'] = df['etablissement'].where(
                        df['etablissement'] != 'nan', 
                        df['raison_sociale_etb'].astype(str)
                    )
                
                df['medicament'] = df['L_ATC5'].astype(str).fillna('Non spécifié')
                df['categorie'] = df['categorie_jur'].astype(str).fillna('Non spécifiée')
                df['ville'] = df['nom_ville'].astype(str).fillna('Non spécifiée')
                df['region'] = df['region_etb'].fillna(0)
                df['code_cip'] = df['CIP13'].astype(str)
                df['libelle_cip'] = df['l_cip13'].fillna('Non spécifié')
                
                # Calculs dérivés
                df['cout_par_boite'] = np.where(df['BOITES'] > 0, df['REM'] / df['BOITES'], 0)
                df['taux_remboursement'] = np.where(df['REM'] > 0, (df['BSE'] / df['REM']) * 100, 0)
            
            return df
        except Exception as e:
            st.warning(f"⚠️ Erreur avec le fichier Parquet: {e}. Essai avec le CSV...")
    
    # Fallback sur CSV
    if os.path.exists(csv_path):
        st.info("📁 Chargement depuis le fichier CSV")
    else:
        # Si aucun fichier n'existe, utiliser les données d'exemple
        try:
            from sample_data import create_sample_data
            st.warning("⚠️ Fichier PHMEV principal non trouvé. Utilisation de données d'exemple pour la démonstration.")
            return create_sample_data()
        except ImportError:
            st.error("❌ Impossible de charger les données d'exemple. Veuillez ajouter le fichier OPEN_PHMEV_2024.parquet ou .CSV")
            return None
    
    # Types de données optimisés pour économiser la mémoire
    dtype_dict = {
        'CIP13': 'str', 
        'l_cip13': 'str',
        'BOITES': 'int32',
        'region_etb': 'int16',
        'nom_etb': 'string',
        'raison_sociale_etb': 'string'
    }
    
    try:
        df = pd.read_csv(
            csv_path, 
            nrows=nrows, 
            encoding='latin1', 
            sep=';',
            low_memory=True,
            dtype=dtype_dict,
            engine='c'
        )
        
        # Création de colonnes enrichies avec gestion sécurisée des NaN
        df['etablissement'] = df['nom_etb'].astype(str).fillna('Non spécifié')
        if 'raison_sociale_etb' in df.columns:
            df['etablissement'] = df['etablissement'].where(
                df['etablissement'] != 'nan', 
                df['raison_sociale_etb'].astype(str)
            )
        
        df['medicament'] = df['L_ATC5'].astype(str).fillna('Non spécifié')
        df['categorie'] = df['categorie_jur'].astype(str).fillna('Non spécifiée')
        df['ville'] = df['nom_ville'].astype(str).fillna('Non spécifiée')
        df['region'] = df['region_etb'].fillna(0)
        
        # Formatage des codes CIP et libellés (ajout pour cohérence avec load_data)
        df['code_cip'] = df['CIP13'].astype(str)
        df['libelle_cip'] = df['l_cip13'].fillna('Non spécifié')
        
        # Conversion des colonnes financières (format français)
        def convert_french_decimal(series):
            """Convertit les décimaux français (virgule) en float"""
            cleaned = series.astype(str).str.strip()
            cleaned = cleaned.replace(['', 'nan', 'NaN', 'NULL', 'null'], np.nan)
            
            def clean_french_number(x):
                if pd.isna(x) or x == 'nan':
                    return np.nan
                x = str(x).strip()
                if ',' in x:
                    parts = x.split(',')
                    if len(parts) == 2:
                        entiere = parts[0].replace('.', '')
                        decimale = parts[1]
                        return f"{entiere}.{decimale}"
                return x.replace('.', '') if '.' in x else x
            
            cleaned = cleaned.apply(clean_french_number)
            return pd.to_numeric(cleaned, errors='coerce')
        
        # Conversion explicite en numérique pour éviter les erreurs de division
        df['BOITES'] = pd.to_numeric(df['BOITES'], errors='coerce')
        df['REM'] = convert_french_decimal(df['REM'])
        df['BSE'] = convert_french_decimal(df['BSE'])
        
        # Calculs des métriques dérivées
        df['cout_par_boite'] = np.where(df['BOITES'] > 0, df['REM'] / df['BOITES'], 0)
        
        return df
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données: {e}")
        return None

def load_data(nrows=None):  # Charger toutes les lignes par défaut
    """🚀 Interface de chargement avec pré-chargement automatique"""
    
    # Vérifier si les données sont déjà en session_state
    if 'phmev_data_cached' in st.session_state and st.session_state.phmev_data_cached is not None:
        return st.session_state.phmev_data_cached
    
    try:
        # Interface de chargement uniquement si pas en cache
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("📁 Lecture du fichier CSV...")
        progress_bar.progress(10)
        
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Priorité 1: Parquet (plus rapide)
        parquet_path = os.path.join(script_dir, 'OPEN_PHMEV_2024.parquet')
        csv_path = os.path.join(script_dir, 'OPEN_PHMEV_2024.CSV')
        
        # Essayer d'abord le format Parquet
        if os.path.exists(parquet_path):
            status_text.text("🚀 Chargement ultra-rapide depuis Parquet...")
            progress_bar.progress(50)
            try:
                df = pd.read_parquet(parquet_path)
                
                # Ajouter les colonnes dérivées si nécessaires
                if 'etablissement' not in df.columns:
                    df['etablissement'] = df['nom_etb'].astype(str).fillna('Non spécifié')
                    if 'raison_sociale_etb' in df.columns:
                        df['etablissement'] = df['etablissement'].where(
                            df['etablissement'] != 'nan', 
                            df['raison_sociale_etb'].astype(str)
                        )
                
                if 'medicament' not in df.columns:
                    df['medicament'] = df['L_ATC5'].astype(str).fillna('Non spécifié')
                if 'categorie' not in df.columns:
                    df['categorie'] = df['categorie_jur'].astype(str).fillna('Non spécifiée')
                if 'ville' not in df.columns:
                    df['ville'] = df['nom_ville'].astype(str).fillna('Non spécifiée')
                if 'region' not in df.columns:
                    df['region'] = df['region_etb'].fillna(0)
                if 'code_cip' not in df.columns:
                    df['code_cip'] = df['CIP13'].astype(str)
                if 'libelle_cip' not in df.columns:
                    df['libelle_cip'] = df['l_cip13'].fillna('Non spécifié')
                
                progress_bar.progress(100)
                status_text.text("✅ Données Parquet chargées avec succès !")
                st.session_state.phmev_data_cached = df
                
                # Nettoyage
                import time, gc
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
                gc.collect()
                
                return df
                
            except Exception as e:
                st.warning(f"⚠️ Erreur avec le fichier Parquet: {e}. Essai avec le CSV...")
        
        # Fallback sur CSV
        if not os.path.exists(csv_path):
            # Si aucun fichier n'existe, utiliser les données d'exemple
            try:
                from sample_data import create_sample_data
                st.warning("⚠️ Fichier PHMEV principal non trouvé. Utilisation de données d'exemple pour la démonstration.")
                df = create_sample_data()
                st.session_state.phmev_data_cached = df
                return df
            except ImportError:
                st.error("❌ Impossible de charger les données d'exemple. Veuillez ajouter le fichier OPEN_PHMEV_2024.parquet ou .CSV")
                return None
        
        # Optimisation mémoire maximale (sans category pour éviter les erreurs)
        dtype_dict = {
            'CIP13': 'str', 
            'l_cip13': 'str',
            'BOITES': 'int32',  # Au lieu de int64
            'region_etb': 'int16',  # Au lieu de int64
            'nom_etb': 'string',  # String nullable plus efficace
            'raison_sociale_etb': 'string'
        }
        
        df = pd.read_csv(
            csv_path, 
            nrows=nrows, 
            encoding='latin1', 
            sep=';',
            low_memory=True,
            dtype=dtype_dict,
            engine='c'  # Moteur C plus rapide
        )
        
        progress_bar.progress(40)
        status_text.text("🔧 Nettoyage des données...")
        
        # Nettoyage et optimisation des données - vérification des colonnes
        status_text.text("💰 Vérification des colonnes financières...")
        
        # Nettoyage des colonnes financières (format français avec virgules)
        
        # Conversion robuste des colonnes financières
        def convert_french_decimal(series):
            """Convertit les décimaux français (point milliers, virgule décimales) en float"""
            cleaned = series.astype(str)
            cleaned = cleaned.str.strip()
            
            # Remplacer les valeurs vides par NaN
            cleaned = cleaned.replace(['', 'nan', 'NaN', 'NULL', 'null'], np.nan)
            
            # Gérer le format français : 336.578,01 → 336578.01
            def clean_french_number(x):
                if pd.isna(x) or x == 'nan':
                    return np.nan
                x = str(x).strip()
                if ',' in x:
                    # Séparer partie entière et décimales
                    parts = x.split(',')
                    if len(parts) == 2:
                        # Partie entière : supprimer les points (milliers)
                        entiere = parts[0].replace('.', '')
                        # Partie décimale
                        decimale = parts[1]
                        # Reconstituer au format anglais
                        return f"{entiere}.{decimale}"
                # Si pas de virgule, supprimer les points (milliers seulement)
                return x.replace('.', '') if '.' in x else x
            
            cleaned = cleaned.apply(clean_french_number)
            return pd.to_numeric(cleaned, errors='coerce')
        
        # Appliquer la conversion
        df['REM'] = convert_french_decimal(df['REM'])
        df['BSE'] = convert_french_decimal(df['BSE'])
        
        # Statistiques de conversion
        total_rows = len(df)
        rem_valid = df['REM'].notna().sum()
        bse_valid = df['BSE'].notna().sum()
        
        # Conversion réussie (message supprimé pour épurer l'interface)
        
        progress_bar.progress(60)
        status_text.text("📊 Création des colonnes dérivées...")
        
        # Création de colonnes enrichies avec gestion sécurisée des NaN
        df['etablissement'] = df['nom_etb'].astype(str).fillna('Non spécifié')
        if 'raison_sociale_etb' in df.columns:
            df['etablissement'] = df['etablissement'].where(
                df['etablissement'] != 'nan', 
                df['raison_sociale_etb'].astype(str)
            )
        
        df['medicament'] = df['L_ATC5'].astype(str).fillna('Non spécifié')
        df['categorie'] = df['categorie_jur'].astype(str).fillna('Non spécifiée')
        df['ville'] = df['nom_ville'].astype(str).fillna('Non spécifiée')
        df['region'] = df['region_etb'].fillna(0)
        
        # Formatage des codes CIP et libellés
        df['code_cip'] = df['CIP13'].astype(str)
        df['libelle_cip'] = df['l_cip13'].fillna('Non spécifié')
        
        # Garder les types par défaut pour éviter les problèmes de mémoire
        
        progress_bar.progress(80)
        status_text.text("🧮 Calculs des métriques...")
        
        # Conversion explicite en numérique pour éviter les erreurs de division
        # Note: REM et BSE sont déjà convertis par convert_french_decimal() plus haut
        df['BOITES'] = pd.to_numeric(df['BOITES'], errors='coerce')
        
        # Calculs dérivés
        df['cout_par_boite'] = df['REM'] / df['BOITES'].replace(0, np.nan)
        df['taux_remboursement'] = (df['REM'] / df['BSE'].replace(0, np.nan) * 100).round(2)
        
        progress_bar.progress(100)
        status_text.text("✅ Données chargées avec succès !")
        
        # Stocker en session_state pour éviter les rechargements
        st.session_state.phmev_data_cached = df
        
        # Nettoyage de l'interface et mémoire
        import time
        import gc
        time.sleep(1)  # Réduire le temps d'attente
        progress_bar.empty()
        status_text.empty()
        gc.collect()  # Forcer le garbage collection
        
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement: {e}")
        return None

@st.cache_data(show_spinner=False, ttl=1800, persist=None)
def get_all_filter_options(df):
    """🚀 Pré-calcule TOUTES les options de filtres en une seule fois pour une vitesse maximale"""
    
    def safe_sort_atc_items(items_dict):
        """Tri sécurisé des items ATC en gérant les types mixtes"""
        try:
            return sorted(items_dict.items(), key=lambda x: (str(x[0]), str(x[1])))
        except Exception:
            # Fallback: trier seulement par libellé
            return sorted(items_dict.items(), key=lambda x: str(x[1]))
    
    options = {
        # ATC Hierarchy avec codes et libellés (tri sécurisé)
        'atc1': safe_sort_atc_items(df[['atc1', 'l_atc1']].drop_duplicates().set_index('atc1')['l_atc1'].dropna().to_dict()),
        'atc2': safe_sort_atc_items(df[['atc2', 'L_ATC2']].drop_duplicates().set_index('atc2')['L_ATC2'].dropna().to_dict()),
        'atc3': safe_sort_atc_items(df[['atc3', 'L_ATC3']].drop_duplicates().set_index('atc3')['L_ATC3'].dropna().to_dict()),
        'atc4': safe_sort_atc_items(df[['atc4', 'L_ATC4']].drop_duplicates().set_index('atc4')['L_ATC4'].dropna().to_dict()),
        'atc5': safe_sort_atc_items(df[['ATC5', 'L_ATC5']].drop_duplicates().set_index('ATC5')['L_ATC5'].dropna().to_dict()),
        
        # CIP avec index de recherche rapide (utiliser les colonnes originales)
        'cip_codes': sorted([str(x) for x in df['CIP13'].dropna().unique()]),
        'cip_libelles': sorted([str(x) for x in df['l_cip13'].dropna().unique()]),
        'cip_search_index': {str(lib).lower(): str(lib) for lib in df['l_cip13'].dropna().unique() if str(lib) not in ['Non restitué', 'Honoraires de dispensation']},
        
        # Autres filtres avec index
        'etablissements': sorted([str(x) for x in df['etablissement'].dropna().unique()]),
        'etablissements_index': {str(etab).lower(): str(etab) for etab in df['etablissement'].dropna().unique()},
        'categories': sorted([str(x) for x in df['categorie'].dropna().unique()]),
        'villes': sorted([str(x) for x in df['ville'].dropna().unique()]),
        'villes_index': {str(ville).lower(): str(ville) for ville in df['ville'].dropna().unique()}
    }
    return options

def ultra_fast_search(search_index, search_term, max_results=50):
    """⚡ Recherche ultra-rapide avec scoring dans un index pré-calculé"""
    if not search_term or len(search_term) < 2:
        return []
    
    search_lower = search_term.lower().strip()
    search_words = search_lower.split()
    results = []
    
    for key_lower, original_value in search_index.items():
        # Vérifier si tous les mots de recherche sont présents
        if all(word in key_lower for word in search_words):
            # Score: priorité aux correspondances exactes et au début
            score = 0
            if key_lower.startswith(search_lower):
                score = -2  # Priorité maximale
            elif search_lower in key_lower:
                score = -1  # Priorité élevée
            else:
                score = len(search_words) - sum(1 for word in search_words if word in key_lower)
            
            results.append((score, original_value))
    
    # Trier par score puis alphabétiquement
    results.sort(key=lambda x: (x[0], x[1].lower()))
    return [item[1] for item in results[:max_results]]

def format_number(value):
    """💫 Formatage sexy des nombres"""
    if pd.isna(value):
        return "N/A"
    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return f"{value:,.0f}"

def format_currency(value):
    """💰 Formatage sexy des montants"""
    if pd.isna(value):
        return "N/A"
    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.1f}B€"
    elif value >= 1_000_000:
        return f"{value/1_000_000:.1f}M€"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K€"
    else:
        return f"{value:,.2f}€"

def create_metric_card(title, value, delta=None, help_text="", icon="📊"):
    """🎨 Créer une carte de métrique stylée"""
    delta_html = f"<div style='color: #4facfe; font-size: 0.8rem; margin-top: 0.5rem;'>{delta}</div>" if delta else ""
    
    return f"""
    <div style="background: #1e2130; padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 10px 30px rgba(0,0,0,0.3); transition: transform 0.3s ease;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <span style="font-size: 1.5rem;">{icon}</span>
            <span style="font-size: 0.9rem; opacity: 0.8; color: white;">{title}</span>
        </div>
        <div style="font-size: 2rem; font-weight: 700; color: #4facfe;">{value}</div>
        {delta_html}
        <div style="font-size: 0.75rem; opacity: 0.7; margin-top: 0.5rem; color: #cccccc;">{help_text}</div>
    </div>
    """

def initialize_app():
    """🚀 Initialise l'application avec chargement en session uniquement"""
    if 'data_preloaded' not in st.session_state:
        st.session_state.data_preloaded = False
        
    if not st.session_state.data_preloaded:
        # Pré-chargement en session uniquement (sans cache disque)
        try:
            if 'phmev_data_cached' not in st.session_state:
                with st.spinner("🚀 Chargement initial des données (dataset complet)..."):
                    df = load_data_background()
                    if df is not None:
                        st.session_state.phmev_data_cached = df
                        st.success("✅ Toutes les données chargées ! Application prête.")
            st.session_state.data_preloaded = True
        except Exception as e:
            st.warning(f"⚠️ Chargement différé : {e}")
            st.session_state.data_preloaded = True

def main():
    # Interface de configuration
    st.sidebar.markdown("## ⚙️ **Configuration**")
    
    # Option pour activer/désactiver le pré-chargement
    auto_preload = st.sidebar.checkbox(
        "🚀 Pré-chargement automatique", 
        value=True, 
        help="Charge les données automatiquement au démarrage"
    )
    
    # 🚀 Initialisation automatique au démarrage si activée
    if auto_preload:
        initialize_app()
    
    # 🔄 Vider le cache si nécessaire
    if st.sidebar.button("🔄 Vider le cache"):
        if 'phmev_data_cached' in st.session_state:
            del st.session_state.phmev_data_cached
        if 'data_preloaded' in st.session_state:
            del st.session_state.data_preloaded
        st.cache_data.clear()
        st.rerun()
    
    # 🎨 Titre sexy de l'application
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; text-align: center; 
                margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <h1 style="font-size: 3rem; font-weight: 700; margin: 0; color: white; 
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            🚀 PHMEV Analytics Pro
        </h1>
        <p style="font-size: 1.2rem; margin: 0.5rem 0 0 0; color: white; opacity: 0.9;">
            ✨ Analyse avancée des délivrances pharmaceutiques
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 🔄 Chargement complet de toutes les données
    df = load_data()  # Charger toutes les lignes du dataset
    
    if df is None:
        st.stop()
    
    # 📊 Informations sur le dataset
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); 
                padding: 1.5rem; border-radius: 15px; text-align: center; 
                margin-bottom: 2rem; backdrop-filter: blur(10px);
                border: 1px solid rgba(102, 126, 234, 0.2);">
        <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 0.8rem;">
                <span style="font-size: 2rem;">📅</span>
                <div>
                    <div style="font-weight: 700; color: white; font-size: 1.3rem;">
                        2024
                    </div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.8); text-transform: uppercase; letter-spacing: 0.5px;">
                        Année étudiée
                    </div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 0.8rem;">
                <span style="font-size: 2rem;">📊</span>
                <div>
                    <div style="font-weight: 700; color: white; font-size: 1.3rem;">
                        {len(df):,} lignes
                    </div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.8); text-transform: uppercase; letter-spacing: 0.5px;">
                        Dataset analysé
                    </div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 0.8rem;">
                <span style="font-size: 2rem;">🏛️</span>
                <div>
                    <div style="font-weight: 700; color: white; font-size: 1.3rem;">
                        CNAM Open Data
                    </div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.8); text-transform: uppercase; letter-spacing: 0.5px;">
                        Source officielle
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 🚀 Pré-calcul ultra-rapide de TOUS les filtres
    filter_options = get_all_filter_options(df)
    
    # 🎛️ Sidebar ultra moderne
    with st.sidebar:
        st.markdown("## ⚡ **Filtres Ultra-Rapides**")
        
        # Hiérarchie pharmaceutique complète selon la structure PHMEV
        st.markdown("### 💊 **Hiérarchie Pharmaceutique**")
        st.markdown("*Navigation hiérarchique : ATC1 → ATC2 → ATC3 → ATC4 → ATC5 → CIP13*")
        
        # ========== NIVEAU 1: ATC1 (Systèmes thérapeutiques) ==========
        st.markdown("#### 🧬 **Niveau 1 - Systèmes Anatomiques (ATC1)**")
        atc1_display = [f"{code} - {libelle}" for code, libelle in filter_options['atc1']]
        
        atc1_selection = st.multiselect(
            "Sélectionner les systèmes anatomiques",
            options=atc1_display,
            default=[],
            help="Première classification : systèmes anatomiques principaux"
        )
        
        # Extraire les codes ATC1 sélectionnés
        atc1_codes = [sel.split(' - ')[0] for sel in atc1_selection] if atc1_selection else []
        atc1_filtre = [dict(filter_options['atc1'])[code] for code in atc1_codes] if atc1_codes else []
        
        # ========== NIVEAU 2: ATC2 (Groupes thérapeutiques) ==========
        if atc1_filtre:
            st.markdown("#### 💉 **Niveau 2 - Groupes Thérapeutiques (ATC2)**")
            # Filtrer ATC2 basé sur ATC1 sélectionnés
            df_atc1_filtered = df[df['l_atc1'].isin(atc1_filtre)]
            atc2_options = sorted(df_atc1_filtered[['atc2', 'L_ATC2']].drop_duplicates().set_index('atc2')['L_ATC2'].dropna().to_dict().items(), key=lambda x: str(x[1]))
            atc2_display = [f"{code} - {libelle}" for code, libelle in atc2_options]
            
            atc2_selection = st.multiselect(
                "Sélectionner les groupes thérapeutiques",
                options=atc2_display,
                default=[],
                help="Deuxième classification : groupes thérapeutiques principaux"
            )
            
            atc2_codes = [sel.split(' - ')[0] for sel in atc2_selection] if atc2_selection else []
            atc2_filtre = [dict(atc2_options)[code] for code in atc2_codes] if atc2_codes else []
        else:
            atc2_filtre = []
        
        # ========== NIVEAU 3: ATC3 (Sous-groupes pharmacologiques) ==========
        if atc2_filtre:
            st.markdown("#### 🔬 **Niveau 3 - Sous-groupes Pharmacologiques (ATC3)**")
            df_atc2_filtered = df[df['L_ATC2'].isin(atc2_filtre)]
            atc3_options = sorted(df_atc2_filtered[['atc3', 'L_ATC3']].drop_duplicates().set_index('atc3')['L_ATC3'].dropna().to_dict().items())
            atc3_display = [f"{code} - {libelle}" for code, libelle in atc3_options]
            
            atc3_selection = st.multiselect(
                "Sélectionner les sous-groupes pharmacologiques",
                options=atc3_display,
                default=[],
                help="Troisième classification : sous-groupes pharmacologiques"
            )
            
            atc3_codes = [sel.split(' - ')[0] for sel in atc3_selection] if atc3_selection else []
            atc3_filtre = [dict(atc3_options)[code] for code in atc3_codes] if atc3_codes else []
        else:
            atc3_filtre = []
        
        # ========== NIVEAU 4: ATC4 (Groupes chimiques) ==========
        if atc3_filtre:
            st.markdown("#### ⚗️ **Niveau 4 - Groupes Chimiques (ATC4)**")
            df_atc3_filtered = df[df['L_ATC3'].isin(atc3_filtre)]
            atc4_options = sorted(df_atc3_filtered[['atc4', 'L_ATC4']].drop_duplicates().set_index('atc4')['L_ATC4'].dropna().to_dict().items())
            atc4_display = [f"{code} - {libelle}" for code, libelle in atc4_options]
            
            atc4_selection = st.multiselect(
                "Sélectionner les groupes chimiques",
                options=atc4_display,
                default=[],
                help="Quatrième classification : groupes chimiques/thérapeutiques"
            )
            
            atc4_codes = [sel.split(' - ')[0] for sel in atc4_selection] if atc4_selection else []
            atc4_filtre = [dict(atc4_options)[code] for code in atc4_codes] if atc4_codes else []
        else:
            atc4_filtre = []
        
        # ========== NIVEAU 5: ATC5 (Substances chimiques) ==========
        if atc4_filtre:
            st.markdown("#### 🧪 **Niveau 5 - Substances Chimiques (ATC5)**")
            df_atc4_filtered = df[df['L_ATC4'].isin(atc4_filtre)]
            atc5_options = sorted(df_atc4_filtered[['ATC5', 'L_ATC5']].drop_duplicates().set_index('ATC5')['L_ATC5'].dropna().to_dict().items())
            
            # Filtrer les "Non restitué"
            atc5_options_clean = [(code, libelle) for code, libelle in atc5_options if libelle != 'Non restitué']
            atc5_display = [f"{code} - {libelle}" for code, libelle in atc5_options_clean]
            
            if atc5_display:
                atc5_selection = st.multiselect(
                    "Sélectionner les substances chimiques",
                    options=atc5_display,
                    default=[],
                    help="Cinquième classification : substances chimiques spécifiques"
                )
                
                atc5_codes = [sel.split(' - ')[0] for sel in atc5_selection] if atc5_selection else []
                atc5_filtre = [dict(atc5_options_clean)[code] for code in atc5_codes] if atc5_codes else []
            else:
                st.info("ℹ️ Données ATC5 anonymisées à ce niveau")
                atc5_filtre = []
        else:
            atc5_filtre = []
        
        # ========== NIVEAU 6: CIP13 (Codes et libellés produits) ==========
        st.markdown("#### 📋 **Niveau 6 - Produits Spécifiques (CIP13)**")
        
        # Déterminer le dataset filtré pour les CIP
        if atc5_filtre:
            df_for_cip = df[df['L_ATC5'].isin(atc5_filtre)]
        elif atc4_filtre:
            df_for_cip = df[df['L_ATC4'].isin(atc4_filtre)]
        elif atc3_filtre:
            df_for_cip = df[df['L_ATC3'].isin(atc3_filtre)]
        elif atc2_filtre:
            df_for_cip = df[df['L_ATC2'].isin(atc2_filtre)]
        elif atc1_filtre:
            df_for_cip = df[df['l_atc1'].isin(atc1_filtre)]
        else:
            df_for_cip = df
        
        # ⚡ Recherche ultra-rapide des médicaments avec aperçu
        libelle_search = st.text_input(
            "🔍 Rechercher un médicament",
            placeholder="Ex: cabometyx, doliprane, ventoline, omeprazole...",
            help="Recherche instantanée dans les noms de médicaments",
            key="libelle_search"
        )
        
        # Filtrage ultra-rapide avec l'index pré-calculé
        if libelle_search:
            libelles_filtered = ultra_fast_search(filter_options['cip_search_index'], libelle_search, max_results=100)
            
            if libelles_filtered:
                st.success(f"⚡ {len(libelles_filtered)} médicaments trouvés instantanément pour '{libelle_search}'")
                # Aperçu des premiers résultats
                if len(libelles_filtered) <= 10:
                    st.info("📋 **Résultats trouvés :** " + " • ".join(libelles_filtered[:10]))
                else:
                    st.info("📋 **Premiers résultats :** " + " • ".join(libelles_filtered[:5]) + f" ... (+{len(libelles_filtered)-5} autres)")
            else:
                st.warning(f"❌ Aucun médicament trouvé pour '{libelle_search}' - Essayez 'cabometyx', 'doliprane', 'ventoline', 'omeprazole'...")
                libelles_filtered = []
        else:
            libelles_filtered = filter_options['cip_libelles'][:100]
            if libelles_filtered:
                st.info(f"💡 {len(filter_options['cip_libelles'])} médicaments disponibles (affichage des 100 premiers)")
        
        libelle_filtre = st.multiselect(
            "🏷️ Sélectionner les médicaments",
            options=libelles_filtered,
            default=[],
            help="Sélectionnez les médicaments spécifiques à analyser"
        )
        
        # Codes CIP correspondants (optionnel)
        if libelle_filtre:
            st.markdown("##### 📋 **Codes CIP correspondants**")
            df_cip_selected = df_for_cip[df_for_cip['libelle_cip'].isin(libelle_filtre)]
            cip_options = sorted(df_cip_selected[['code_cip', 'libelle_cip']].drop_duplicates().values.tolist())
            cip_display = [f"{code} - {libelle}" for code, libelle in cip_options]
            
            cip_filtre_display = st.multiselect(
                "Codes CIP spécifiques (optionnel)",
                options=cip_display,
                default=[],
                help="Affinage par codes CIP si nécessaire"
            )
            
            cip_filtre = [sel.split(' - ')[0] for sel in cip_filtre_display] if cip_filtre_display else []
        else:
            cip_filtre = []
        
        st.markdown("---")
        
        # ⚡ Filtres ultra-rapides avec icônes
        st.markdown("### 🏥 **Établissements**")
        
        etablissement_search = st.text_input(
            "🔍 Rechercher un établissement",
            placeholder="Tapez pour filtrer les établissements...",
            help="Recherche instantanée dans les établissements",
            key="etablissement_search"
        )
        
        # Filtrage ultra-rapide avec l'index pré-calculé
        if etablissement_search:
            etablissements_filtered = ultra_fast_search(filter_options['etablissements_index'], etablissement_search, max_results=100)
            if etablissements_filtered:
                st.success(f"⚡ {len(etablissements_filtered)} établissements trouvés instantanément")
                # Aperçu des premiers résultats
                if len(etablissements_filtered) <= 5:
                    st.info("🏥 **Résultats :** " + " • ".join(etablissements_filtered[:5]))
                else:
                    st.info("🏥 **Premiers résultats :** " + " • ".join(etablissements_filtered[:3]) + f" ... (+{len(etablissements_filtered)-3} autres)")
            else:
                st.warning(f"❌ Aucun établissement trouvé pour '{etablissement_search}'")
                etablissements_filtered = []
        else:
            etablissements_filtered = filter_options['etablissements'][:100]
            if etablissements_filtered:
                st.info(f"💡 {len(filter_options['etablissements'])} établissements disponibles (affichage des 100 premiers)")
        
        etablissement_filtre = st.multiselect(
            "Sélectionner les établissements",
            options=etablissements_filtered,
            default=[],
            help="Choisissez un ou plusieurs établissements"
        )
        
        st.markdown("### 🏛️ **Catégories**")
        categorie_filtre = st.multiselect(
            "Types d'établissement",
            options=filter_options['categories'],
            default=[],
            help="Filtrer par catégorie juridique"
        )
        
        st.markdown("### 🌍 **Géographie**")
        
        ville_search = st.text_input(
            "🔍 Rechercher une ville",
            placeholder="Tapez pour filtrer les villes...",
            help="Recherche instantanée dans les villes",
            key="ville_search"
        )
        
        # Filtrage ultra-rapide avec l'index pré-calculé
        if ville_search:
            villes_filtered = ultra_fast_search(filter_options['villes_index'], ville_search, max_results=100)
            if villes_filtered:
                st.success(f"⚡ {len(villes_filtered)} villes trouvées instantanément")
                # Aperçu des premiers résultats
                if len(villes_filtered) <= 8:
                    st.info("🌍 **Résultats :** " + " • ".join(villes_filtered[:8]))
                else:
                    st.info("🌍 **Premiers résultats :** " + " • ".join(villes_filtered[:5]) + f" ... (+{len(villes_filtered)-5} autres)")
            else:
                st.warning(f"❌ Aucune ville trouvée pour '{ville_search}'")
                villes_filtered = []
        else:
            villes_filtered = filter_options['villes'][:100]
            
        ville_filtre = st.multiselect(
            "Sélectionner les villes",
            options=villes_filtered,
            default=[],
            help="Filtrage géographique"
        )
        
        st.markdown("### 📊 **Paramètres d'analyse**")
        top_n = st.slider(
            "🏆 Top N établissements",
            min_value=5,
            max_value=100,
            value=20,
            step=5,
            help="Nombre d'établissements dans le classement"
        )
        
        # Filtres avancés
        with st.expander("⚙️ **Filtres Avancés**"):
            min_boites = st.number_input(
                "📦 Minimum de boîtes",
                min_value=0,
                value=0,
                help="Seuil minimum de boîtes délivrées"
            )
            
            show_percentages = st.checkbox(
                "📈 Afficher les pourcentages",
                value=True,
                help="Inclure les pourcentages dans les tableaux"
            )
    
    # 🔧 Application des filtres (éviter df.copy() pour économiser la mémoire)
    df_filtered = df
    
    # Filtres ATC hiérarchiques (molécules/produits)
    if atc1_filtre:
        df_filtered = df_filtered[df_filtered['l_atc1'].isin(atc1_filtre)]
    
    if atc2_filtre:
        df_filtered = df_filtered[df_filtered['L_ATC2'].isin(atc2_filtre)]
    
    if atc3_filtre:
        df_filtered = df_filtered[df_filtered['L_ATC3'].isin(atc3_filtre)]
    
    if atc4_filtre:
        df_filtered = df_filtered[df_filtered['L_ATC4'].isin(atc4_filtre)]
    
    if atc5_filtre:
        df_filtered = df_filtered[df_filtered['L_ATC5'].isin(atc5_filtre)]
    
    # Filtres CIP
    if cip_filtre:
        df_filtered = df_filtered[df_filtered['code_cip'].isin(cip_filtre)]
    
    if libelle_filtre:
        df_filtered = df_filtered[df_filtered['libelle_cip'].isin(libelle_filtre)]
    
    # Autres filtres
    if etablissement_filtre:
        df_filtered = df_filtered[df_filtered['etablissement'].isin(etablissement_filtre)]
    
    if categorie_filtre:
        df_filtered = df_filtered[df_filtered['categorie'].isin(categorie_filtre)]
    
    if ville_filtre:
        df_filtered = df_filtered[df_filtered['ville'].isin(ville_filtre)]
    
    if min_boites > 0:
        df_filtered = df_filtered[df_filtered['BOITES'] >= min_boites]
    
    # 📊 Indicateur de filtrage actif
    filters_active = []
    if atc1_filtre: filters_active.append(f"ATC1: {len(atc1_filtre)}")
    if atc2_filtre: filters_active.append(f"ATC2: {len(atc2_filtre)}")
    if atc3_filtre: filters_active.append(f"ATC3: {len(atc3_filtre)}")
    if atc4_filtre: filters_active.append(f"ATC4: {len(atc4_filtre)}")
    if atc5_filtre: filters_active.append(f"ATC5: {len(atc5_filtre)}")
    if libelle_filtre: filters_active.append(f"Médicaments: {len(libelle_filtre)}")
    if cip_filtre: filters_active.append(f"CIP: {len(cip_filtre)}")
    if etablissement_filtre: filters_active.append(f"Établissements: {len(etablissement_filtre)}")
    if ville_filtre: filters_active.append(f"Villes: {len(ville_filtre)}")
    
    if filters_active:
        st.markdown(f"""
        <div class="info-card">
            <strong>🎯 Filtres actifs:</strong> {" | ".join(filters_active)}<br>
            <strong>📊 Données filtrées:</strong> {len(df_filtered):,} lignes sur {len(df):,} ({len(df_filtered)/len(df)*100:.1f}%)
        </div>
        """, unsafe_allow_html=True)
        
    
    if len(df_filtered) == 0:
        st.markdown("""
        <div class="warning-card">
            <strong>⚠️ Aucune donnée trouvée</strong><br>
            Essayez de modifier vos filtres pour obtenir des résultats
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    # 📊 KPIs Ultra Sexy
    st.markdown('## 💎 Métriques Globales')
    
    # Conversion finale des colonnes numériques pour éviter les erreurs de division
    # Note: REM et BSE sont déjà au bon format numérique depuis le chargement
    df_filtered['BOITES'] = pd.to_numeric(df_filtered['BOITES'], errors='coerce').fillna(0)
    df_filtered['REM'] = df_filtered['REM'].fillna(0)
    df_filtered['BSE'] = df_filtered['BSE'].fillna(0)
    
    # Calculs des métriques avec vérification
    total_boites = df_filtered['BOITES'].sum()
    total_rem = df_filtered['REM'].sum()
    total_bse = df_filtered['BSE'].sum()
    nb_etablissements = df_filtered['etablissement'].nunique()
    
    # Calculer les métriques dérivées correctement
    cout_moyen = total_rem / total_boites if total_boites > 0 else 0
    taux_remb_moyen = (total_rem / total_bse * 100) if total_bse > 0 else 0
    
    # Affichage des KPIs en grid ultra sexy
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card boxes">
            <div class="kpi-icon">📦</div>
            <div class="kpi-value">{format_number(total_boites)}</div>
            <div class="kpi-label">Total Boîtes</div>
            <div class="kpi-delta">Boîtes délivrées</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card money">
            <div class="kpi-icon">💰</div>
            <div class="kpi-value">{format_currency(total_rem)}</div>
            <div class="kpi-label">Montant Remboursé</div>
            <div class="kpi-delta">Par l'Assurance Maladie</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card base">
            <div class="kpi-icon">🏦</div>
            <div class="kpi-value">{format_currency(total_bse)}</div>
            <div class="kpi-label">Base Remboursable</div>
            <div class="kpi-delta">Montant de référence</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card count">
            <div class="kpi-icon">🏥</div>
            <div class="kpi-value">{format_number(nb_etablissements)}</div>
            <div class="kpi-label">Établissements</div>
            <div class="kpi-delta">Établissements uniques</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Métriques secondaires sexy
    st.markdown("<br>", unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown(f"""
        <div class="kpi-card money" style="margin-top: 1rem;">
            <div class="kpi-icon">💊</div>
            <div class="kpi-value">{format_currency(cout_moyen)}</div>
            <div class="kpi-label">Coût Moyen/Boîte</div>
            <div class="kpi-delta">Par boîte délivrée</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        taux_display = f"{taux_remb_moyen:.1f}%" if not pd.isna(taux_remb_moyen) else "N/A"
        st.markdown(f"""
        <div class="kpi-card base" style="margin-top: 1rem;">
            <div class="kpi-icon">📊</div>
            <div class="kpi-value">{taux_display}</div>
            <div class="kpi-label">Taux Remboursement</div>
            <div class="kpi-delta">Pourcentage moyen</div>
        </div>
        """, unsafe_allow_html=True)
    
    
    # 🏆 Analyse des Top établissements
    st.markdown(f'## 🏆 Top {top_n} Établissements')
    
    # Agrégation avec les colonnes essentielles
    groupby_cols = ['etablissement', 'ville', 'categorie']
    
    df_etb = df_filtered.groupby(groupby_cols).agg({
        'BOITES': 'sum',
        'REM': 'sum', 
        'BSE': 'sum'
    }).reset_index()
    
    # Conversion des colonnes numériques dans df_etb pour éviter les erreurs
    # Note: REM et BSE sont déjà au bon format numérique depuis le chargement
    df_etb['BOITES'] = pd.to_numeric(df_etb['BOITES'], errors='coerce').fillna(0)
    df_etb['REM'] = df_etb['REM'].fillna(0)
    df_etb['BSE'] = df_etb['BSE'].fillna(0)
    
    # Calculer les métriques dérivées après le groupby avec gestion des zéros
    df_etb['cout_par_boite'] = np.where(
        df_etb['BOITES'] > 0, 
        df_etb['REM'] / df_etb['BOITES'], 
        0
    )
    df_etb['taux_remboursement'] = np.where(
        df_etb['BSE'] > 0, 
        (df_etb['REM'] / df_etb['BSE'] * 100).round(2), 
        0
    )
    
    # Calcul des pourcentages avec protection contre division par zéro
    if show_percentages:
        df_etb['pct_boites'] = (df_etb['BOITES'] / max(total_boites, 1) * 100).round(2)
        df_etb['pct_rem'] = (df_etb['REM'] / max(total_rem, 1) * 100).round(2)
        df_etb['pct_bse'] = (df_etb['BSE'] / max(total_bse, 1) * 100).round(2)
    
    # Top N
    df_top = df_etb.nlargest(top_n, 'BOITES')
    
    # 📋 Tableau stylé
    
    # Formatage du tableau (optimisé mémoire)
    df_display_data = {
        'etablissement': df_top['etablissement'].tolist(),
        'ville': df_top['ville'].tolist(),
        'categorie': df_top['categorie'].tolist(),
        'Boîtes': [format_number(x) for x in df_top['BOITES']],
        'Remboursé': [format_currency(x) for x in df_top['REM']],
        'Remboursable': [format_currency(x) for x in df_top['BSE']],
        'Coût/Boîte': [format_currency(x) for x in df_top['cout_par_boite']],
        'Taux Remb.': [f"{x:.1f}%" if not pd.isna(x) else "N/A" for x in df_top['taux_remboursement']]
    }
    
    # Ajouter les colonnes ATC si nécessaires
    if atc1_filtre or atc2_filtre or atc3_filtre or atc4_filtre or atc5_filtre:
        if atc5_filtre and 'L_ATC5' in df_top.columns:
            df_display_data['L_ATC5'] = df_top['L_ATC5'].tolist()
        elif atc4_filtre and 'L_ATC4' in df_top.columns:
            df_display_data['L_ATC4'] = df_top['L_ATC4'].tolist()
        elif atc3_filtre and 'L_ATC3' in df_top.columns:
            df_display_data['L_ATC3'] = df_top['L_ATC3'].tolist()
        elif atc2_filtre and 'L_ATC2' in df_top.columns:
            df_display_data['L_ATC2'] = df_top['L_ATC2'].tolist()
        elif atc1_filtre and 'l_atc1' in df_top.columns:
            df_display_data['l_atc1'] = df_top['l_atc1'].tolist()
    
    # Ajouter les colonnes CIP si filtrées
    if cip_filtre and 'code_cip' in df_top.columns:
        df_display_data['code_cip'] = df_top['code_cip'].tolist()
    if libelle_filtre and 'libelle_cip' in df_top.columns:
        df_display_data['libelle_cip'] = df_top['libelle_cip'].tolist()
        
    df_display = pd.DataFrame(df_display_data)
    
    # Les colonnes sont déjà nommées correctement dans df_display
    columns_to_show = list(df_display.columns)
    
    # Calculer les pourcentages si demandés
    if show_percentages:
        # Recalculer les valeurs numériques pour les pourcentages
        total_boites = df_top['BOITES'].sum()
        total_rem = df_top['REM'].sum()
        
        df_display['% Boîtes'] = [(x/total_boites*100) for x in df_top['BOITES']]
        df_display['% Boîtes'] = [f"{x:.1f}%" for x in df_display['% Boîtes']]
        
        df_display['% Remboursé'] = [(x/total_rem*100) for x in df_top['REM']]
        df_display['% Remboursé'] = [f"{x:.1f}%" for x in df_display['% Remboursé']]
        
        columns_to_show = list(df_display.columns)
    
    table_display = df_display
    
    st.dataframe(
        table_display,
        use_container_width=True,
        hide_index=True
    )
    
    # Export des données établissements (déplacé ici)
    csv_data = table_display.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger Top Établissements",
        data=csv_data,
        file_name=f"top_{top_n}_etablissements_phmev_pro_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        help="Export CSV du classement des établissements",
        type="primary"
    )
    
    
    # 🏆 Top Produits pour les établissements sélectionnés
    if len(df_filtered) > 0:
        st.markdown('## 🏆 Top Produits des Établissements Sélectionnés')
        
        # Analyse des produits les plus délivrés (exclure Non restitué)
        df_top_produits = df_filtered[
            ~df_filtered['libelle_cip'].isin(['Non restitué', 'Non spécifié', 'Honoraires de dispensation'])
        ].groupby(['libelle_cip']).agg({
            'BOITES': 'sum',
            'REM': 'sum',
            'BSE': 'sum',
            'etablissement': 'nunique'
        }).reset_index()
        
        # Calculer les métriques dérivées
        df_top_produits['cout_par_boite'] = np.where(
            df_top_produits['BOITES'] > 0,
            df_top_produits['REM'] / df_top_produits['BOITES'],
            0
        )
        df_top_produits['taux_remboursement'] = np.where(
            df_top_produits['BSE'] > 0,
            df_top_produits['REM'] / df_top_produits['BSE'] * 100,
            0
        )
        
        # Trier par nombre de boîtes et prendre le top 15
        df_top_produits = df_top_produits.nlargest(15, 'BOITES')
        
        # Formatage pour l'affichage (optimisé mémoire)
        df_produits_data = {
            'Produit': df_top_produits['libelle_cip'].tolist(),
            'Boîtes': [format_number(x) for x in df_top_produits['BOITES']],
            'Montant Remboursé': [format_currency(x) for x in df_top_produits['REM']],
            'Base Remboursement': [format_currency(x) for x in df_top_produits['BSE']],
            'Nb Établissements': df_top_produits['etablissement'].tolist(),
            'Coût/Boîte': [format_currency(x) for x in df_top_produits['cout_par_boite']],
            'Taux Remboursement': [f"{x:.1f}%" for x in df_top_produits['taux_remboursement']]
        }
        df_top_produits_display = pd.DataFrame(df_produits_data)
        
        st.dataframe(
            df_top_produits_display,
            use_container_width=True,
            hide_index=True
        )
        
        # Export des données produits
        csv_data_produits = df_top_produits_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger Top Produits",
            data=csv_data_produits,
            file_name=f"top_produits_phmev_pro_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            help="Export CSV du top des produits",
            type="primary"
        )
        
    
    # 🧪 TOP MOLÉCULES (SUBSTANCES CHIMIQUES)
    if len(df_filtered) > 0 and 'L_ATC5' in df_filtered.columns:
        st.markdown('## 🧪 Top Molécules (Substances Chimiques)')
        
        # Filtrer les molécules valides (exclure "Non restitué" et NaN)
        # Utiliser un masque pour éviter les problèmes de mémoire avec .copy()
        mask_molecules = (
            (df_filtered['L_ATC5'].notna()) & 
            (df_filtered['L_ATC5'] != 'Non restitué') &
            (df_filtered['L_ATC5'] != 'Non spécifié') &
            (df_filtered['L_ATC5'].str.strip() != '')
        )
        df_molecules = df_filtered[mask_molecules]
        
        if len(df_molecules) > 0:
            # Grouper par molécule (substance chimique)
            df_top_molecules = df_molecules.groupby('L_ATC5').agg({
                'BOITES': 'sum',
                'REM': 'sum',
                'BSE': 'sum',
                'etablissement': 'nunique',
                'libelle_cip': 'nunique'  # Nombre de produits différents
            }).reset_index()
            
            # Calculer les métriques dérivées
            df_top_molecules['cout_par_boite'] = np.where(
                df_top_molecules['BOITES'] > 0,
                df_top_molecules['REM'] / df_top_molecules['BOITES'],
                0
            )
            df_top_molecules['taux_remboursement'] = np.where(
                df_top_molecules['BSE'] > 0,
                df_top_molecules['REM'] / df_top_molecules['BSE'] * 100,
                0
            )
            
            # Trier par nombre de boîtes et prendre le top 15
            df_top_molecules = df_top_molecules.nlargest(15, 'BOITES')
            
            # Affichage du tableau uniquement (sans graphique)
            # Formatage pour l'affichage (optimisé mémoire)
            df_display_data = {
                'Molécule': df_top_molecules['L_ATC5'].tolist(),
                'Boîtes': [format_number(x) for x in df_top_molecules['BOITES']],
                'Montant Remboursé': [format_currency(x) for x in df_top_molecules['REM']],
                'Base Remboursement': [format_currency(x) for x in df_top_molecules['BSE']],
                'Nb Établissements': df_top_molecules['etablissement'].tolist(),
                'Nb Produits': df_top_molecules['libelle_cip'].tolist(),
                'Coût/Boîte': [format_currency(x) for x in df_top_molecules['cout_par_boite']],
                'Taux Remboursement': [f"{x:.1f}%" for x in df_top_molecules['taux_remboursement']]
            }
            df_top_molecules_display = pd.DataFrame(df_display_data)
            
            st.dataframe(
                df_top_molecules_display,
                use_container_width=True,
                hide_index=True
            )
            
            # Export des données molécules
            csv_data_molecules = df_top_molecules_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger Top Molécules",
                data=csv_data_molecules,
                file_name=f"top_molecules_phmev_pro_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                help="Export CSV du top des molécules",
                type="primary"
            )
        else:
            st.info("🔍 Aucune molécule spécifique trouvée avec les filtres actuels.")
    
    # 💊 Analyse des molécules/produits si filtrés
    if atc1_filtre or atc2_filtre or atc3_filtre or atc4_filtre:
        st.markdown('<h2 class="section-header">💊 Analyse des Molécules/Produits</h2>', unsafe_allow_html=True)
        
        # Déterminer quelle colonne ATC utiliser
        if atc4_filtre:
            atc_col = 'L_ATC4'
            atc_title = "Groupes Chimiques"
        elif atc3_filtre:
            atc_col = 'L_ATC3'
            atc_title = "Sous-groupes Pharmacologiques"
        elif atc2_filtre:
            atc_col = 'L_ATC2'
            atc_title = "Groupes Thérapeutiques"
        else:
            atc_col = 'l_atc1'
            atc_title = "Systèmes Thérapeutiques"
        
        # Analyse par produit/molécule
        df_produits = df_filtered.groupby(atc_col).agg({
            'BOITES': 'sum',
            'REM': 'sum',
            'BSE': 'sum',
            'etablissement': 'nunique',
            'cout_par_boite': 'mean'
        }).reset_index()
        
        df_produits.columns = ['Produit/Molécule', 'Boîtes', 'Remboursé', 'Remboursable', 'Nb Établissements', 'Coût Moyen/Boîte']
        
        # Formatage
        df_produits['Boîtes'] = df_produits['Boîtes'].apply(format_number)
        df_produits['Remboursé'] = df_produits['Remboursé'].apply(format_currency)
        df_produits['Remboursable'] = df_produits['Remboursable'].apply(format_currency)
        df_produits['Coût Moyen/Boîte'] = df_produits['Coût Moyen/Boîte'].apply(format_currency)
        
        st.markdown(f"### 📊 **{atc_title} Sélectionnés**")
        st.dataframe(df_produits, use_container_width=True, hide_index=True)
        
        # Graphique des produits
        if len(df_produits) > 1:
            fig_produits = px.bar(
                df_produits.head(10),
                x='Produit/Molécule',
                y=df_produits['Boîtes'].apply(lambda x: float(x.replace('K', '000').replace('M', '000000').replace(',', '')) if 'K' in x or 'M' in x else float(x.replace(',', ''))),
                title=f"🧬 Top 10 {atc_title} par Boîtes Délivrées",
                color_discrete_sequence=['#667eea']
            )
            
            fig_produits.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                title_font_size=16,
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig_produits, use_container_width=True)
    
    # 📋 Analyse des codes CIP si filtrés
    if cip_filtre or libelle_filtre:
        st.markdown('<h2 class="section-header">📋 Analyse des Codes CIP</h2>', unsafe_allow_html=True)
        
        # Analyse par code CIP
        df_cip = df_filtered.groupby(['code_cip', 'libelle_cip']).agg({
            'BOITES': 'sum',
            'REM': 'sum',
            'BSE': 'sum',
            'etablissement': 'nunique',
            'cout_par_boite': 'mean'
        }).reset_index()
        
        df_cip.columns = ['Code CIP', 'Libellé', 'Boîtes', 'Remboursé', 'Remboursable', 'Nb Établissements', 'Coût Moyen/Boîte']
        
        # Formatage
        df_cip['Boîtes'] = df_cip['Boîtes'].apply(format_number)
        df_cip['Remboursé'] = df_cip['Remboursé'].apply(format_currency)
        df_cip['Remboursable'] = df_cip['Remboursable'].apply(format_currency)
        df_cip['Coût Moyen/Boîte'] = df_cip['Coût Moyen/Boîte'].apply(format_currency)
        
        st.markdown("### 💊 **Détail des Codes CIP Sélectionnés**")
        st.dataframe(df_cip, use_container_width=True, hide_index=True)
        
        # Graphique des CIP les plus délivrés
        if len(df_cip) > 1:
            # Créer un libellé court pour l'affichage (optimisé mémoire)
            df_top10 = df_cip.head(10)
            libelles_courts = [x[:30] + "..." if len(x) > 30 else x for x in df_top10['Libellé']]
            boites_values = [float(x.replace('K', '000').replace('M', '000000').replace(',', '')) if 'K' in x or 'M' in x else float(x.replace(',', '')) for x in df_top10['Boîtes']]
            
            fig_cip = px.bar(
                x=libelles_courts,
                y=boites_values,
                title="📋 Top 10 Codes CIP par Boîtes Délivrées",
                color_discrete_sequence=['#f093fb'],
                labels={'x': 'Libellé', 'y': 'Boîtes'}
            )
            
            fig_cip.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                title_font_size=16,
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig_cip, use_container_width=True)
    
    # Section d'export supprimée - boutons déplacés sous chaque tableau
    
    # ℹ️ Informations détaillées
    with st.expander("ℹ️ **Informations Techniques**"):
        st.markdown(f"""
        ### 📊 **Statistiques du Dataset**
        - **Lignes totales:** {len(df):,}
        - **Lignes filtrées:** {len(df_filtered):,}
        - **Taux de filtrage:** {(len(df_filtered)/len(df)*100):.1f}%
        - **Source:** OPEN_PHMEV_2024.CSV
        
        ### 🔧 **Colonnes Analysées**
        - **BOITES:** Nombre de boîtes délivrées
        - **REM:** Montant remboursé par l'Assurance Maladie (€)
        - **BSE:** Montant remboursable - base de remboursement (€)
        - **Coût/Boîte:** Coût moyen par boîte (calculé)
        - **Taux Remb.:** Pourcentage de remboursement (calculé)
        
        ### 🎨 **Fonctionnalités Pro**
        - Interface moderne et responsive
        - Filtres intelligents avec recherche
        - Visualisations interactives
        - Métriques calculées automatiquement
        - Export multi-format
        
        ---
        <div style="text-align: center; opacity: 0.7; margin-top: 2rem;">
            <strong>🚀 PHMEV Analytics Pro</strong> - Version {datetime.now().strftime('%Y.%m')}
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
