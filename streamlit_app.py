"""
🚀 Application Streamlit SEXY pour l'analyse des données PHMEV
💊 Analyse avancée des délivrances pharmaceutiques par établissement
✨ Design moderne et interface intuitive - Version optimisée Streamlit Cloud
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

# CSS léger pour embellir juste la partie résultats
st.markdown("""
<style>
/* Colonnes avec fond contrasté pour bien voir les tableaux blancs */
[data-testid="column"] {
    background: linear-gradient(145deg, #e2e8f0 0%, #cbd5e1 100%) !important;
    border: 1px solid #94a3b8 !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    margin: 0.5rem !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
}

/* 🎯 VRAIES CARDS MODERNES - Design Premium */
.kpi-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    border: 2px solid #e2e8f0;
    border-radius: 20px;
    padding: 2rem 1.5rem;
    margin: 1rem 0.5rem;
    min-height: 160px;
        position: relative;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 
        0 4px 20px rgba(0,0,0,0.08),
        inset 0 1px 0 rgba(255,255,255,0.9);
    text-align: center;
        overflow: hidden;
    }
    
/* Barre colorée selon le type de card */
.kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
    height: 5px;
    border-radius: 20px 20px 0 0;
}

.kpi-card.money::before { background: linear-gradient(90deg, #667eea, #764ba2); }
.kpi-card.base::before { background: linear-gradient(90deg, #4facfe, #00f2fe); }
.kpi-card.count::before { background: linear-gradient(90deg, #43e97b, #38f9d7); }

/* Effet hover magnifique - RENFORCÉ */
.kpi-card:hover,
div[class*="kpi-card"]:hover {
    transform: translateY(-8px) scale(1.02) !important;
    box-shadow: 
        0 25px 50px rgba(0,0,0,0.15),
        inset 0 1px 0 rgba(255,255,255,0.9) !important;
    border-color: rgba(102, 126, 234, 0.4) !important;
}

/* Styles KPI persistants après filtrage */
.kpi-value,
div[class*="kpi-value"] {
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    line-height: 1 !important;
    margin: 1rem 0 !important;
    background: linear-gradient(135deg, #1e293b, #475569) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
}

.kpi-icon,
div[class*="kpi-icon"] {
    font-size: 2.5rem !important;
    margin-bottom: 1rem !important;
    display: block !important;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1)) !important;
}

.kpi-label,
div[class*="kpi-label"] {
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #475569 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    margin: 0.5rem 0 !important;
}


/* Delta/Description */
.kpi-delta {
    font-size: 0.85rem;
    color: #64748b;
    opacity: 0.8;
    font-style: italic;
    margin-top: 0.5rem;
}

/* 📊 TABLES - Centrage forcé avec CSS et JavaScript */
[data-testid="stDataFrame"] {
    border-radius: 8px !important;
    overflow: hidden !important;
    background: white !important;
}

/* 🎯 CENTRAGE ULTRA-FORCÉ - Tous les sélecteurs possibles */
[data-testid="stDataFrame"] td:nth-child(n+2),
[data-testid="stDataFrame"] th:nth-child(n+2),
.stDataFrame td:nth-child(n+2),
.stDataFrame th:nth-child(n+2),
div[data-testid="stDataFrame"] table td:nth-child(n+2),
div[data-testid="stDataFrame"] table th:nth-child(n+2) {
    text-align: center !important;
    text-align-last: center !important;
    font-weight: 600 !important;
    justify-content: center !important;
}

/* Première colonne à gauche */
[data-testid="stDataFrame"] td:first-child,
[data-testid="stDataFrame"] th:first-child {
    text-align: left !important;
    font-weight: 600 !important;
    padding-left: 1rem !important;
}

/* Headers de sections - Style normal et lisible */
h2 {
    color: #ffffff !important;
    border-bottom: 2px solid rgba(255,255,255,0.2) !important;
    padding-bottom: 0.5rem !important;
    margin-bottom: 1rem !important;
    font-weight: 600 !important;
}

/* Boutons download plus jolis */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        border: none !important;
    border-radius: 8px !important;
    color: white !important;
        font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(79, 172, 254, 0.3) !important;
    transition: transform 0.2s ease !important;
    }
    
    .stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(79, 172, 254, 0.4) !important;
}

/* Section d'infos dataset plus sombre et lisible */
div[style*="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1))"] {
    background: linear-gradient(135deg, #334155 0%, #475569 100%) !important;
    color: white !important;
    border: 1px solid #64748b !important;
}

/* Forcer le texte blanc dans la section d'infos */
div[style*="backdrop-filter: blur(10px)"] {
    background: linear-gradient(135deg, #334155 0%, #475569 100%) !important;
    color: white !important;
}

div[style*="backdrop-filter: blur(10px)"] div {
    color: white !important;
}

/* 🌙 FOND NOIR pour TOUTE la zone principale - RENFORCÉ pour persister */
[data-testid="stAppViewContainer"] .main .block-container,
.stApp .main .block-container,
section.main > div,
.main > div.block-container,
[data-testid="stAppViewContainer"] .main,
.stApp .main,
section.main,
.main {
    background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    margin: 1rem !important;
    box-shadow: 
        0 10px 40px rgba(0,0,0,0.3),
        inset 0 1px 0 rgba(255,255,255,0.1) !important;
    border: 1px solid #404040 !important;
}

/* ⚡ SIDEBAR - Thème classique avec éléments visibles */
[data-testid="stSidebar"] {
    background: white !important;
    color: #262730 !important;
}

/* 🔧 WIDGETS SIDEBAR - Styles pour visibilité */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: white !important;
    color: #262730 !important;
    border: 1px solid #d1d5db !important;
}

[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: white !important;
    color: #262730 !important;
    border: 1px solid #d1d5db !important;
}

[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: white !important;
    color: #262730 !important;
    border: 1px solid #d1d5db !important;
}

/* Options des multiselect visibles */
[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] {
    background: white !important;
    color: #262730 !important;
}

[data-testid="stSidebar"] .stMultiSelect div[role="listbox"] {
    background: white !important;
    color: #262730 !important;
}

[data-testid="stSidebar"] .stMultiSelect div[role="option"] {
    background: white !important;
    color: #262730 !important;
}

/* Texte des labels et options */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #262730 !important;
}

/* Checkbox styling */
[data-testid="stSidebar"] .stCheckbox {
    color: #262730 !important;
}

/* Slider styling */
[data-testid="stSidebar"] .stSlider {
    color: #262730 !important;
}

/* 🎯 MULTISELECT - Styles ultra-spécifiques pour visibilité */
[data-testid="stSidebar"] .stMultiSelect > div > div > div {
    background: white !important;
    color: #262730 !important;
}

[data-testid="stSidebar"] .stMultiSelect span {
    color: #262730 !important;
}

/* Dropdown menu background */
[data-testid="stSidebar"] div[data-baseweb="popover"] {
    background: white !important;
}

[data-testid="stSidebar"] div[data-baseweb="popover"] * {
    background: white !important;
    color: #262730 !important;
}

/* Selected items in multiselect */
[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="tag"] {
    background: #e2e8f0 !important;
    color: #262730 !important;
    border: 1px solid #cbd5e1 !important;
}

/* Input placeholder text */
[data-testid="stSidebar"] input::placeholder {
    color: #9ca3af !important;
}

/* Focus states */
[data-testid="stSidebar"] input:focus,
[data-testid="stSidebar"] select:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 1px #667eea !important;
}

/* 🌙 FOND NOIR - Approche ULTRA-AGRESSIVE */
html, body {
    background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%) !important;
}

.stApp {
    background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%) !important;
}

/* Zone principale avec fond noir garanti */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%) !important;
}

/* Conteneur principal */
.main .block-container {
    background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    margin: 1rem !important;
    box-shadow: 
        0 10px 40px rgba(0,0,0,0.3),
        inset 0 1px 0 rgba(255,255,255,0.1) !important;
    border: 1px solid #404040 !important;
}

/* Forcer sur TOUS les éléments principaux */
[data-testid="stAppViewContainer"] > div,
[data-testid="stAppViewContainer"] > div > div:not([data-testid="stSidebar"]),
.main,
section.main {
    background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%) !important;
}

/* Texte blanc partout dans la zone principale */
.main h1, .main h2, .main h3, .main h4, .main p, .main div, .main span {
    color: white !important;
}

/* Titres normaux et lisibles */
.main h1 {
    color: #ffffff !important;
    font-weight: 700 !important;
}

.main h2 {
    color: #ffffff !important;
    font-weight: 600 !important;
}

.main h3 {
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* 📋 EXPANDEUR - Design moderne et lisible avec fond contrasté */
.main [data-testid="stExpander"] {
    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.98) 100%) !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 15px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
    margin: 1rem 0 !important;
}

.main [data-testid="stExpander"] summary {
    color: #1a202c !important;
    font-weight: 700 !important;
    font-size: 1.2rem !important;
    padding: 1rem !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

.main [data-testid="stExpander"] div {
    color: #2d3748 !important;
    background: rgba(255,255,255,0.9) !important;
    padding: 1.5rem !important;
    border-radius: 0 0 15px 15px !important;
    line-height: 1.6 !important;
}

/* FORCER le texte NOIR dans TOUT l'expandeur pour lisibilité */
.main [data-testid="stExpander"] p,
.main [data-testid="stExpander"] strong,
.main [data-testid="stExpander"] div,
.main [data-testid="stExpander"] span,
.main [data-testid="stExpander"] h1,
.main [data-testid="stExpander"] h2,
.main [data-testid="stExpander"] h3,
.main [data-testid="stExpander"] h4,
.main [data-testid="stExpander"] li,
.main [data-testid="stExpander"] ul {
    color: #2d3748 !important;
    font-weight: 500 !important;
}

/* Titres dans l'expandeur en couleur */
.main [data-testid="stExpander"] h3 {
    color: #667eea !important;
    font-weight: 700 !important;
    margin: 1rem 0 0.5rem 0 !important;
}

/* Strong elements en bleu */
.main [data-testid="stExpander"] strong {
    color: #667eea !important;
    font-weight: 700 !important;
}

/* Markdown dans l'expandeur */
.main [data-testid="stExpander"] [data-testid="stMarkdown"] {
    color: #2d3748 !important;
}

.main [data-testid="stExpander"] [data-testid="stMarkdown"] * {
    color: #2d3748 !important;
}

/* Colonnes adaptées au fond noir */
.main [data-testid="column"] {
    background: linear-gradient(145deg, #2a2a2a 0%, #3a3a3a 100%) !important;
    border: 1px solid #505050 !important;
}

/* Cards ultra-contrastées - FORCÉES pour persister lors du filtrage */
.main .kpi-card,
[data-testid="stAppViewContainer"] .kpi-card,
.stApp .kpi-card,
div[class*="kpi-card"] {
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%) !important;
    box-shadow: 
        0 8px 30px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(255,255,255,0.9) !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 20px !important;
    padding: 2rem 1.5rem !important;
    margin: 1rem 0.5rem !important;
    min-height: 160px !important;
    position: relative !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    text-align: center !important;
    overflow: hidden !important;
    color: #1e293b !important;
}

/* 🎨 SIDEBAR - Titres en noir pour lisibilité */
[data-testid="stSidebar"] h2 {
    color: #1a1a1a !important;
    font-weight: 700 !important;
    text-shadow: none !important;
    border-bottom: 2px solid #667eea !important;
}

/* 🔄 Bouton Vider le Cache - Simple et efficace */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
}


/* Force refresh styles after filtering - CLOUD FIX */
[data-testid="stAppViewContainer"].filtered {
    animation: refreshStyles 0.1s ease-in-out;
}

@keyframes refreshStyles {
    0% { opacity: 0.99; }
    100% { opacity: 1; }
}
</style>

<script>
// 🌙 Force l'arrière-plan noir après chargement
setTimeout(function() {
    // Appliquer l'arrière-plan noir à tous les éléments principaux
    const elements = [
        document.querySelector('.stApp'),
        document.querySelector('[data-testid="stAppViewContainer"]'),
        document.querySelector('.main'),
        document.body,
        document.documentElement
    ];
    
    elements.forEach(el => {
        if (el && !el.closest('[data-testid="stSidebar"]')) {
            el.style.background = 'linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%)';
            el.style.backgroundColor = '#1a1a1a';
        }
    });
    
    // Forcer la sidebar en blanc et les éléments visibles
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        sidebar.style.background = 'white';
        sidebar.style.backgroundColor = 'white';
        sidebar.style.color = '#262730';
        
        // Forcer tous les éléments de la sidebar à être visibles
        const sidebarElements = sidebar.querySelectorAll('*');
        sidebarElements.forEach(el => {
            if (!el.style.color || el.style.color === 'white' || el.style.color === '#ffffff') {
                el.style.color = '#262730';
            }
            if (el.tagName === 'INPUT' || el.tagName === 'SELECT') {
                el.style.backgroundColor = 'white';
                el.style.color = '#262730';
                el.style.border = '1px solid #d1d5db';
            }
        });
    }
    
    // 📊 FORCER LE CENTRAGE DES TABLEAUX
    function centerTableColumns() {
        const tables = document.querySelectorAll('[data-testid="stDataFrame"] table');
        tables.forEach(table => {
            const rows = table.querySelectorAll('tr');
            rows.forEach(row => {
                const cells = row.querySelectorAll('td, th');
                cells.forEach((cell, index) => {
                    if (index > 0) { // Toutes les colonnes sauf la première
                        cell.style.textAlign = 'center';
                        cell.style.fontWeight = '600';
                    } else { // Première colonne à gauche
                        cell.style.textAlign = 'left';
                        cell.style.fontWeight = '600';
                        cell.style.paddingLeft = '1rem';
                    }
                });
            });
        });
    }
    
    // Centrer immédiatement et après chaque changement
    centerTableColumns();
    
    // Observer les changements dans les tableaux
    const tableObserver = new MutationObserver(function(mutations) {
        let shouldCenter = false;
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && 
                (mutation.target.closest('[data-testid="stDataFrame"]') || 
                 mutation.target.querySelector('[data-testid="stDataFrame"]'))) {
                shouldCenter = true;
            }
        });
        if (shouldCenter) {
            setTimeout(centerTableColumns, 50);
        }
    });
    
    // Observer tout le conteneur principal
    const mainContainer = document.querySelector('[data-testid="stAppViewContainer"]');
    if (mainContainer) {
        tableObserver.observe(mainContainer, {
            childList: true,
            subtree: true
        });
    }
}, 100);
</script>

""", unsafe_allow_html=True)

# Cache intelligent avec session_state pour éviter les rechargements
def load_data_background(nrows=None):
    """🚀 Charge les données PHMEV en arrière-plan (cache désactivé pour éviter les erreurs mémoire)"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # UNIQUEMENT le fichier sample_10k (contient les 3,504,612 lignes)
    parquet_sample_path = os.path.join(script_dir, 'OPEN_PHMEV_2024_sample_10k.parquet')
    
    # Utiliser UNIQUEMENT OPEN_PHMEV_2024_sample_10k.parquet
    if os.path.exists(parquet_sample_path):
        try:
            df = pd.read_parquet(parquet_sample_path, engine='pyarrow')
            return df
        except Exception as e:
            st.error(f"❌ Erreur avec OPEN_PHMEV_2024_sample_10k.parquet: {e}")
            return None
    
    # Si le fichier n'existe pas, erreur
    else:
        st.error("❌ Fichier OPEN_PHMEV_2024_sample_10k.parquet non trouvé !")
        st.info("💡 Veuillez vous assurer que le fichier OPEN_PHMEV_2024_sample_10k.parquet est présent dans le répertoire.")
        return None
        try:
            import pyarrow.parquet as pq
            df = pd.read_parquet(parquet_path, engine='pyarrow')
            
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
            st.error("❌ Impossible de charger les données. Veuillez ajouter le fichier OPEN_PHMEV_2024_sample_10k.parquet")
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
        
        # UNIQUEMENT le fichier sample_10k (contient les 3,504,612 lignes)
        parquet_sample_path = os.path.join(script_dir, 'OPEN_PHMEV_2024_sample_10k.parquet')
        
        # Utiliser UNIQUEMENT OPEN_PHMEV_2024_sample_10k.parquet
        if os.path.exists(parquet_sample_path):
            status_text.text("🚀 Chargement des 3,504,612 lignes...")
            progress_bar.progress(70)
            try:
                df = pd.read_parquet(parquet_sample_path, engine='pyarrow')
                progress_bar.progress(100)
                status_text.text("✅ Données chargées avec succès !")
                
                # Nettoyage interface
                import time, gc
                time.sleep(0.5)
                progress_bar.empty()
                status_text.empty()
                gc.collect()
                
                st.session_state.phmev_data_cached = df
                return df
            except Exception as e:
                st.error(f"❌ Erreur avec OPEN_PHMEV_2024_sample_10k.parquet: {e}")
                progress_bar.empty()
                status_text.empty()
                return None
        
        # Si le fichier n'existe pas, erreur
        else:
            progress_bar.empty()
            status_text.empty()
            st.error("❌ Fichier OPEN_PHMEV_2024_sample_10k.parquet non trouvé !")
            st.info("💡 Veuillez vous assurer que le fichier OPEN_PHMEV_2024_sample_10k.parquet est présent dans le répertoire.")
            return None
        
        # En local, essayer d'abord le format Parquet
        if os.path.exists(parquet_path):
            status_text.text("🚀 Chargement ultra-rapide depuis Parquet...")
            progress_bar.progress(50)
            try:
                import pyarrow.parquet as pq
                df = pd.read_parquet(parquet_path, engine='pyarrow')
                
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
                st.error("❌ Impossible de charger les données. Veuillez ajouter le fichier OPEN_PHMEV_2024_sample_10k.parquet")
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

def get_filtered_dataframe(df, current_filters):
    """🔄 Applique tous les filtres actuels et retourne le DataFrame filtré"""
    df_filtered = df
    
    # Filtres ATC hiérarchiques
    if current_filters.get('atc1_filtre'):
        df_filtered = df_filtered[df_filtered['l_atc1'].isin(current_filters['atc1_filtre'])]
    if current_filters.get('atc2_filtre'):
        df_filtered = df_filtered[df_filtered['L_ATC2'].isin(current_filters['atc2_filtre'])]
    if current_filters.get('atc3_filtre'):
        df_filtered = df_filtered[df_filtered['L_ATC3'].isin(current_filters['atc3_filtre'])]
    if current_filters.get('atc4_filtre'):
        df_filtered = df_filtered[df_filtered['L_ATC4'].isin(current_filters['atc4_filtre'])]
    if current_filters.get('atc5_filtre'):
        df_filtered = df_filtered[df_filtered['L_ATC5'].isin(current_filters['atc5_filtre'])]
    
    # Filtres CIP/Médicaments
    if current_filters.get('libelle_filtre'):
        df_filtered = df_filtered[df_filtered['libelle_cip'].isin(current_filters['libelle_filtre'])]
    
    # Filtres géographiques et organisationnels
    if current_filters.get('ville_filtre'):
        df_filtered = df_filtered[df_filtered['ville'].isin(current_filters['ville_filtre'])]
    if current_filters.get('categorie_filtre'):
        df_filtered = df_filtered[df_filtered['categorie'].isin(current_filters['categorie_filtre'])]
    if current_filters.get('etablissement_filtre'):
        df_filtered = df_filtered[df_filtered['etablissement'].isin(current_filters['etablissement_filtre'])]
    
    return df_filtered

def get_available_options(df_filtered, filter_type):
    """📊 Retourne les options disponibles pour un type de filtre donné"""
    if filter_type == 'atc1':
        return sorted(df_filtered[['atc1', 'l_atc1']].drop_duplicates().set_index('atc1')['l_atc1'].dropna().to_dict().items())
    elif filter_type == 'atc2':
        return sorted(df_filtered[['atc2', 'L_ATC2']].drop_duplicates().set_index('atc2')['L_ATC2'].dropna().to_dict().items())
    elif filter_type == 'atc3':
        return sorted(df_filtered[['atc3', 'L_ATC3']].drop_duplicates().set_index('atc3')['L_ATC3'].dropna().to_dict().items())
    elif filter_type == 'atc4':
        return sorted(df_filtered[['atc4', 'L_ATC4']].drop_duplicates().set_index('atc4')['L_ATC4'].dropna().to_dict().items())
    elif filter_type == 'atc5':
        return sorted(df_filtered[['ATC5', 'L_ATC5']].drop_duplicates().set_index('ATC5')['L_ATC5'].dropna().to_dict().items())
    elif filter_type == 'etablissements':
        return sorted(df_filtered['etablissement'].dropna().unique().tolist())
    elif filter_type == 'villes':
        return sorted(df_filtered['ville'].dropna().unique().tolist())
    elif filter_type == 'categories':
        return sorted(df_filtered['categorie'].dropna().unique().tolist())
    elif filter_type == 'medicaments':
        return sorted([x for x in df_filtered['libelle_cip'].dropna().unique() if x not in ['Non restitué', 'Honoraires de dispensation']])
    else:
        return []

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
                with st.spinner("🚀 Chargement initial des données optimisées..."):
                    df = load_data_background()
                    if df is not None:
                        st.session_state.phmev_data_cached = df
            st.session_state.data_preloaded = True
        except Exception as e:
            st.warning(f"⚠️ Chargement différé : {e}")
            st.session_state.data_preloaded = True

def force_dark_theme():
    """Pas de thème - Streamlit par défaut"""
    pass

def main():
    # Forcer le thème sombre
    force_dark_theme()
    
    # Interface de configuration
    st.sidebar.markdown("## ⚙️ **Configuration**")
    
    # Option pour activer/désactiver le pré-chargement
    auto_preload = st.sidebar.checkbox(
        "🚀 Pré-chargement automatique", 
        value=True, 
        key="auto_preload_checkbox",
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
    
    
    # 🚀 Pré-calcul ultra-rapide de TOUS les filtres
    filter_options = get_all_filter_options(df)
    
    # 🎛️ Sidebar ultra moderne avec filtres interdépendants
    with st.sidebar:
        st.markdown("## ⚡ **Filtres Interdépendants**")
        st.markdown("*Chaque sélection met à jour les autres filtres automatiquement*")
        
        # 🔄 SYSTÈME DE FILTRES INTERDÉPENDANTS
        # Logique: ATC → Médicaments → Villes → Établissements
        
        # Initialiser les filtres actuels
        current_filters = {}
        
        # ========== HIÉRARCHIE PHARMACEUTIQUE D'ABORD ==========
        st.markdown("### 💊 **Hiérarchie Pharmaceutique (QUOI)**")
        st.markdown("*Sélectionnez d'abord les médicaments qui vous intéressent*")
        
        # Niveau 1: ATC1
        st.markdown("#### 🧬 **Systèmes Anatomiques (ATC1)**")
        df_temp = get_filtered_dataframe(df, current_filters)
        atc1_options = get_available_options(df_temp, 'atc1')
        atc1_display = [f"{code} - {libelle}" for code, libelle in atc1_options]
        
        atc1_selection = st.multiselect(
            f"Systèmes anatomiques ({len(atc1_options)} disponibles)",
            options=atc1_display,
            default=[],
            key="atc1_multiselect_interdep"
        )
        
        atc1_codes = [sel.split(' - ')[0] for sel in atc1_selection] if atc1_selection else []
        atc1_filtre = [dict(atc1_options)[code] for code in atc1_codes] if atc1_codes else []
        current_filters['atc1_filtre'] = atc1_filtre
        
        # Niveau 2: ATC2 (Groupes thérapeutiques)
        st.markdown("#### 💉 **Groupes Thérapeutiques (ATC2)**")
        df_temp = get_filtered_dataframe(df, current_filters)
        atc2_options = get_available_options(df_temp, 'atc2')
        atc2_display = [f"{code} - {libelle}" for code, libelle in atc2_options]
        
        if atc2_options:
            atc2_selection = st.multiselect(
                f"Groupes thérapeutiques ({len(atc2_options)} disponibles)",
                options=atc2_display,
                default=[],
                key="atc2_multiselect_interdep"
            )
            
            atc2_codes = [sel.split(' - ')[0] for sel in atc2_selection] if atc2_selection else []
            atc2_filtre = [dict(atc2_options)[code] for code in atc2_codes] if atc2_codes else []
        else:
            atc2_filtre = []
            st.info("👆 Sélectionnez d'abord des filtres pour voir les groupes thérapeutiques")
        
        current_filters['atc2_filtre'] = atc2_filtre
        
        # Niveau 3: ATC3 (Sous-groupes pharmacologiques)
        st.markdown("#### 🔬 **Sous-groupes Pharmacologiques (ATC3)**")
        df_temp = get_filtered_dataframe(df, current_filters)
        atc3_options = get_available_options(df_temp, 'atc3')
        atc3_display = [f"{code} - {libelle}" for code, libelle in atc3_options]
        
        if atc3_options:
            atc3_selection = st.multiselect(
                f"Sous-groupes pharmacologiques ({len(atc3_options)} disponibles)",
                options=atc3_display,
                default=[],
                key="atc3_multiselect_interdep"
            )
            
            atc3_codes = [sel.split(' - ')[0] for sel in atc3_selection] if atc3_selection else []
            atc3_filtre = [dict(atc3_options)[code] for code in atc3_codes] if atc3_codes else []
        else:
            atc3_filtre = []
            if current_filters.get('atc2_filtre'):
                st.info("👆 Affinez vos sélections pour voir les sous-groupes")
        
        current_filters['atc3_filtre'] = atc3_filtre
        
        # Niveau 4: ATC4 (Groupes chimiques)
        st.markdown("#### ⚗️ **Groupes Chimiques (ATC4)**")
        df_temp = get_filtered_dataframe(df, current_filters)
        atc4_options = get_available_options(df_temp, 'atc4')
        atc4_display = [f"{code} - {libelle}" for code, libelle in atc4_options]
        
        if atc4_options:
            atc4_selection = st.multiselect(
                f"Groupes chimiques ({len(atc4_options)} disponibles)",
                options=atc4_display,
                default=[],
                key="atc4_multiselect_interdep"
            )
            
            atc4_codes = [sel.split(' - ')[0] for sel in atc4_selection] if atc4_selection else []
            atc4_filtre = [dict(atc4_options)[code] for code in atc4_codes] if atc4_codes else []
        else:
            atc4_filtre = []
        
        current_filters['atc4_filtre'] = atc4_filtre
        
        # Niveau 5: ATC5 (Substances chimiques)
        st.markdown("#### 🧪 **Substances Chimiques (ATC5)**")
        df_temp = get_filtered_dataframe(df, current_filters)
        atc5_options = get_available_options(df_temp, 'atc5')
        atc5_display = [f"{code} - {libelle}" for code, libelle in atc5_options]
        
        if atc5_options:
            atc5_selection = st.multiselect(
                f"Substances chimiques ({len(atc5_options)} disponibles)",
                options=atc5_display,
                default=[],
                key="atc5_multiselect_interdep"
            )
            
            atc5_codes = [sel.split(' - ')[0] for sel in atc5_selection] if atc5_selection else []
            atc5_filtre = [dict(atc5_options)[code] for code in atc5_codes] if atc5_codes else []
        else:
            atc5_filtre = []
        
        current_filters['atc5_filtre'] = atc5_filtre
        
        # Médicaments spécifiques
        st.markdown("#### 💊 **Médicaments Spécifiques**")
        df_temp = get_filtered_dataframe(df, current_filters)
        medicaments_disponibles = get_available_options(df_temp, 'medicaments')
        
        libelle_search = st.text_input(
            "🔍 Rechercher un médicament",
            placeholder="Ex: cabometyx, doliprane, ventoline...",
            key="libelle_search_interdep"
        )
        
        if libelle_search:
            medicaments_filtered = [m for m in medicaments_disponibles if libelle_search.lower() in m.lower()][:50]
        else:
            medicaments_filtered = medicaments_disponibles[:50]
        
        if medicaments_filtered:
            libelle_filtre = st.multiselect(
                f"Médicaments ({len(medicaments_disponibles)} disponibles)",
                options=medicaments_filtered,
                default=[],
                key="libelle_multiselect_interdep"
            )
        else:
            libelle_filtre = []
            st.info("👆 Aucun médicament disponible pour cette sélection")
        
        current_filters['libelle_filtre'] = libelle_filtre
        
        st.markdown("---")
        
        # ========== FILTRES GÉOGRAPHIQUES (OÙ) ==========
        st.markdown("### 🌍 **Localisation Géographique (OÙ)**")
        st.markdown("*Filtrez par localisation selon les médicaments sélectionnés*")
        
        # Villes (filtrées selon les médicaments sélectionnés)
        st.markdown("#### 🏙️ **Villes**")
        df_temp = get_filtered_dataframe(df, current_filters)
        villes_disponibles = get_available_options(df_temp, 'villes')
        
        ville_search = st.text_input(
            "🔍 Rechercher une ville",
            placeholder="Tapez pour filtrer les villes...",
            key="ville_search_interdep"
        )
        
        if ville_search:
            villes_filtered = [v for v in villes_disponibles if ville_search.lower() in v.lower()][:50]
        else:
            villes_filtered = villes_disponibles[:50]
        
        ville_filtre = st.multiselect(
            f"Sélectionner les villes ({len(villes_disponibles)} disponibles)",
            options=villes_filtered,
            default=[],
            key="ville_multiselect_interdep"
        )
        current_filters['ville_filtre'] = ville_filtre
        
        st.markdown("---")
        
        # ========== FILTRES ORGANISATIONNELS (QUI) ==========
        st.markdown("### 🏥 **Établissements de Santé (QUI)**")
        st.markdown("*Filtrez par établissement selon médicaments et villes sélectionnés*")
        
        # Catégories d'établissements
        st.markdown("#### 🏛️ **Types d'Établissements**")
        df_temp = get_filtered_dataframe(df, current_filters)
        categories_disponibles = get_available_options(df_temp, 'categories')
        
        categorie_filtre = st.multiselect(
            f"Types d'établissement ({len(categories_disponibles)} disponibles)",
            options=categories_disponibles,
            default=[],
            key="categorie_multiselect_interdep"
        )
        current_filters['categorie_filtre'] = categorie_filtre
        
        # Établissements spécifiques
        st.markdown("#### 🏥 **Établissements Spécifiques**")
        df_temp = get_filtered_dataframe(df, current_filters)
        etablissements_disponibles = get_available_options(df_temp, 'etablissements')
        
        etablissement_search = st.text_input(
            "🔍 Rechercher un établissement",
            placeholder="Tapez pour filtrer les établissements...",
            key="etablissement_search_interdep"
        )
        
        if etablissement_search:
            etablissements_filtered = [e for e in etablissements_disponibles if etablissement_search.lower() in e.lower()][:50]
        else:
            etablissements_filtered = etablissements_disponibles[:50]
        
        etablissement_filtre = st.multiselect(
            f"Sélectionner les établissements ({len(etablissements_disponibles)} disponibles)",
            options=etablissements_filtered,
            default=[],
            key="etablissement_multiselect_interdep"
        )
        current_filters['etablissement_filtre'] = etablissement_filtre
        
        st.markdown("---")
        
        # ========== PARAMÈTRES D'ANALYSE ==========
        
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
    
    # 🔧 Application des filtres interdépendants
    df_filtered = get_filtered_dataframe(df, current_filters)
    
    # Appliquer le filtre de boîtes minimum
    if min_boites > 0:
        df_filtered = df_filtered[df_filtered['BOITES'] >= min_boites]
    
    # 📊 Indicateur de filtrage actif avec nouveau système
    filters_active = []
    if current_filters.get('ville_filtre'): filters_active.append(f"Villes: {len(current_filters['ville_filtre'])}")
    if current_filters.get('categorie_filtre'): filters_active.append(f"Catégories: {len(current_filters['categorie_filtre'])}")
    if current_filters.get('etablissement_filtre'): filters_active.append(f"Établissements: {len(current_filters['etablissement_filtre'])}")
    if current_filters.get('atc1_filtre'): filters_active.append(f"ATC1: {len(current_filters['atc1_filtre'])}")
    if current_filters.get('atc2_filtre'): filters_active.append(f"ATC2: {len(current_filters['atc2_filtre'])}")
    if current_filters.get('atc3_filtre'): filters_active.append(f"ATC3: {len(current_filters['atc3_filtre'])}")
    if current_filters.get('atc4_filtre'): filters_active.append(f"ATC4: {len(current_filters['atc4_filtre'])}")
    if current_filters.get('atc5_filtre'): filters_active.append(f"ATC5: {len(current_filters['atc5_filtre'])}")
    if current_filters.get('libelle_filtre'): filters_active.append(f"Médicaments: {len(current_filters['libelle_filtre'])}")
    
    # 📊 Informations sur le dataset (toujours visible)
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
    
    # Affichage des filtres actifs seulement s'il y en a
    if filters_active:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1.5rem; border-radius: 15px; 
                    margin: 1rem 0; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                    border: 2px solid rgba(255,255,255,0.2);">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <span style="font-size: 2rem;">🎯</span>
                <div>
                    <h3 style="margin: 0; font-size: 1.3rem; font-weight: 700;">FILTRES ACTIFS</h3>
                    <div style="font-size: 1rem; opacity: 0.9; margin-top: 0.3rem;">
                        {" | ".join(filters_active)}
                    </div>
                </div>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.5rem;">📊</span>
                        <div>
                            <div style="font-size: 1.8rem; font-weight: 700;">
                                {len(df_filtered):,}
                            </div>
                            <div style="font-size: 0.9rem; opacity: 0.8;">
                                Lignes filtrées
                            </div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.5rem;">📈</span>
                        <div>
                            <div style="font-size: 1.8rem; font-weight: 700;">
                                {len(df_filtered)/len(df)*100:.1f}%
                            </div>
                            <div style="font-size: 0.9rem; opacity: 0.8;">
                                du dataset total
                            </div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.5rem;">🗂️</span>
                        <div>
                            <div style="font-size: 1.8rem; font-weight: 700;">
                                3,504,612 lignes
                            </div>
                            <div style="font-size: 0.9rem; opacity: 0.8;">
                                Dataset analysé
                            </div>
                        </div>
                    </div>
                </div>
            </div>
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
    if any([current_filters.get('atc1_filtre'), current_filters.get('atc2_filtre'), 
            current_filters.get('atc3_filtre'), current_filters.get('atc4_filtre'), 
            current_filters.get('atc5_filtre')]):
        if current_filters.get('atc5_filtre') and 'L_ATC5' in df_top.columns:
            df_display_data['L_ATC5'] = df_top['L_ATC5'].tolist()
        elif current_filters.get('atc4_filtre') and 'L_ATC4' in df_top.columns:
            df_display_data['L_ATC4'] = df_top['L_ATC4'].tolist()
        elif current_filters.get('atc3_filtre') and 'L_ATC3' in df_top.columns:
            df_display_data['L_ATC3'] = df_top['L_ATC3'].tolist()
        elif current_filters.get('atc2_filtre') and 'L_ATC2' in df_top.columns:
            df_display_data['L_ATC2'] = df_top['L_ATC2'].tolist()
        elif current_filters.get('atc1_filtre') and 'l_atc1' in df_top.columns:
            df_display_data['l_atc1'] = df_top['l_atc1'].tolist()
    
    # Ajouter les colonnes CIP si filtrées
    if current_filters.get('libelle_filtre') and 'libelle_cip' in df_top.columns:
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
        st.markdown('## 💊 Top Produits des Établissements Sélectionnés')
        
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
    
    # Section "📊 Systèmes Thérapeutiques Sélectionnés" supprimée sur demande utilisateur
    
    # 📋 Analyse des codes CIP si filtrés
    if current_filters.get('libelle_filtre'):
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
        - **Source:** OPEN_PHMEV_2024_sample_10k.parquet
        
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
