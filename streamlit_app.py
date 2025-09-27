"""
🏥 PHMEV Analytics Pro - Version Finale BigQuery
Tous les filtres hiérarchiques + TOP N optimisé + Performance maximale
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

# Configuration de la page
st.set_page_config(
    page_title="🏥 PHMEV Analytics Pro",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS thème mixte élégant
st.markdown("""
<style>
/* Arrière-plan principal sombre pour tout le contenu */
.main .block-container {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    padding: 2rem;
    border-radius: 20px;
    margin: 10px;
    min-height: calc(100vh - 20px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}

/* Arrière-plan de la page entière */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Header avec dégradé élégant */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
}

/* KPI Cards avec thème clair */
.kpi-container {
    background: linear-gradient(135deg, #ffffff 0%, #e8f4fd 100%);
    padding: 1.5rem;
    border-radius: 20px;
    border-left: 6px solid #667eea;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin: 1rem 0;
    transition: all 0.3s ease;
}

.kpi-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.2);
}

.kpi-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: #4a5568;
    margin: 0;
}

.kpi-label {
    color: #718096;
    font-size: 1rem;
    margin-top: 0.5rem;
    font-weight: 500;
}

/* Tableaux avec style transparent */
[data-testid="stDataFrame"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stDataFrame"] th {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    font-weight: bold !important;
    border: none !important;
    padding: 15px !important;
}

[data-testid="stDataFrame"] td {
    background: transparent !important;
    color: white !important;
    border: none !important;
    padding: 12px 15px !important;
}

[data-testid="stDataFrame"] tr:nth-child(even) td {
    background: rgba(255,255,255,0.05) !important;
}

[data-testid="stDataFrame"] tr:hover td {
    background: rgba(102, 126, 234, 0.2) !important;
    transition: all 0.2s ease;
}

/* Onglets avec style transparent */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 8px;
}

.stTabs [data-baseweb="tab"] {
    color: #a0a0a0;
    background-color: transparent;
    border-radius: 12px;
    font-weight: 600;
    padding: 12px 20px;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(102, 126, 234, 0.2);
    color: #667eea;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    transform: translateY(-2px);
}

/* Métriques Streamlit avec thème clair */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%);
    border: 2px solid #e2e8f0;
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    border-color: #667eea;
}

/* Couleurs pour les valeurs des métriques */
[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #4a5568 !important;
    font-weight: bold !important;
}

[data-testid="metric-container"] [data-testid="metric-delta"] {
    color: #38a169 !important;
}


/* Tous les textes en blanc dans la zone principale */
.main .block-container h1,
.main .block-container h2, 
.main .block-container h3,
.main .block-container h4,
.main .block-container h5,
.main .block-container h6,
.main .block-container p,
.main .block-container div,
.main .block-container span,
.main .block-container .stMarkdown {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Fonctions utilitaires
def format_number(value):
    if pd.isna(value) or value == 0:
        return "0"
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.0f}K"
    else:
        return f"{value:.0f}"

def format_currency(value):
    if pd.isna(value) or value == 0:
        return "0,00€"
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M€"
    elif value >= 1_000:
        return f"{value/1_000:.0f}K€"
    else:
        return f"{value:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.')

# Configuration BigQuery
@st.cache_resource
def init_bigquery():
    """Initialise BigQuery avec gestion d'erreurs robuste"""
    try:
        # Priorité 1: Utiliser les secrets Streamlit Cloud
        if "gcp_service_account" in st.secrets:
            try:
                credentials_info = dict(st.secrets["gcp_service_account"])
                credentials = service_account.Credentials.from_service_account_info(credentials_info)
                client = bigquery.Client(credentials=credentials, project=credentials_info["project_id"])
                # Test rapide de connexion
                client.query("SELECT 1").result()
                return client, credentials_info["project_id"]
            except Exception as e:
                pass  # Silencieux
        
        # Priorité 2: Fichier local (développement)
        import os
        json_file = 'test-db-473321-aed58eeb55a8.json'
        if os.path.exists(json_file):
            try:
                credentials = service_account.Credentials.from_service_account_file(json_file)
                client = bigquery.Client(credentials=credentials, project='test-db-473321')
                # Test rapide de connexion
                client.query("SELECT 1").result()
                pass  # Connexion réussie silencieusement
                return client, 'test-db-473321'
            except Exception as e:
                pass  # Silencieux
        
        # Priorité 3: Authentification par défaut Google Cloud
        try:
            client = bigquery.Client(project='test-db-473321')
            # Test rapide de connexion
            client.query("SELECT 1").result()
            pass  # Connexion réussie silencieusement
            return client, 'test-db-473321'
        except Exception as e:
            pass  # Silencieux
        
        # Fallback silencieux
        return None, None
        
    except Exception as e:
        # Erreur silencieuse pour éviter de casser l'interface
        return None, None

@st.cache_data(ttl=86400)  # Cache 24 heures
def get_base_filter_options():
    """Récupère les options de base depuis le cache (ultra-rapide)"""
    import pickle
    import json
    import os
    from datetime import datetime, timedelta
    
    try:
        # PRIORITÉ 1: Cache intégré (pour Streamlit Cloud)
        try:
            from filter_cache_embedded import get_embedded_cache
            options = get_embedded_cache()
            return options
        except ImportError:
            pass
        
        # PRIORITÉ 2: Cache pickle local (pour développement local)
        cache_file = 'filter_options_cache.pkl'
        if os.path.exists(cache_file):
            cache_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_file))
            if cache_age < timedelta(hours=24):
                with open(cache_file, 'rb') as f:
                    options = pickle.load(f)
                return options
        
        # PRIORITÉ 3: Cache JSON local
        json_file = 'filter_options_cache.json'
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                options = json.load(f)
            return options
        
        # FALLBACK: BigQuery (silencieux)
        return get_base_filter_options_from_bigquery()
        
    except Exception as e:
        # Erreur silencieuse, fallback automatique
        return get_base_filter_options_from_bigquery()

def get_base_filter_options_from_bigquery():
    """Fallback : récupère les options depuis BigQuery"""
    client, project_id = init_bigquery()
    if not client:
        return {}
    
    try:
        query = f"""
        SELECT DISTINCT
            atc1, l_atc1,
            atc2, L_ATC2,
            atc3, L_ATC3,
            atc4, L_ATC4,
            ATC5, L_ATC5,
            COALESCE(NULLIF(nom_ville, ''), 'Non spécifiée') as ville,
            COALESCE(NULLIF(categorie_jur, ''), 'Non spécifiée') as categorie,
            COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié') as etablissement,
            COALESCE(NULLIF(l_cip13, ''), 'Non spécifié') as medicament
        FROM `{project_id}.dataset.PHMEV2024`
        WHERE l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')
        AND l_cip13 IS NOT NULL
        """
        
        df = client.query(query).to_dataframe()
        
        options = {}
        if 'atc1' in df.columns:
            options['atc1'] = sorted([(row['atc1'], row['l_atc1']) for _, row in df[['atc1', 'l_atc1']].dropna().drop_duplicates().iterrows()])
        if 'atc2' in df.columns:
            options['atc2'] = sorted([(row['atc2'], row['L_ATC2']) for _, row in df[['atc2', 'L_ATC2']].dropna().drop_duplicates().iterrows()])
        if 'atc3' in df.columns:
            options['atc3'] = sorted([(row['atc3'], row['L_ATC3']) for _, row in df[['atc3', 'L_ATC3']].dropna().drop_duplicates().iterrows()])
        if 'atc4' in df.columns:
            options['atc4'] = sorted([(row['atc4'], row['L_ATC4']) for _, row in df[['atc4', 'L_ATC4']].dropna().drop_duplicates().iterrows()])
        if 'ATC5' in df.columns:
            options['atc5'] = sorted([(row['ATC5'], row['L_ATC5']) for _, row in df[['ATC5', 'L_ATC5']].dropna().drop_duplicates().iterrows()])
        
        options['villes'] = sorted(df['ville'].dropna().unique().tolist())
        options['categories'] = sorted(df['categorie'].dropna().unique().tolist())
        options['etablissements'] = sorted(df['etablissement'].dropna().unique().tolist())
        options['medicaments'] = sorted(df['medicament'].dropna().unique().tolist())
        
        return options
        
    except Exception as e:
        # Erreur silencieuse pour éviter l'affichage technique
        return {}

@st.cache_data(ttl=300)  # Cache 5 minutes pour les filtres dynamiques
def get_filtered_options(current_filters):
    """Récupère les options filtrées dynamiquement"""
    client, project_id = init_bigquery()
    if not client:
        return {}
    
    try:
        # Construire la clause WHERE avec les filtres actuels
        where_conditions = [
            "l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')",
            "l_cip13 IS NOT NULL"
        ]
        
        # Ajouter les filtres existants
        for level in ['atc1', 'atc2', 'atc3', 'atc4']:
            if current_filters.get(level):
                level_list = "', '".join(current_filters[level])
                where_conditions.append(f"{level} IN ('{level_list}')")
        
        if current_filters.get('atc5'):
            atc5_list = "', '".join(current_filters['atc5'])
            where_conditions.append(f"ATC5 IN ('{atc5_list}')")
        
        if current_filters.get('villes'):
            villes_list = "', '".join(current_filters['villes'])
            where_conditions.append(f"COALESCE(NULLIF(nom_ville, ''), 'Non spécifiée') IN ('{villes_list}')")
        
        if current_filters.get('categories'):
            cat_list = "', '".join(current_filters['categories'])
            where_conditions.append(f"COALESCE(NULLIF(categorie_jur, ''), 'Non spécifiée') IN ('{cat_list}')")
        
        if current_filters.get('etablissements'):
            etab_list = "', '".join(current_filters['etablissements'])
            where_conditions.append(f"COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié') IN ('{etab_list}')")
        
        where_clause = " AND ".join(where_conditions)
        
        query = f"""
        SELECT DISTINCT
            atc1, l_atc1,
            atc2, L_ATC2,
            atc3, L_ATC3,
            atc4, L_ATC4,
            ATC5, L_ATC5,
            COALESCE(NULLIF(nom_ville, ''), 'Non spécifiée') as ville,
            COALESCE(NULLIF(categorie_jur, ''), 'Non spécifiée') as categorie,
            COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié') as etablissement,
            COALESCE(NULLIF(l_cip13, ''), 'Non spécifié') as medicament
        FROM `{project_id}.dataset.PHMEV2024`
        WHERE {where_clause}
        """
        
        df = client.query(query).to_dataframe()
        
        options = {}
        if 'atc2' in df.columns:
            options['atc2'] = sorted([(row['atc2'], row['L_ATC2']) for _, row in df[['atc2', 'L_ATC2']].dropna().drop_duplicates().iterrows()])
        if 'atc3' in df.columns:
            options['atc3'] = sorted([(row['atc3'], row['L_ATC3']) for _, row in df[['atc3', 'L_ATC3']].dropna().drop_duplicates().iterrows()])
        if 'atc4' in df.columns:
            options['atc4'] = sorted([(row['atc4'], row['L_ATC4']) for _, row in df[['atc4', 'L_ATC4']].dropna().drop_duplicates().iterrows()])
        if 'ATC5' in df.columns:
            options['atc5'] = sorted([(row['ATC5'], row['L_ATC5']) for _, row in df[['ATC5', 'L_ATC5']].dropna().drop_duplicates().iterrows()])
        
        options['villes'] = sorted(df['ville'].dropna().unique().tolist())
        options['categories'] = sorted(df['categorie'].dropna().unique().tolist())
        options['etablissements'] = sorted(df['etablissement'].dropna().unique().tolist())
        options['medicaments'] = sorted(df['medicament'].dropna().unique().tolist())
        
        return options
        
    except Exception as e:
        # Erreur silencieuse, retour aux options de base
        return {}

def build_where_clause(filters):
    """Construit la clause WHERE dynamique"""
    where_conditions = [
        "l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')",
        "l_cip13 IS NOT NULL"
    ]
    
    # Filtres ATC hiérarchiques
    for level in ['atc1', 'atc2', 'atc3', 'atc4']:
        if filters.get(level):
            level_list = "', '".join(filters[level])
            where_conditions.append(f"{level} IN ('{level_list}')")
    
    if filters.get('atc5'):
        atc5_list = "', '".join(filters['atc5'])
        where_conditions.append(f"ATC5 IN ('{atc5_list}')")
    
    # Autres filtres
    if filters.get('villes'):
        villes_list = "', '".join(filters['villes'])
        where_conditions.append(f"COALESCE(NULLIF(nom_ville, ''), 'Non spécifiée') IN ('{villes_list}')")
    
    if filters.get('categories'):
        cat_list = "', '".join(filters['categories'])
        where_conditions.append(f"COALESCE(NULLIF(categorie_jur, ''), 'Non spécifiée') IN ('{cat_list}')")
    
    if filters.get('etablissements'):
        etab_list = "', '".join(filters['etablissements'])
        where_conditions.append(f"COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié') IN ('{etab_list}')")
    
    if filters.get('medicaments'):
        med_list = "', '".join(filters['medicaments'])
        where_conditions.append(f"COALESCE(NULLIF(l_cip13, ''), 'Non spécifié') IN ('{med_list}')")
    
    if filters.get('min_boites', 0) > 0:
        where_conditions.append(f"BOITES >= {filters['min_boites']}")
    
    return " AND ".join(where_conditions)

def get_kpis(filters):
    """Récupère les KPIs depuis BigQuery"""
    client, project_id = init_bigquery()
    if not client:
        return {}
    
    try:
        where_clause = build_where_clause(filters)
        query = f"""
        SELECT 
            COUNT(*) as total_lignes,
            SUM(REM) as total_rem,
            SUM(BSE) as total_bse,
            SUM(BOITES) as total_boites,
            COUNT(DISTINCT COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié')) as nb_etablissements,
            COUNT(DISTINCT COALESCE(NULLIF(l_cip13, ''), 'Non spécifié')) as nb_medicaments,
            COUNT(DISTINCT COALESCE(NULLIF(nom_ville, ''), 'Non spécifiée')) as nb_villes
        FROM `{project_id}.dataset.PHMEV2024`
        WHERE {where_clause}
        """
        
        result = client.query(query).to_dataframe()
        if len(result) > 0:
            kpis_dict = result.iloc[0].to_dict()
            # S'assurer que toutes les valeurs numériques sont valides
            for key, value in kpis_dict.items():
                if pd.isna(value) or value is None:
                    kpis_dict[key] = 0
            return kpis_dict
        return {}
    except Exception as e:
        # Erreur silencieuse pour les KPIs
        return {}

def get_top_data(table_type, filters, limit=50):
    """Récupère le TOP N pour un type de tableau"""
    client, project_id = init_bigquery()
    if not client:
        return pd.DataFrame()
    
    try:
        where_clause = build_where_clause(filters)
        
        if table_type == "etablissements":
            query = f"""
            SELECT 
                COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié') as etablissement,
                COALESCE(NULLIF(nom_ville, ''), 'Non spécifiée') as ville,
                COALESCE(NULLIF(categorie_jur, ''), 'Non spécifiée') as categorie,
                SUM(REM) as REM,
                SUM(BSE) as BSE,
                SUM(BOITES) as BOITES,
                SUM(REM) / SUM(BOITES) as cout_par_boite,
                (SUM(REM) / SUM(BSE)) * 100 as taux_remboursement
            FROM `{project_id}.dataset.PHMEV2024`
            WHERE {where_clause}
            GROUP BY etablissement, ville, categorie
            ORDER BY REM DESC
            LIMIT {limit}
            """
        
        elif table_type == "medicaments":
            query = f"""
            SELECT 
                COALESCE(NULLIF(l_cip13, ''), 'Non spécifié') as medicament,
                atc1, l_atc1,
                SUM(REM) as REM,
                SUM(BSE) as BSE,
                SUM(BOITES) as BOITES,
                COUNT(DISTINCT COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié')) as nb_etablissements,
                SUM(REM) / SUM(BOITES) as cout_par_boite,
                (SUM(REM) / SUM(BSE)) * 100 as taux_remboursement
            FROM `{project_id}.dataset.PHMEV2024`
            WHERE {where_clause}
            GROUP BY medicament, atc1, l_atc1
            ORDER BY REM DESC
            LIMIT {limit}
            """
        
        elif table_type == "molecules":
            query = f"""
            SELECT 
                COALESCE(NULLIF(L_ATC5, ''), 'Non spécifié') as molecule,
                atc1, l_atc1,
                SUM(REM) as REM,
                SUM(BSE) as BSE,
                SUM(BOITES) as BOITES,
                COUNT(DISTINCT COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié')) as nb_etablissements,
                SUM(REM) / SUM(BOITES) as cout_par_boite,
                (SUM(REM) / SUM(BSE)) * 100 as taux_remboursement
            FROM `{project_id}.dataset.PHMEV2024`
            WHERE {where_clause}
            GROUP BY molecule, atc1, l_atc1
            ORDER BY REM DESC
            LIMIT {limit}
            """
        
        return client.query(query).to_dataframe()
        
    except Exception as e:
        # Erreur silencieuse pour les données
        return pd.DataFrame()

def main():
    # En-tête
    st.markdown("""
    <div class="main-header">
        <h1>🏥 PHMEV Analytics Pro</h1>
        <p>Analyse pharmaceutique avec BigQuery - Performance maximale</p>
        <p><small>⚡ Filtres hiérarchiques + TOP N optimisé</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialiser les filtres dans session_state
    if 'filters' not in st.session_state:
        st.session_state.filters = {}
    
    # Chargement des options de base (optimisé)
    base_options = get_base_filter_options()
    
    if not base_options:
        st.warning("⚠️ Chargement des données en cours...")
        st.stop()
    
    # Test de connexion BigQuery (silencieux)
    client, project_id = init_bigquery()
    
    # Sidebar - Filtres hiérarchiques avec mise à jour automatique
    st.sidebar.header("🎛️ Filtres Hiérarchiques ⚡")
    st.sidebar.caption("🔄 Mise à jour automatique activée")
    
    filters = {}
    
    # Classification ATC hiérarchique
    st.sidebar.subheader("🧬 Classification Thérapeutique")
    
    # ATC1 (toujours disponible)
    atc1_options = base_options.get('atc1', [])
    filters['atc1'] = st.sidebar.multiselect(
        "ATC Niveau 1", 
        options=[code for code, label in atc1_options],
        format_func=lambda x: f"{x} - {dict(atc1_options).get(x, x)}",
        key="atc1_filter"
    )
    
    # Fonction pour obtenir les options filtrées de manière optimisée
    def get_current_options(current_filters):
        if any(current_filters.values()) and client:
            return get_filtered_options(current_filters)
        return base_options
    
    # Options initiales
    filtered_options = get_current_options(filters)
    
    # ATC2 (conditionnel et dynamique)
    if filters['atc1']:
        atc2_options = filtered_options.get('atc2', [])
        filters['atc2'] = st.sidebar.multiselect(
            "ATC Niveau 2", 
            options=[code for code, label in atc2_options],
            format_func=lambda x: f"{x} - {dict(atc2_options).get(x, x)}",
            key="atc2_filter"
        )
    else:
        filters['atc2'] = []
        st.sidebar.multiselect("ATC Niveau 2", [], disabled=True, help="Sélectionnez d'abord ATC Niveau 1")
    
    # Mise à jour des options si ATC2 sélectionné
    if filters.get('atc2'):
        filtered_options = get_current_options(filters)
    
    # ATC3 (conditionnel et dynamique)
    if filters.get('atc2'):
        atc3_options = filtered_options.get('atc3', [])
        filters['atc3'] = st.sidebar.multiselect(
            "ATC Niveau 3", 
            options=[code for code, label in atc3_options],
            format_func=lambda x: f"{x} - {dict(atc3_options).get(x, x)}",
            key="atc3_filter"
        )
    else:
        filters['atc3'] = []
        st.sidebar.multiselect("ATC Niveau 3", [], disabled=True, help="Sélectionnez d'abord ATC Niveau 2")
    
    # Mise à jour des options si ATC3 sélectionné
    if filters.get('atc3'):
        filtered_options = get_current_options(filters)
    
    # ATC4 (conditionnel et dynamique)
    if filters.get('atc3'):
        atc4_options = filtered_options.get('atc4', [])
        filters['atc4'] = st.sidebar.multiselect(
            "ATC Niveau 4", 
            options=[code for code, label in atc4_options],
            format_func=lambda x: f"{x} - {dict(atc4_options).get(x, x)}",
            key="atc4_filter"
        )
    else:
        filters['atc4'] = []
        st.sidebar.multiselect("ATC Niveau 4", [], disabled=True, help="Sélectionnez d'abord ATC Niveau 3")
    
    # Mise à jour des options si ATC4 sélectionné
    if filters.get('atc4'):
        filtered_options = get_current_options(filters)
    
    # ATC5 (conditionnel et dynamique)
    if filters.get('atc4'):
        atc5_options = filtered_options.get('atc5', [])
        filters['atc5'] = st.sidebar.multiselect(
            "ATC Niveau 5", 
            options=[code for code, label in atc5_options],
            format_func=lambda x: f"{x} - {dict(atc5_options).get(x, x)}",
            key="atc5_filter"
        )
    else:
        filters['atc5'] = []
        st.sidebar.multiselect("ATC Niveau 5", [], disabled=True, help="Sélectionnez d'abord ATC Niveau 4")
    
    # Mise à jour finale des options avec tous les filtres ATC
    filtered_options = get_current_options(filters)
    
    # Autres filtres dynamiques
    st.sidebar.subheader("🏥 Filtres Géographiques & Organisationnels")
    
    filters['villes'] = st.sidebar.multiselect(
        "🏙️ Villes", 
        options=filtered_options.get('villes', []),
        key="villes_filter"
    )
    
    filters['categories'] = st.sidebar.multiselect(
        "🏥 Catégories", 
        options=filtered_options.get('categories', []),
        key="categories_filter"
    )
    
    # Recherche d'établissements (similaire aux médicaments)
    st.sidebar.subheader("🏢 Recherche d'Établissements")
    search_etab = st.sidebar.text_input(
        "🔍 Rechercher un établissement", 
        placeholder="Ex: chu, clinique, hopital...",
        key="etab_search"
    )
    
    # Filtrer les établissements selon la recherche
    etab_options = filtered_options.get('etablissements', [])
    if search_etab:
        search_lower = search_etab.lower().strip()
        etab_options = [etab for etab in etab_options if search_lower in etab.lower()]
        etab_options.sort()
    
    filters['etablissements'] = st.sidebar.multiselect(
        "🏢 Établissements", 
        options=etab_options,
        help=f"{'❌ Aucun établissement trouvé pour \"' + search_etab + '\"' if search_etab and not etab_options else f'✅ {len(etab_options)} établissements disponibles'}",
        key="etablissements_filter"
    )
    
    # Recherche médicament dynamique
    st.sidebar.subheader("💊 Recherche de Médicaments")
    search_term = st.sidebar.text_input(
        "🔍 Rechercher", 
        placeholder="Ex: cabometyx, keytruda...",
        key="med_search"
    )
    
    # Mapping des noms commerciaux (maintenant on cherche directement dans l_cip13)
    drug_aliases = {
        'cabome': 'cabometyx',
        'keytr': 'keytruda', 
        'opdi': 'opdivo',
        'tecfi': 'tecfidera',
        'humi': 'humira',
        'avast': 'avastin',
        'hercep': 'herceptin'
    }
    
    # Utiliser les médicaments filtrés selon les autres critères
    med_options = filtered_options.get('medicaments', [])
    
    if search_term:
        search_lower = search_term.lower().strip()
        # Recherche directe dans les noms commerciaux
        direct_matches = [med for med in med_options if search_lower in med.lower()]
        
        # Recherche via alias (pour les abréviations)
        alias_matches = []
        for alias, full_name in drug_aliases.items():
            if search_lower.startswith(alias):
                alias_matches.extend([med for med in med_options if full_name.lower() in med.lower()])
        
        # Combiner les résultats (sans doublons)
        med_options = list(set(direct_matches + alias_matches))
        med_options.sort()
    
    filters['medicaments'] = st.sidebar.multiselect(
        "💊 Médicaments", 
        options=med_options,
        key="medicaments_filter",
        help=f"{'❌ Aucun médicament trouvé pour \"' + search_term + '\"' if search_term and not med_options else f'✅ {len(med_options)} médicaments disponibles (filtrés automatiquement)'}"
    )
    
    filters['min_boites'] = st.sidebar.number_input(
        "📦 Nombre minimum de boîtes", 
        min_value=0, 
        value=0,
        key="min_boites_filter"
    )
    
    # Indicateur de filtres actifs
    active_filters = sum(1 for v in filters.values() if v)
    if active_filters > 0:
        st.sidebar.success(f"🎯 {active_filters} filtre(s) actif(s)")
    
    # Boutons d'action
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        if st.button("🔄 Reset", width="stretch"):
            # Clear all session state keys for filters
            for key in list(st.session_state.keys()):
                if key.endswith('_filter') or key == 'med_search':
                    del st.session_state[key]
            st.rerun()
    
    with col2:
        if st.button("⚡ Actualiser", width="stretch"):
            st.cache_data.clear()
            st.rerun()
    
    with col3:
        if st.button("🔧 Cache", width="stretch", help="Régénérer le cache des filtres"):
            with st.spinner("Régénération du cache..."):
                import subprocess
                try:
                    result = subprocess.run(['python', 'generate_filter_cache.py'], 
                                          capture_output=True, text=True, timeout=120)
                    if result.returncode == 0:
                        st.success("✅ Cache mis à jour")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.warning("⚠️ Mise à jour impossible")
                except Exception as e:
                    st.warning("⚠️ Fonctionnalité temporairement indisponible")
    
    # KPIs (seulement si BigQuery disponible)
    client, project_id = init_bigquery()
    if client:
        with st.spinner("📊 Calcul des KPIs..."):
            kpis = get_kpis(filters)
    else:
        # Mode cache uniquement - KPIs non disponibles
        kpis = {}
    
    if kpis:
        # Calcul du coût par boîte avec gestion robuste des valeurs None/NaN
        total_rem = kpis.get('total_rem', 0)
        total_boites = kpis.get('total_boites', 0)
        
        # Conversion sécurisée des valeurs
        if pd.isna(total_rem) or total_rem is None:
            total_rem = 0
        if pd.isna(total_boites) or total_boites is None:
            total_boites = 0
            
        cout_par_boite = total_rem / total_boites if total_boites and total_boites > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_number(kpis.get('total_boites', 0))}</div>
                <div class="kpi-label">📦 Nombre de Boîtes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_currency(cout_par_boite)}</div>
                <div class="kpi-label">💰 Coût par Boîte</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_currency(kpis.get('total_rem', 0))}</div>
                <div class="kpi-label">💸 Montant Remboursé</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{kpis.get('nb_etablissements', 0)}</div>
                <div class="kpi-label">🏥 Établissements</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.info(f"📊 **{kpis.get('total_lignes', 0):,}** lignes trouvées avec les filtres appliqués")
    
    # Onglets pour les 3 tableaux
    tab1, tab2, tab3 = st.tabs(["🏥 Top Établissements", "💊 Top Produits", "🧬 Top Molécules"])
    
    with tab1:
        st.subheader("🏥 Top Établissements par Remboursement")
        
        limit_etabs = st.selectbox("Nombre à afficher", [20, 50, 100], index=1, key="limit_etabs")
        
        with st.spinner("🏥 Chargement TOP établissements..."):
            client, project_id = init_bigquery()
            if client:
                df_etabs = get_top_data("etablissements", filters, limit_etabs)
            else:
                st.warning("⚠️ Données indisponibles - BigQuery non accessible")
                df_etabs = pd.DataFrame()
        
        if len(df_etabs) > 0:
            # Formatage
            df_display = df_etabs.copy()
            df_display['REM'] = df_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['BSE'] = df_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['cout_par_boite'] = df_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['taux_remboursement'] = df_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            df_display['BOITES'] = df_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            df_display.columns = ['Établissement', 'Ville', 'Catégorie', 'Montant Remboursé', 'Base Remboursable', 'Boîtes', 'Coût/Boîte', 'Taux Remb.']
            
            st.dataframe(df_display, width="stretch")
            
            
            csv = df_display.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger", csv, f"etablissements_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
        else:
            st.warning("Aucun établissement trouvé")
    
    with tab2:
        st.subheader("💊 Top Produits par Remboursement")
        
        limit_meds = st.selectbox("Nombre à afficher", [20, 50, 100], index=1, key="limit_meds")
        
        with st.spinner("💊 Chargement TOP médicaments..."):
            client, project_id = init_bigquery()
            if client:
                df_meds = get_top_data("medicaments", filters, limit_meds)
            else:
                st.warning("⚠️ Données indisponibles - BigQuery non accessible")
                df_meds = pd.DataFrame()
        
        if len(df_meds) > 0:
            # Formatage
            df_display = df_meds.copy()
            df_display['REM'] = df_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['BSE'] = df_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['cout_par_boite'] = df_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['taux_remboursement'] = df_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            df_display['BOITES'] = df_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            df_display.columns = ['Médicament', 'ATC1', 'Libellé ATC1', 'Montant Remboursé', 'Base Remboursable', 'Boîtes', 'Nb Établissements', 'Coût/Boîte', 'Taux Remb.']
            
            st.dataframe(df_display, width="stretch")
            
            
            csv = df_display.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger", csv, f"medicaments_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", key="dl_meds")
        else:
            st.warning("Aucun médicament trouvé")
    
    with tab3:
        st.subheader("🧬 Top Molécules par Remboursement")
        
        limit_mols = st.selectbox("Nombre à afficher", [20, 50, 100], index=1, key="limit_mols")
        
        with st.spinner("🧬 Chargement TOP molécules..."):
            client, project_id = init_bigquery()
            if client:
                df_mols = get_top_data("molecules", filters, limit_mols)
            else:
                st.warning("⚠️ Données indisponibles - BigQuery non accessible")
                df_mols = pd.DataFrame()
        
        if len(df_mols) > 0:
            # Formatage
            df_display = df_mols.copy()
            df_display['REM'] = df_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['BSE'] = df_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['cout_par_boite'] = df_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['taux_remboursement'] = df_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            df_display['BOITES'] = df_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            df_display.columns = ['Molécule', 'ATC1', 'Libellé ATC1', 'Montant Remboursé', 'Base Remboursable', 'Boîtes', 'Nb Établissements', 'Coût/Boîte', 'Taux Remb.']
            
            st.dataframe(df_display, width="stretch")
            
            
            csv = df_display.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger", csv, f"molecules_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", key="dl_mols")
        else:
            st.warning("Aucune molécule trouvée")
    
    # Footer avec informations de performance
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🏥 <strong>PHMEV Analytics Pro - Version Dynamique</strong></p>
        <p>⚡ BigQuery + Filtres hiérarchiques dynamiques + Mise à jour automatique</p>
        <p><small>🚀 Performance optimisée sur 2,5M lignes | 🔄 Filtres en temps réel | 💊 Noms commerciaux</small></p>
        <p><small>✅ Cabometyx maintenant détectable | 🎯 Filtres intelligents</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
