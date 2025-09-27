"""
🏥 PHMEV Analytics Pro - Version BigQuery
Application d'analyse des données pharmaceutiques PHMEV avec Google BigQuery
Version complète identique à la classique mais optimisée cloud
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account
import json

# Configuration de la page
st.set_page_config(
    page_title="🏥 PHMEV Analytics Pro - BigQuery",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS moderne identique à la version classique
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
}

.main-header p {
    margin: 0.5rem 0 0 0;
    font-size: 1.1rem;
    opacity: 0.9;
}

.kpi-container {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    padding: 1.5rem;
    border-radius: 12px;
    border-left: 5px solid #667eea;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin: 1rem 0;
    transition: transform 0.2s ease;
}

.kpi-container:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

.kpi-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: #667eea;
    margin: 0;
    line-height: 1;
}

.kpi-label {
    color: #666;
    font-size: 1rem;
    margin-top: 0.5rem;
    font-weight: 500;
}

.metric-card {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    margin: 0.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.filter-section {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    border-left: 3px solid #667eea;
}

.stDataFrame {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

[data-testid="stDataFrame"] {
    background-color: white !important;
}

[data-testid="stDataFrame"] table {
    background-color: white !important;
    color: black !important;
    font-size: 0.9rem;
}

[data-testid="stDataFrame"] th {
    background-color: #667eea !important;
    color: white !important;
    font-weight: bold !important;
    padding: 12px 8px !important;
    text-align: center !important;
}

[data-testid="stDataFrame"] td {
    background-color: white !important;
    color: black !important;
    padding: 10px 8px !important;
    border-bottom: 1px solid #e9ecef !important;
}

[data-testid="stDataFrame"] tr:nth-child(even) td {
    background-color: #f8f9fa !important;
}

[data-testid="stDataFrame"] tr:hover td {
    background-color: #e3f2fd !important;
}

.stSelectbox > div > div {
    background-color: white;
    border: 2px solid #e9ecef;
    border-radius: 8px;
}

.stMultiSelect > div > div {
    background-color: white;
    border: 2px solid #e9ecef;
    border-radius: 8px;
}

.stButton > button {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.info-box {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #2196f3;
    margin: 1rem 0;
}

.warning-box {
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #ff9800;
    margin: 1rem 0;
}

.success-box {
    background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #4caf50;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Fonctions utilitaires
def format_number(value):
    """Format un nombre avec séparateurs français"""
    if pd.isna(value) or value == 0:
        return "0"
    
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.0f}K"
    else:
        return f"{value:.0f}"

def format_currency(value):
    """Format une valeur monétaire en euros"""
    if pd.isna(value) or value == 0:
        return "0,00€"
    
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M€"
    elif value >= 1_000:
        return f"{value/1_000:.0f}K€"
    else:
        return f"{value:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.')

def format_percentage(value):
    """Format un pourcentage"""
    if pd.isna(value):
        return "0.0%"
    return f"{value:.1f}%"

def create_demo_data():
    """Crée des données de démonstration si BigQuery n'est pas accessible"""
    np.random.seed(42)
    n_rows = 50000  # Échantillon plus réaliste pour démo
    
    # Listes de données réalistes
    etablissements = [
        "CHU de Lyon", "Hôpital Saint-Antoine", "Clinique des Lilas",
        "CHR de Lille", "Hôpital Européen", "Clinique du Parc"
    ] * 100
    
    medicaments = [
        "Cabometyx", "Keytruda", "Opdivo", "Tecfidera", "Humira"
    ] * 100
    
    villes = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"] * 100
    categories = ["CHU", "CHR", "Clinique Privée"] * 100
    
    # Générer les données
    data = {
        'etablissement': np.random.choice(etablissements, n_rows),
        'medicament': np.random.choice(medicaments, n_rows),
        'ville': np.random.choice(villes, n_rows),
        'categorie': np.random.choice(categories, n_rows),
        'BOITES': np.random.exponential(50, n_rows).astype(int) + 1,
        'REM': np.random.exponential(5000, n_rows),
        'BSE': np.random.exponential(6000, n_rows),
        'atc1': np.random.choice(['A', 'B', 'C', 'D', 'G'], n_rows),
        'L_ATC1': np.random.choice([
            'Système digestif', 'Sang et organes', 'Système cardiovasculaire'
        ], n_rows),
        'L_ATC5': np.random.choice(medicaments, n_rows)
    }
    
    df = pd.DataFrame(data)
    df['cout_par_boite'] = df['REM'] / df['BOITES']
    df['taux_remboursement'] = (df['REM'] / df['BSE']) * 100
    df = df.replace([np.inf, -np.inf], 0).fillna(0)
    
    return df

# Configuration BigQuery
@st.cache_resource
def init_bigquery():
    """🔗 Initialise la connexion BigQuery"""
    try:
        # Essayer d'abord avec les secrets Streamlit
        if "gcp_service_account" in st.secrets:
            credentials_info = st.secrets["gcp_service_account"]
            credentials = service_account.Credentials.from_service_account_info(credentials_info)
            client = bigquery.Client(credentials=credentials, project=credentials_info["project_id"])
            return client, credentials_info["project_id"]
        
        # Fallback pour développement local
        else:
            # Utiliser les credentials par défaut (gcloud auth application-default login)
            client = bigquery.Client(project='test-db-473321')
            return client, 'test-db-473321'
            
    except Exception as e:
        st.error(f"❌ Erreur de connexion BigQuery: {e}")
        return None, None

@st.cache_data(ttl=3600)  # Cache 1 heure
def get_filter_options_bigquery():
    """🎛️ Récupère les options de filtres depuis BigQuery (optimisé)"""
    client, project_id = init_bigquery()
    
    if not client:
        return {}
    
    try:
        # Requête ultra-optimisée avec LIMIT pour le chargement initial
        query = f"""
        SELECT DISTINCT
            atc1, l_atc1,
            COALESCE(NULLIF(nom_ville, ''), 'Non spécifiée') as ville,
            COALESCE(NULLIF(categorie_jur, ''), 'Non spécifiée') as categorie,
            COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié') as etablissement,
            COALESCE(NULLIF(L_ATC5, ''), 'Non spécifié') as medicament
        FROM `{project_id}.dataset.PHMEV2024`
        WHERE l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')
        AND l_cip13 IS NOT NULL
        LIMIT 50000
        """
        
        df_options = client.query(query).to_dataframe()
        
        # Construire les options de filtres (optimisé)
        options = {
            'atc1': sorted([(row['atc1'], row['l_atc1']) for _, row in df_options[['atc1', 'l_atc1']].dropna().drop_duplicates().iterrows()]),
            'villes': sorted(df_options['ville'].dropna().unique().tolist()),
            'categories': sorted(df_options['categorie'].dropna().unique().tolist()),
            'etablissements': sorted(df_options['etablissement'].dropna().unique().tolist()),
            'medicaments': sorted(df_options['medicament'].dropna().unique().tolist())
        }
        
        return options
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la récupération des options: {e}")
        return {}

def get_top_etablissements_bigquery(filters, limit=50):
    """🏥 Récupère le TOP N établissements directement depuis BigQuery"""
    client, project_id = init_bigquery()
    
    if not client:
        return pd.DataFrame()
    
    try:
        # Construire la clause WHERE
        where_conditions = [
            "l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')",
            "l_cip13 IS NOT NULL"
        ]
        
        # Ajouter les filtres
        if filters.get('atc1'):
            atc1_list = "', '".join(filters['atc1'])
            where_conditions.append(f"atc1 IN ('{atc1_list}')")
        
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
            where_conditions.append(f"COALESCE(NULLIF(L_ATC5, ''), 'Non spécifié') IN ('{med_list}')")
        
        if filters.get('min_boites', 0) > 0:
            where_conditions.append(f"BOITES >= {filters['min_boites']}")
        
        where_clause = " AND ".join(where_conditions)
        
        # Requête agrégée pour TOP établissements
        query = f"""
        SELECT 
            COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié') as etablissement,
            COALESCE(NULLIF(nom_ville, ''), 'Non spécifiée') as ville,
            COALESCE(NULLIF(categorie_jur, ''), 'Non spécifiée') as categorie,
            SUM(REM) as REM,
            SUM(BSE) as BSE,
            SUM(BOITES) as BOITES,
            COUNT(*) as nb_lignes,
            SUM(REM) / SUM(BOITES) as cout_par_boite,
            (SUM(REM) / SUM(BSE)) * 100 as taux_remboursement
        FROM `{project_id}.dataset.PHMEV2024`
        WHERE {where_clause}
        GROUP BY etablissement, ville, categorie
        ORDER BY REM DESC
        LIMIT {limit}
        """
        
        return client.query(query).to_dataframe()
        
    except Exception as e:
        st.error(f"❌ Erreur BigQuery établissements: {e}")
        return pd.DataFrame()

def get_top_medicaments_bigquery(filters, limit=50):
    """💊 Récupère le TOP N médicaments directement depuis BigQuery"""
    client, project_id = init_bigquery()
    
    if not client:
        return pd.DataFrame()
    
    try:
        # Construire la clause WHERE (même logique)
        where_conditions = [
            "l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')",
            "l_cip13 IS NOT NULL"
        ]
        
        # Ajouter les filtres
        if filters.get('atc1'):
            atc1_list = "', '".join(filters['atc1'])
            where_conditions.append(f"atc1 IN ('{atc1_list}')")
        
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
            where_conditions.append(f"COALESCE(NULLIF(L_ATC5, ''), 'Non spécifié') IN ('{med_list}')")
        
        if filters.get('min_boites', 0) > 0:
            where_conditions.append(f"BOITES >= {filters['min_boites']}")
        
        where_clause = " AND ".join(where_conditions)
        
        # Requête agrégée pour TOP médicaments
        query = f"""
        SELECT 
            COALESCE(NULLIF(L_ATC5, ''), 'Non spécifié') as medicament,
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
        
        return client.query(query).to_dataframe()
        
    except Exception as e:
        st.error(f"❌ Erreur BigQuery médicaments: {e}")
        return pd.DataFrame()

def get_top_molecules_bigquery(filters, limit=50):
    """🧬 Récupère le TOP N molécules directement depuis BigQuery"""
    client, project_id = init_bigquery()
    
    if not client:
        return pd.DataFrame()
    
    try:
        # Construire la clause WHERE (même logique)
        where_conditions = [
            "l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')",
            "l_cip13 IS NOT NULL"
        ]
        
        # Ajouter les filtres
        if filters.get('atc1'):
            atc1_list = "', '".join(filters['atc1'])
            where_conditions.append(f"atc1 IN ('{atc1_list}')")
        
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
            where_conditions.append(f"COALESCE(NULLIF(L_ATC5, ''), 'Non spécifié') IN ('{med_list}')")
        
        if filters.get('min_boites', 0) > 0:
            where_conditions.append(f"BOITES >= {filters['min_boites']}")
        
        where_clause = " AND ".join(where_conditions)
        
        # Requête agrégée pour TOP molécules (utilise L_ATC5 comme molécule)
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
        st.error(f"❌ Erreur BigQuery molécules: {e}")
        return pd.DataFrame()

def get_kpis_bigquery(filters):
    """📊 Récupère les KPIs directement depuis BigQuery"""
    client, project_id = init_bigquery()
    
    if not client:
        return {}
    
    try:
        # Construire la clause WHERE (même logique)
        where_conditions = [
            "l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')",
            "l_cip13 IS NOT NULL"
        ]
        
        # Ajouter les filtres
        if filters.get('atc1'):
            atc1_list = "', '".join(filters['atc1'])
            where_conditions.append(f"atc1 IN ('{atc1_list}')")
        
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
            where_conditions.append(f"COALESCE(NULLIF(L_ATC5, ''), 'Non spécifié') IN ('{med_list}')")
        
        if filters.get('min_boites', 0) > 0:
            where_conditions.append(f"BOITES >= {filters['min_boites']}")
        
        where_clause = " AND ".join(where_conditions)
        
        # Requête pour KPIs
        query = f"""
        SELECT 
            COUNT(*) as total_lignes,
            SUM(REM) as total_rem,
            SUM(BSE) as total_bse,
            SUM(BOITES) as total_boites,
            COUNT(DISTINCT COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié')) as nb_etablissements,
            COUNT(DISTINCT COALESCE(NULLIF(L_ATC5, ''), 'Non spécifié')) as nb_medicaments,
            COUNT(DISTINCT COALESCE(NULLIF(nom_ville, ''), 'Non spécifiée')) as nb_villes,
            AVG(CASE WHEN BOITES > 0 THEN REM / BOITES ELSE 0 END) as cout_moyen_boite
        FROM `{project_id}.dataset.PHMEV2024`
        WHERE {where_clause}
        """
        
        result = client.query(query).to_dataframe()
        if len(result) > 0:
            return result.iloc[0].to_dict()
        return {}
        
    except Exception as e:
        st.error(f"❌ Erreur BigQuery KPIs: {e}")
        return {}

@st.cache_data
def get_all_filter_options(df):
    """Récupère toutes les options de filtres disponibles"""
    if df is None or len(df) == 0:
        return {}
    
    def safe_sort_atc_items(items):
        """Tri sécurisé pour les codes ATC mixtes"""
        try:
            return sorted(items, key=lambda x: (str(x[0]), str(x[1])))
        except:
            return sorted([(str(k), str(v)) for k, v in items])
    
    return {
        'atc1': safe_sort_atc_items(df[['atc1', 'l_atc1']].drop_duplicates().set_index('atc1')['l_atc1'].dropna().to_dict().items()) if 'l_atc1' in df.columns else [],
        'atc2': safe_sort_atc_items(df[['atc2', 'L_ATC2']].drop_duplicates().set_index('atc2')['L_ATC2'].dropna().to_dict().items()) if 'atc2' in df.columns and 'L_ATC2' in df.columns else [],
        'atc3': safe_sort_atc_items(df[['atc3', 'L_ATC3']].drop_duplicates().set_index('atc3')['L_ATC3'].dropna().to_dict().items()) if 'atc3' in df.columns and 'L_ATC3' in df.columns else [],
        'atc4': safe_sort_atc_items(df[['atc4', 'L_ATC4']].drop_duplicates().set_index('atc4')['L_ATC4'].dropna().to_dict().items()) if 'atc4' in df.columns and 'L_ATC4' in df.columns else [],
        'atc5': safe_sort_atc_items(df[['ATC5', 'L_ATC5']].drop_duplicates().set_index('ATC5')['L_ATC5'].dropna().to_dict().items()) if 'ATC5' in df.columns else [],
        'villes': sorted([str(x) for x in df['ville'].dropna().unique()]),
        'categories': sorted([str(x) for x in df['categorie'].dropna().unique()]),
        'etablissements': sorted([str(x) for x in df['etablissement'].dropna().unique()]),
        'medicaments': sorted([str(x) for x in df['medicament'].dropna().unique()])
    }

def get_available_options(df_filtered, column_mapping):
    """Récupère les options disponibles selon les filtres appliqués"""
    if df_filtered is None or len(df_filtered) == 0:
        return []
    
    try:
        code_col, label_col = column_mapping
        if code_col not in df_filtered.columns or label_col not in df_filtered.columns:
            return []
        
        # Filtrer les valeurs non informatives
        df_clean = df_filtered[
            (df_filtered[code_col].notna()) & 
            (df_filtered[label_col].notna()) &
            (~df_filtered[code_col].isin(['', 'Non restitué', 'Non spécifié'])) &
            (~df_filtered[label_col].isin(['', 'Non restitué', 'Non spécifié']))
        ]
        
        if len(df_clean) == 0:
            return []
        
        # Créer le dictionnaire et trier
        items = df_clean[[code_col, label_col]].drop_duplicates().set_index(code_col)[label_col].to_dict().items()
        return sorted(items, key=lambda x: (str(x[0]), str(x[1])))
        
    except Exception as e:
        st.error(f"Erreur dans get_available_options: {e}")
        return []

# Fonction apply_filters supprimée - remplacée par load_filtered_data_bigquery

def main():
    """Application principale"""
    
    # En-tête
    st.markdown("""
    <div class="main-header">
        <h1>🏥 PHMEV Analytics Pro - BigQuery Edition</h1>
        <p>Analyse complète des données pharmaceutiques PHMEV</p>
        <p><small>⚡ Powered by Google BigQuery - Performance maximale</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des options de filtres (une seule fois)
    with st.spinner("🚀 Connexion à BigQuery et récupération des filtres..."):
        filter_options = get_filter_options_bigquery()
    
    if not filter_options:
        st.error("❌ Impossible de charger les options depuis BigQuery")
        st.info("Vérifiez la configuration des credentials dans les secrets Streamlit")
        return
    
    # Initialisation des filtres dans session_state
    if 'filters' not in st.session_state:
        st.session_state.filters = {}
    
    # Sidebar - Filtres hiérarchiques identiques à la version classique
    st.sidebar.header("🎛️ Filtres Hiérarchiques")
    
    # Filtre ATC1 (simplifié)
    st.sidebar.subheader("🧬 Classification Thérapeutique")
    atc1_options = filter_options.get('atc1', [])
    selected_atc1 = st.sidebar.multiselect(
        "ATC Niveau 1", 
        options=[code for code, label in atc1_options],
        format_func=lambda x: f"{x} - {dict(atc1_options).get(x, x)}",
        key="atc1_filter",
        help="Classification thérapeutique anatomique niveau 1"
    )
    st.session_state.filters['atc1'] = selected_atc1
    
    # Autres filtres
    st.sidebar.subheader("🏥 Filtres Géographiques & Organisationnels")
    
    # Filtre Villes
    ville_options = filter_options.get('villes', [])
    selected_villes = st.sidebar.multiselect(
        "🏙️ Villes", 
        options=ville_options,
        key="villes_filter"
    )
    st.session_state.filters['villes'] = selected_villes
    
    # Filtre Catégories
    cat_options = filter_options.get('categories', [])
    selected_categories = st.sidebar.multiselect(
        "🏥 Catégories d'Établissements", 
        options=cat_options,
        key="categories_filter"
    )
    st.session_state.filters['categories'] = selected_categories
    
    # Filtre Établissements
    etab_options = filter_options.get('etablissements', [])
    selected_etablissements = st.sidebar.multiselect(
        "🏢 Établissements", 
        options=etab_options,
        key="etablissements_filter"
    )
    st.session_state.filters['etablissements'] = selected_etablissements
    
    # Recherche de médicaments
    st.sidebar.subheader("💊 Recherche de Médicaments")
    
    # Recherche par nom
    search_term = st.sidebar.text_input(
        "🔍 Rechercher un médicament", 
        placeholder="Ex: cabome, keytruda...",
        key="med_search"
    )
    
    # Filtrer les médicaments selon la recherche
    med_options = filter_options.get('medicaments', [])
    if search_term:
        med_options = [med for med in med_options if search_term.lower() in med.lower()]
    
    selected_medicaments = st.sidebar.multiselect(
        "💊 Médicaments", 
        options=med_options,
        key="medicaments_filter",
        help=f"{'❌ Aucun médicament trouvé pour ' + repr(search_term) if search_term and not med_options else '✅ ' + str(len(med_options)) + ' médicaments disponibles'}"
    )
    st.session_state.filters['medicaments'] = selected_medicaments
    
    # Filtre nombre de boîtes
    min_boites = st.sidebar.number_input(
        "📦 Nombre minimum de boîtes", 
        min_value=0, 
        value=0,
        key="min_boites_filter",
        help="Filtrer par nombre minimum de boîtes dispensées"
    )
    st.session_state.filters['min_boites'] = min_boites
    
    # Bouton reset
    if st.sidebar.button("🔄 Réinitialiser tous les filtres"):
        for key in list(st.session_state.keys()):
            if key.endswith('_filter'):
                del st.session_state[key]
        st.session_state.filters = {}
        st.rerun()
    
    # Chargement des données filtrées depuis BigQuery
    with st.spinner("📊 Application des filtres dans BigQuery..."):
        df_filtered = load_filtered_data_bigquery(st.session_state.filters)
    
    # Affichage des informations de filtrage
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.info(f"📊 **{len(df_filtered):,}** lignes trouvées")
    with col_info2:
        if st.session_state.filters:
            st.info(f"🎯 **Filtres actifs** - Données optimisées BigQuery")
    
    # KPIs principaux
    if len(df_filtered) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_rem = df_filtered['REM'].sum()
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_currency(total_rem)}</div>
                <div class="kpi-label">💰 Montant Total Remboursé</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_bse = df_filtered['BSE'].sum()
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_currency(total_bse)}</div>
                <div class="kpi-label">🏦 Base Remboursable Totale</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_boites = df_filtered['BOITES'].sum()
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_number(total_boites)}</div>
                <div class="kpi-label">📦 Boîtes Totales</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            taux_moyen = (df_filtered['REM'].sum() / df_filtered['BSE'].sum()) * 100 if df_filtered['BSE'].sum() > 0 else 0
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_percentage(taux_moyen)}</div>
                <div class="kpi-label">📊 Taux Remboursement Moyen</div>
            </div>
            """, unsafe_allow_html=True)
        
        # KPIs secondaires
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            nb_etabs = df_filtered['etablissement'].nunique()
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{nb_etabs}</div>
                <div class="kpi-label">🏥 Établissements Uniques</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            nb_medicaments = df_filtered['medicament'].nunique()
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{nb_medicaments}</div>
                <div class="kpi-label">💊 Médicaments Uniques</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col7:
            nb_villes = df_filtered['ville'].nunique()
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{nb_villes}</div>
                <div class="kpi-label">🏙️ Villes Uniques</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col8:
            cout_moyen = df_filtered['cout_par_boite'].mean()
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_currency(cout_moyen)}</div>
                <div class="kpi-label">💰 Coût Moyen/Boîte</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Onglets pour les analyses (identiques à la version classique)
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏥 Établissements", 
        "💊 Médicaments", 
        "🧬 Molécules", 
        "🏙️ Géographie", 
        "📊 Classifications", 
        "📋 Données Détaillées"
    ])
    
    with tab1:
        st.subheader("🏥 Analyse par Établissements")
        
        if len(df_filtered) > 0:
            # Agrégation par établissement
            df_etabs = df_filtered.groupby(['etablissement', 'categorie', 'ville']).agg({
                'REM': 'sum',
                'BSE': 'sum',
                'BOITES': 'sum'
            }).reset_index()
            
            df_etabs['cout_par_boite'] = df_etabs['REM'] / df_etabs['BOITES']
            df_etabs['taux_remboursement'] = (df_etabs['REM'] / df_etabs['BSE']) * 100
            df_etabs = df_etabs.sort_values('REM', ascending=False)
            
            # Options d'affichage
            col_opt1, col_opt2 = st.columns(2)
            with col_opt1:
                nb_etabs = st.selectbox("Nombre d'établissements à afficher", [10, 20, 50, 100], index=1)
            with col_opt2:
                show_chart = st.checkbox("📊 Afficher le graphique", value=True)
            
            # Tableau
            df_etabs_display = df_etabs.head(nb_etabs).copy()
            
            # Formatage pour affichage
            df_etabs_display['REM'] = df_etabs_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_etabs_display['BSE'] = df_etabs_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_etabs_display['cout_par_boite'] = df_etabs_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_etabs_display['taux_remboursement'] = df_etabs_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            df_etabs_display['BOITES'] = df_etabs_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            df_etabs_display.columns = ['Établissement', 'Catégorie', 'Ville', 'Montant Remboursé', 'Base Remboursable', 'Boîtes', 'Coût/Boîte', 'Taux Remb.']
            
            st.dataframe(df_etabs_display, use_container_width=True)
            
            # Graphique
            if show_chart:
                fig = px.bar(
                    df_etabs.head(15), 
                    x='REM', 
                    y='etablissement',
                    orientation='h',
                    title=f"Top 15 Établissements par Remboursement",
                    labels={'REM': 'Montant Remboursé (€)', 'etablissement': 'Établissement'},
                    color='REM',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Export CSV
            csv_etabs = df_etabs_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger les données établissements",
                data=csv_etabs,
                file_name=f"etablissements_phmev_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("Aucune donnée disponible avec les filtres sélectionnés")
    
    with tab2:
        st.subheader("💊 Analyse par Médicaments")
        
        if len(df_filtered) > 0:
            # Agrégation par médicament
            df_meds = df_filtered.groupby(['medicament', 'L_ATC1']).agg({
                'REM': 'sum',
                'BSE': 'sum',
                'BOITES': 'sum'
            }).reset_index()
            
            df_meds['cout_par_boite'] = df_meds['REM'] / df_meds['BOITES']
            df_meds['taux_remboursement'] = (df_meds['REM'] / df_meds['BSE']) * 100
            df_meds = df_meds.sort_values('REM', ascending=False)
            
            # Options d'affichage
            col_opt1, col_opt2 = st.columns(2)
            with col_opt1:
                nb_meds = st.selectbox("Nombre de médicaments à afficher", [10, 20, 50, 100], index=1, key="nb_meds")
            with col_opt2:
                show_chart_meds = st.checkbox("📊 Afficher le graphique", value=True, key="chart_meds")
            
            # Tableau
            df_meds_display = df_meds.head(nb_meds).copy()
            
            # Formatage pour affichage
            df_meds_display['REM'] = df_meds_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_meds_display['BSE'] = df_meds_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_meds_display['cout_par_boite'] = df_meds_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_meds_display['taux_remboursement'] = df_meds_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            df_meds_display['BOITES'] = df_meds_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            df_meds_display.columns = ['Médicament', 'Classification ATC1', 'Montant Remboursé', 'Base Remboursable', 'Boîtes', 'Coût/Boîte', 'Taux Remb.']
            
            st.dataframe(df_meds_display, use_container_width=True)
            
            # Graphique
            if show_chart_meds:
                fig = px.bar(
                    df_meds.head(15), 
                    x='REM', 
                    y='medicament',
                    orientation='h',
                    title=f"Top 15 Médicaments par Remboursement",
                    labels={'REM': 'Montant Remboursé (€)', 'medicament': 'Médicament'},
                    color='REM',
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Export CSV
            csv_meds = df_meds_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger les données médicaments",
                data=csv_meds,
                file_name=f"medicaments_phmev_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_meds"
            )
        else:
            st.warning("Aucune donnée disponible avec les filtres sélectionnés")
    
    with tab3:
        st.subheader("🧬 Analyse par Molécules/Principes Actifs")
        
        if len(df_filtered) > 0 and 'L_ATC5' in df_filtered.columns:
            # Agrégation par molécule (L_ATC5)
            df_molecules = df_filtered.groupby(['L_ATC5', 'L_ATC1']).agg({
                'REM': 'sum',
                'BSE': 'sum',
                'BOITES': 'sum'
            }).reset_index()
            
            df_molecules['cout_par_boite'] = df_molecules['REM'] / df_molecules['BOITES']
            df_molecules['taux_remboursement'] = (df_molecules['REM'] / df_molecules['BSE']) * 100
            df_molecules = df_molecules.sort_values('REM', ascending=False)
            
            # Options d'affichage
            col_opt1, col_opt2 = st.columns(2)
            with col_opt1:
                nb_molecules = st.selectbox("Nombre de molécules à afficher", [10, 20, 50, 100], index=1, key="nb_molecules")
            with col_opt2:
                show_chart_molecules = st.checkbox("📊 Afficher le graphique", value=True, key="chart_molecules")
            
            # Tableau
            df_molecules_display = df_molecules.head(nb_molecules).copy()
            
            # Formatage pour affichage
            df_molecules_display['REM'] = df_molecules_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_molecules_display['BSE'] = df_molecules_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_molecules_display['cout_par_boite'] = df_molecules_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_molecules_display['taux_remboursement'] = df_molecules_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            df_molecules_display['BOITES'] = df_molecules_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            df_molecules_display.columns = ['Molécule/Principe Actif', 'Classification ATC1', 'Montant Remboursé', 'Base Remboursable', 'Boîtes', 'Coût/Boîte', 'Taux Remb.']
            
            st.dataframe(df_molecules_display, use_container_width=True)
            
            # Graphique
            if show_chart_molecules:
                fig = px.bar(
                    df_molecules.head(15), 
                    x='REM', 
                    y='L_ATC5',
                    orientation='h',
                    title=f"Top 15 Molécules par Remboursement",
                    labels={'REM': 'Montant Remboursé (€)', 'L_ATC5': 'Molécule'},
                    color='REM',
                    color_continuous_scale='Plasma'
                )
                fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Export CSV
            csv_molecules = df_molecules_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger les données molécules",
                data=csv_molecules,
                file_name=f"molecules_phmev_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_molecules"
            )
        else:
            st.warning("Aucune donnée de molécules disponible avec les filtres sélectionnés")
    
    with tab4:
        st.subheader("🏙️ Analyse Géographique")
        
        if len(df_filtered) > 0:
            # Agrégation par ville et région
            df_geo = df_filtered.groupby(['ville', 'region']).agg({
                'REM': 'sum',
                'BSE': 'sum',
                'BOITES': 'sum',
                'etablissement': 'nunique'
            }).reset_index()
            
            df_geo['cout_par_boite'] = df_geo['REM'] / df_geo['BOITES']
            df_geo['taux_remboursement'] = (df_geo['REM'] / df_geo['BSE']) * 100
            df_geo = df_geo.sort_values('REM', ascending=False)
            
            # Options d'affichage
            col_opt1, col_opt2 = st.columns(2)
            with col_opt1:
                nb_villes_geo = st.selectbox("Nombre de villes à afficher", [10, 20, 50, 100], index=1, key="nb_villes_geo")
            with col_opt2:
                show_chart_geo = st.checkbox("📊 Afficher le graphique", value=True, key="chart_geo")
            
            # Tableau
            df_geo_display = df_geo.head(nb_villes_geo).copy()
            
            # Formatage pour affichage
            df_geo_display['REM'] = df_geo_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_geo_display['BSE'] = df_geo_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_geo_display['cout_par_boite'] = df_geo_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_geo_display['taux_remboursement'] = df_geo_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            df_geo_display['BOITES'] = df_geo_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            df_geo_display.columns = ['Ville', 'Région', 'Montant Remboursé', 'Base Remboursable', 'Boîtes', 'Nb Établissements', 'Coût/Boîte', 'Taux Remb.']
            
            st.dataframe(df_geo_display, use_container_width=True)
            
            # Graphique
            if show_chart_geo:
                fig = px.bar(
                    df_geo.head(15), 
                    x='REM', 
                    y='ville',
                    orientation='h',
                    title=f"Top 15 Villes par Remboursement",
                    labels={'REM': 'Montant Remboursé (€)', 'ville': 'Ville'},
                    color='etablissement',
                    color_continuous_scale='Oranges'
                )
                fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Export CSV
            csv_geo = df_geo_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger les données géographiques",
                data=csv_geo,
                file_name=f"geographie_phmev_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_geo"
            )
        else:
            st.warning("Aucune donnée géographique disponible avec les filtres sélectionnés")
    
    with tab5:
        st.subheader("📊 Analyse par Classifications ATC")
        
        if len(df_filtered) > 0:
            # Analyse par ATC1
            st.write("### Classification ATC Niveau 1")
            df_atc1 = df_filtered.groupby(['atc1', 'L_ATC1']).agg({
                'REM': 'sum',
                'BSE': 'sum',
                'BOITES': 'sum'
            }).reset_index()
            
            df_atc1['cout_par_boite'] = df_atc1['REM'] / df_atc1['BOITES']
            df_atc1['taux_remboursement'] = (df_atc1['REM'] / df_atc1['BSE']) * 100
            df_atc1 = df_atc1.sort_values('REM', ascending=False)
            
            # Formatage pour affichage
            df_atc1_display = df_atc1.copy()
            df_atc1_display['REM'] = df_atc1_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_atc1_display['BSE'] = df_atc1_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_atc1_display['cout_par_boite'] = df_atc1_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_atc1_display['taux_remboursement'] = df_atc1_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            df_atc1_display['BOITES'] = df_atc1_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            df_atc1_display.columns = ['Code ATC1', 'Libellé ATC1', 'Montant Remboursé', 'Base Remboursable', 'Boîtes', 'Coût/Boîte', 'Taux Remb.']
            
            st.dataframe(df_atc1_display, use_container_width=True)
            
            # Graphique en secteurs pour ATC1
            if st.checkbox("📊 Afficher le graphique en secteurs ATC1", key="chart_atc1"):
                fig_pie = px.pie(
                    df_atc1, 
                    values='REM', 
                    names='L_ATC1',
                    title="Répartition des Remboursements par Classification ATC1"
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Export CSV
            csv_atc1 = df_atc1_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger les données ATC1",
                data=csv_atc1,
                file_name=f"atc1_phmev_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_atc1"
            )
        else:
            st.warning("Aucune donnée de classification disponible avec les filtres sélectionnés")
    
    with tab6:
        st.subheader("📋 Données Détaillées")
        
        if len(df_filtered) > 0:
            # Options d'affichage
            col_opt1, col_opt2, col_opt3 = st.columns(3)
            with col_opt1:
                nb_lignes = st.selectbox("Nombre de lignes à afficher", [100, 500, 1000, 5000], index=0)
            with col_opt2:
                colonnes_essentielles = st.checkbox("Afficher colonnes essentielles uniquement", value=True)
            with col_opt3:
                trier_par = st.selectbox("Trier par", ['REM', 'BSE', 'BOITES', 'cout_par_boite'], index=0)
            
            # Sélection des colonnes
            if colonnes_essentielles:
                colonnes = ['etablissement', 'medicament', 'ville', 'categorie', 'REM', 'BSE', 'BOITES', 'cout_par_boite', 'taux_remboursement']
            else:
                colonnes = df_filtered.columns.tolist()
            
            # Tri et limitation
            df_detail = df_filtered[colonnes].sort_values(trier_par, ascending=False).head(nb_lignes)
            
            # Formatage pour affichage
            df_detail_display = df_detail.copy()
            if 'REM' in df_detail_display.columns:
                df_detail_display['REM'] = df_detail_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            if 'BSE' in df_detail_display.columns:
                df_detail_display['BSE'] = df_detail_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            if 'cout_par_boite' in df_detail_display.columns:
                df_detail_display['cout_par_boite'] = df_detail_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            if 'taux_remboursement' in df_detail_display.columns:
                df_detail_display['taux_remboursement'] = df_detail_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            if 'BOITES' in df_detail_display.columns:
                df_detail_display['BOITES'] = df_detail_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            st.dataframe(df_detail_display, use_container_width=True)
            
            # Export CSV complet
            csv_detail = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger toutes les données filtrées",
                data=csv_detail,
                file_name=f"donnees_completes_phmev_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_detail"
            )
            
            # Statistiques du dataset
            st.write("### 📊 Statistiques du Dataset Filtré")
            
            col_stat1, col_stat2 = st.columns(2)
            
            with col_stat1:
                st.markdown(f"""
                <div class="info-box">
                    <h4>📈 Statistiques Générales</h4>
                    <ul>
                        <li><strong>Lignes totales:</strong> {len(df_filtered):,}</li>
                        <li><strong>Établissements uniques:</strong> {df_filtered['etablissement'].nunique():,}</li>
                        <li><strong>Médicaments uniques:</strong> {df_filtered['medicament'].nunique():,}</li>
                        <li><strong>Villes uniques:</strong> {df_filtered['ville'].nunique():,}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col_stat2:
                st.markdown(f"""
                <div class="success-box">
                    <h4>💰 Statistiques Financières</h4>
                    <ul>
                        <li><strong>Montant total remboursé:</strong> {format_currency(df_filtered['REM'].sum())}</li>
                        <li><strong>Base remboursable totale:</strong> {format_currency(df_filtered['BSE'].sum())}</li>
                        <li><strong>Boîtes totales:</strong> {format_number(df_filtered['BOITES'].sum())}</li>
                        <li><strong>Coût moyen par boîte:</strong> {format_currency(df_filtered['cout_par_boite'].mean())}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Aucune donnée disponible avec les filtres sélectionnés")
    
    # Footer avec informations BigQuery
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🏥 <strong>PHMEV Analytics Pro - BigQuery Edition</strong></p>
        <p>⚡ Powered by Google BigQuery | 🚀 Performance maximale pour l'analyse de données pharmaceutiques</p>
        <p><small>📊 Données PHMEV 2024 | Interface développée avec Streamlit</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
