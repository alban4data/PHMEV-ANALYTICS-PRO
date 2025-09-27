"""
🚀 PHMEV Analytics Pro - Version DuckDB
Application d'analyse des données pharmaceutiques avec DuckDB pour optimiser la mémoire
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import duckdb
import os
import gc
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="🏥 PHMEV Analytics Pro - DuckDB",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS pour le style (version allégée)
st.markdown("""
<style>
/* 🎨 VARIABLES CSS */
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --error-color: #ef4444;
    --bg-dark: #0e1117;
    --bg-secondary: #1e2130;
    --text-light: #fafafa;
}

/* 🌟 STYLE GÉNÉRAL */
.main {
    padding: 1rem 2rem;
}

/* 📊 MÉTRIQUES */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    border: none;
    padding: 1rem;
    border-radius: 12px;
    color: white;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

[data-testid="metric-container"] > div {
    color: white !important;
}

/* 📈 GRAPHIQUES */
.js-plotly-plot {
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

/* 📋 TABLES */
[data-testid="stDataFrame"] {
    background: white !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
}

[data-testid="stDataFrame"] td {
    background: white !important;
    color: #000000 !important;
    border-bottom: 1px solid #e5e7eb !important;
}

[data-testid="stDataFrame"] th {
    background: #f9fafb !important;
    color: #000000 !important;
    font-weight: 600 !important;
}

/* 🔄 SIDEBAR */
.css-1d391kg {
    background: linear-gradient(180deg, var(--bg-secondary), var(--bg-dark));
}

/* ⚡ BOUTONS */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
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

# Initialisation de la connexion DuckDB
@st.cache_resource
def init_duckdb():
    """🦆 Initialise la connexion DuckDB"""
    conn = duckdb.connect(':memory:')
    return conn

@st.cache_resource
def load_data_duckdb():
    """🚀 Charge les données PHMEV avec DuckDB (optimisé mémoire)"""
    conn = init_duckdb()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parquet_path = os.path.join(script_dir, 'OPEN_PHMEV_2024.parquet')
    
    progress_placeholder = st.empty()
    
    try:
        progress_placeholder.info("🦆 Initialisation DuckDB...")
        
        if not os.path.exists(parquet_path):
            st.error("❌ Fichier OPEN_PHMEV_2024.parquet non trouvé !")
            return None
            
        progress_placeholder.info("📊 Chargement du fichier parquet dans DuckDB...")
        
        # Créer une table DuckDB à partir du fichier parquet
        conn.execute("""
            CREATE TABLE phmev AS 
            SELECT * FROM read_parquet(?)
        """, [parquet_path])
        
        progress_placeholder.info("🔄 Filtrage des données non informatives...")
        
        # Filtrer les données non informatives directement en SQL
        conn.execute("""
            DELETE FROM phmev 
            WHERE l_cip13 IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')
            OR l_cip13 IS NULL
        """)
        
        progress_placeholder.info("✨ Création des colonnes dérivées...")
        
        # Ajouter les colonnes dérivées avec SQL
        conn.execute("""
            ALTER TABLE phmev ADD COLUMN etablissement VARCHAR;
            ALTER TABLE phmev ADD COLUMN medicament VARCHAR;
            ALTER TABLE phmev ADD COLUMN categorie VARCHAR;
            ALTER TABLE phmev ADD COLUMN ville VARCHAR;
            ALTER TABLE phmev ADD COLUMN region_clean VARCHAR;
            ALTER TABLE phmev ADD COLUMN code_cip VARCHAR;
            ALTER TABLE phmev ADD COLUMN libelle_cip VARCHAR;
            ALTER TABLE phmev ADD COLUMN cout_par_boite DOUBLE;
            ALTER TABLE phmev ADD COLUMN taux_remboursement DOUBLE;
        """)
        
        # Remplir les colonnes dérivées
        conn.execute("""
            UPDATE phmev SET
                etablissement = COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié'),
                medicament = COALESCE(NULLIF(L_ATC5, ''), 'Non spécifié'),
                categorie = COALESCE(NULLIF(categorie_jur, ''), 'Non spécifiée'),
                ville = COALESCE(NULLIF(nom_ville, ''), 'Non spécifiée'),
                region_clean = COALESCE(region_etb, 0),
                code_cip = CAST(CIP13 AS VARCHAR),
                libelle_cip = COALESCE(NULLIF(l_cip13, ''), 'Non spécifié'),
                cout_par_boite = CASE WHEN BOITES > 0 THEN REM / BOITES ELSE 0 END,
                taux_remboursement = CASE WHEN BSE > 0 THEN (REM / BSE) * 100 ELSE 0 END
        """)
        
        # Obtenir le nombre de lignes
        count_result = conn.execute("SELECT COUNT(*) FROM phmev").fetchone()
        total_rows = count_result[0] if count_result else 0
        
        progress_placeholder.success(f"✅ {total_rows:,} lignes chargées et prêtes !")
        progress_placeholder.empty()
        
        return conn
        
    except Exception as e:
        progress_placeholder.error(f"❌ Erreur DuckDB: {e}")
        st.info(f"🔍 Type d'erreur: {type(e).__name__}")
        return None

def get_filter_options_duckdb(conn, filter_type, current_filters=None):
    """📊 Obtient les options disponibles pour un type de filtre avec filtrage interdépendant"""
    if conn is None:
        return []
    
    try:
        # Construire la clause WHERE basée sur les filtres actuels
        where_clauses = []
        params = []
        
        if current_filters:
            if current_filters.get('atc1_filtre'):
                placeholders = ','.join(['?' for _ in current_filters['atc1_filtre']])
                where_clauses.append(f"l_atc1 IN ({placeholders})")
                params.extend(current_filters['atc1_filtre'])
                
            if current_filters.get('atc2_filtre'):
                placeholders = ','.join(['?' for _ in current_filters['atc2_filtre']])
                where_clauses.append(f"L_ATC2 IN ({placeholders})")
                params.extend(current_filters['atc2_filtre'])
                
            if current_filters.get('atc3_filtre'):
                placeholders = ','.join(['?' for _ in current_filters['atc3_filtre']])
                where_clauses.append(f"L_ATC3 IN ({placeholders})")
                params.extend(current_filters['atc3_filtre'])
                
            if current_filters.get('atc4_filtre'):
                placeholders = ','.join(['?' for _ in current_filters['atc4_filtre']])
                where_clauses.append(f"L_ATC4 IN ({placeholders})")
                params.extend(current_filters['atc4_filtre'])
                
            if current_filters.get('atc5_filtre'):
                placeholders = ','.join(['?' for _ in current_filters['atc5_filtre']])
                where_clauses.append(f"L_ATC5 IN ({placeholders})")
                params.extend(current_filters['atc5_filtre'])
                
            if current_filters.get('ville_filtre'):
                placeholders = ','.join(['?' for _ in current_filters['ville_filtre']])
                where_clauses.append(f"ville IN ({placeholders})")
                params.extend(current_filters['ville_filtre'])
                
            if current_filters.get('categorie_filtre'):
                placeholders = ','.join(['?' for _ in current_filters['categorie_filtre']])
                where_clauses.append(f"categorie IN ({placeholders})")
                params.extend(current_filters['categorie_filtre'])
                
            if current_filters.get('etablissement_filtre'):
                placeholders = ','.join(['?' for _ in current_filters['etablissement_filtre']])
                where_clauses.append(f"etablissement IN ({placeholders})")
                params.extend(current_filters['etablissement_filtre'])
                
            if current_filters.get('libelle_filtre'):
                placeholders = ','.join(['?' for _ in current_filters['libelle_filtre']])
                where_clauses.append(f"libelle_cip IN ({placeholders})")
                params.extend(current_filters['libelle_filtre'])
        
        # Ajouter les conditions spécifiques au type de filtre
        if filter_type == 'atc1':
            where_clauses.append("atc1 IS NOT NULL AND l_atc1 IS NOT NULL")
        elif filter_type == 'atc2':
            where_clauses.append("atc2 IS NOT NULL AND L_ATC2 IS NOT NULL")
        elif filter_type == 'atc3':
            where_clauses.append("atc3 IS NOT NULL AND L_ATC3 IS NOT NULL")
        elif filter_type == 'atc4':
            where_clauses.append("atc4 IS NOT NULL AND L_ATC4 IS NOT NULL")
        elif filter_type == 'atc5':
            where_clauses.append("ATC5 IS NOT NULL AND L_ATC5 IS NOT NULL")
        elif filter_type == 'villes':
            where_clauses.append("ville IS NOT NULL AND ville != 'Non spécifiée'")
        elif filter_type == 'categories':
            where_clauses.append("categorie IS NOT NULL AND categorie != 'Non spécifiée'")
        elif filter_type == 'etablissements':
            where_clauses.append("etablissement IS NOT NULL AND etablissement != 'Non spécifié'")
        elif filter_type == 'medicaments':
            where_clauses.append("libelle_cip IS NOT NULL AND libelle_cip != 'Non spécifié'")
        
        where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        if filter_type == 'atc1':
            query = f"""
                SELECT DISTINCT atc1, l_atc1 
                FROM phmev 
                {where_sql}
                ORDER BY l_atc1
            """
        elif filter_type == 'atc2':
            query = f"""
                SELECT DISTINCT atc2, L_ATC2 
                FROM phmev 
                {where_sql}
                ORDER BY L_ATC2
            """
        elif filter_type == 'atc3':
            query = f"""
                SELECT DISTINCT atc3, L_ATC3 
                FROM phmev 
                {where_sql}
                ORDER BY L_ATC3
            """
        elif filter_type == 'atc4':
            query = f"""
                SELECT DISTINCT atc4, L_ATC4 
                FROM phmev 
                {where_sql}
                ORDER BY L_ATC4
            """
        elif filter_type == 'atc5':
            query = f"""
                SELECT DISTINCT ATC5, L_ATC5 
                FROM phmev 
                {where_sql}
                ORDER BY L_ATC5
            """
        elif filter_type in ['villes', 'categories', 'etablissements', 'medicaments']:
            column_map = {
                'villes': 'ville',
                'categories': 'categorie', 
                'etablissements': 'etablissement',
                'medicaments': 'libelle_cip'
            }
            column = column_map[filter_type]
            query = f"""
                SELECT DISTINCT {column}
                FROM phmev 
                {where_sql}
                ORDER BY {column}
            """
        else:
            return []
        
        result = conn.execute(query, params).fetchall()
        
        if filter_type in ['atc1', 'atc2', 'atc3', 'atc4', 'atc5']:
            return [(row[0], row[1]) for row in result]
        else:
            return [row[0] for row in result]
            
    except Exception as e:
        st.error(f"Erreur lors de la récupération des options {filter_type}: {e}")
        return []

def get_filtered_data_duckdb(conn, filters, min_boites=0):
    """🔄 Applique les filtres et retourne les données"""
    if conn is None:
        return pd.DataFrame()
    
    try:
        where_clauses = []
        params = []
        
        # Construire les clauses WHERE pour tous les niveaux ATC
        if filters.get('atc1_filtre'):
            placeholders = ','.join(['?' for _ in filters['atc1_filtre']])
            where_clauses.append(f"l_atc1 IN ({placeholders})")
            params.extend(filters['atc1_filtre'])
            
        if filters.get('atc2_filtre'):
            placeholders = ','.join(['?' for _ in filters['atc2_filtre']])
            where_clauses.append(f"L_ATC2 IN ({placeholders})")
            params.extend(filters['atc2_filtre'])
            
        if filters.get('atc3_filtre'):
            placeholders = ','.join(['?' for _ in filters['atc3_filtre']])
            where_clauses.append(f"L_ATC3 IN ({placeholders})")
            params.extend(filters['atc3_filtre'])
            
        if filters.get('atc4_filtre'):
            placeholders = ','.join(['?' for _ in filters['atc4_filtre']])
            where_clauses.append(f"L_ATC4 IN ({placeholders})")
            params.extend(filters['atc4_filtre'])
            
        if filters.get('atc5_filtre'):
            placeholders = ','.join(['?' for _ in filters['atc5_filtre']])
            where_clauses.append(f"L_ATC5 IN ({placeholders})")
            params.extend(filters['atc5_filtre'])
            
        if filters.get('ville_filtre'):
            placeholders = ','.join(['?' for _ in filters['ville_filtre']])
            where_clauses.append(f"ville IN ({placeholders})")
            params.extend(filters['ville_filtre'])
            
        if filters.get('categorie_filtre'):
            placeholders = ','.join(['?' for _ in filters['categorie_filtre']])
            where_clauses.append(f"categorie IN ({placeholders})")
            params.extend(filters['categorie_filtre'])
            
        if filters.get('etablissement_filtre'):
            placeholders = ','.join(['?' for _ in filters['etablissement_filtre']])
            where_clauses.append(f"etablissement IN ({placeholders})")
            params.extend(filters['etablissement_filtre'])
            
        if filters.get('libelle_filtre'):
            placeholders = ','.join(['?' for _ in filters['libelle_filtre']])
            where_clauses.append(f"libelle_cip IN ({placeholders})")
            params.extend(filters['libelle_filtre'])
        
        # Filtre minimum de boîtes
        if min_boites > 0:
            where_clauses.append("BOITES >= ?")
            params.append(min_boites)
        
        where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        query = f"""
            SELECT *
            FROM phmev
            {where_sql}
        """
        
        result = conn.execute(query, params).fetchdf()
        return result
        
    except Exception as e:
        st.error(f"Erreur lors du filtrage: {e}")
        return pd.DataFrame()

def search_medications_duckdb(conn, search_term, max_results=50):
    """🔍 Recherche de médicaments avec DuckDB"""
    if conn is None or not search_term:
        return []
    
    try:
        # Recherche insensible à la casse avec LIKE
        search_pattern = f"%{search_term.lower()}%"
        
        query = """
            SELECT DISTINCT libelle_cip
            FROM phmev
            WHERE LOWER(libelle_cip) LIKE ?
            AND libelle_cip IS NOT NULL 
            AND libelle_cip != 'Non spécifié'
            ORDER BY 
                CASE WHEN LOWER(libelle_cip) LIKE ? THEN 1 ELSE 2 END,
                LENGTH(libelle_cip),
                libelle_cip
            LIMIT ?
        """
        
        exact_pattern = f"{search_term.lower()}%"
        result = conn.execute(query, [search_pattern, exact_pattern, max_results]).fetchall()
        
        return [row[0] for row in result]
        
    except Exception as e:
        st.error(f"Erreur lors de la recherche: {e}")
        return []

def main():
    """🎯 Application principale"""
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #667eea; font-size: 3rem; margin-bottom: 0.5rem;">
            🏥 PHMEV Analytics Pro
        </h1>
        <h3 style="color: #764ba2; font-weight: 300; margin-bottom: 2rem;">
            📊 Version DuckDB - Optimisée Mémoire
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données
    with st.spinner("🦆 Initialisation DuckDB..."):
        conn = load_data_duckdb()
    
    if conn is None:
        st.stop()
    
    # 🎛️ Sidebar ultra moderne avec filtres interdépendants complets
    with st.sidebar:
        st.markdown("## ⚡ **Filtres Interdépendants**")
        st.markdown("*Chaque sélection met à jour les autres filtres automatiquement*")
        
        # Initialiser les filtres actuels
        current_filters = {}
        
        # ========== HIÉRARCHIE PHARMACEUTIQUE D'ABORD ==========
        st.markdown("### 💊 **Hiérarchie Pharmaceutique (QUOI)**")
        st.markdown("*Sélectionnez d'abord les médicaments qui vous intéressent*")
        
        # Niveau 1: ATC1
        st.markdown("#### 🧬 **Systèmes Anatomiques (ATC1)**")
        atc1_options = get_filter_options_duckdb(conn, 'atc1', current_filters)
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
        atc2_options = get_filter_options_duckdb(conn, 'atc2', current_filters)
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
        atc3_options = get_filter_options_duckdb(conn, 'atc3', current_filters)
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
        atc4_options = get_filter_options_duckdb(conn, 'atc4', current_filters)
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
        atc5_options = get_filter_options_duckdb(conn, 'atc5', current_filters)
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
        medicaments_disponibles = get_filter_options_duckdb(conn, 'medicaments', current_filters)
        
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
        villes_disponibles = get_filter_options_duckdb(conn, 'villes', current_filters)
        
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
        categories_disponibles = get_filter_options_duckdb(conn, 'categories', current_filters)
        
        categorie_filtre = st.multiselect(
            f"Types d'établissement ({len(categories_disponibles)} disponibles)",
            options=categories_disponibles,
            default=[],
            key="categorie_multiselect_interdep"
        )
        current_filters['categorie_filtre'] = categorie_filtre
        
        # Établissements spécifiques
        st.markdown("#### 🏥 **Établissements Spécifiques**")
        etablissements_disponibles = get_filter_options_duckdb(conn, 'etablissements', current_filters)
        
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
            "🏆 Top N éléments",
            min_value=5,
            max_value=100,
            value=20,
            step=5,
            help="Nombre d'éléments dans chaque classement"
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
            
            show_charts = st.checkbox(
                "📊 Afficher les graphiques",
                value=True,
                help="Inclure les graphiques dans les analyses"
            )
    
    # 🔧 Application des filtres interdépendants
    with st.spinner("🔄 Application des filtres..."):
        df_filtered = get_filtered_data_duckdb(conn, current_filters, min_boites)
    
    # 📊 Indicateur de filtrage actif
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
    
    # Informations sur le dataset
    total_rows = conn.execute("SELECT COUNT(*) FROM phmev").fetchone()[0]
    
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
            <div style="display: flex; align-items: center; gap: 0.8rem;">
                <span style="font-size: 2rem;">🦆</span>
                <div>
                    <div style="font-weight: 700; color: white; font-size: 1.3rem;">
                        DuckDB Engine
                    </div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.8); text-transform: uppercase; letter-spacing: 0.5px;">
                        Optimisé mémoire
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
                                {len(df_filtered)/total_rows*100:.1f}%
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
                                {total_rows:,} lignes
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
    
    if df_filtered.empty:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
                    color: white; padding: 1.5rem; border-radius: 15px; text-align: center;
                    box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3); margin: 1rem 0;">
            <strong>⚠️ Aucune donnée trouvée</strong><br>
            Essayez de modifier vos filtres pour obtenir des résultats
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    # KPIs globaux filtrés
    st.markdown('## 💎 Métriques Filtrées')
    
    total_boites = df_filtered['BOITES'].sum()
    total_rem = df_filtered['REM'].sum()
    total_bse = df_filtered['BSE'].sum()
    nb_etablissements = df_filtered['etablissement'].nunique()
    
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
        <div class="kpi-card count">
            <div class="kpi-icon">🏥</div>
            <div class="kpi-value">{format_number(nb_etablissements)}</div>
            <div class="kpi-label">Établissements</div>
            <div class="kpi-delta">Établissements uniques</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        cout_moyen = total_rem / total_boites if total_boites > 0 else 0
        st.markdown(f"""
        <div class="kpi-card base">
            <div class="kpi-icon">💊</div>
            <div class="kpi-value">{format_currency(cout_moyen)}</div>
            <div class="kpi-label">Coût Moyen/Boîte</div>
            <div class="kpi-delta">Par boîte délivrée</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Les 3 tableaux principaux avec filtres
    st.markdown('## 📊 Analyses Principales')
    
    tab1, tab2, tab3 = st.tabs(["🏥 Top Établissements", "💊 Top Produits", "🧪 Top Molécules"])
    
    # TAB 1: Top Établissements
    with tab1:
        st.subheader(f"🏥 Top {top_n} Établissements par Remboursement")
        
        if len(df_filtered) > 0:
            # Grouper par établissement
            df_etabs = df_filtered.groupby(['etablissement', 'ville', 'categorie']).agg({
                'BOITES': 'sum',
                'REM': 'sum', 
                'BSE': 'sum'
            }).reset_index()
            
            # Calculer les métriques dérivées
            df_etabs['cout_moyen_boite'] = np.where(
                df_etabs['BOITES'] > 0, 
                df_etabs['REM'] / df_etabs['BOITES'], 
                0
            )
            df_etabs['taux_remb_moyen'] = np.where(
                df_etabs['BSE'] > 0, 
                (df_etabs['REM'] / df_etabs['BSE'] * 100), 
                0
            )
            
            df_etabs = df_etabs.nlargest(top_n, 'REM')
            
            # Formatage pour affichage
            df_etabs_display = df_etabs.copy()
            df_etabs_display['Total Boîtes'] = df_etabs_display['BOITES'].apply(format_number)
            df_etabs_display['Montant Remboursé'] = df_etabs_display['REM'].apply(format_currency)
            df_etabs_display['Base Remboursable'] = df_etabs_display['BSE'].apply(format_currency)
            df_etabs_display['Coût/Boîte'] = df_etabs_display['cout_moyen_boite'].apply(format_currency)
            df_etabs_display['Taux Remb.'] = df_etabs_display['taux_remb_moyen'].apply(lambda x: f"{x:.1f}%")
            
            # Colonnes à afficher
            cols_display = ['etablissement', 'ville', 'categorie', 'Total Boîtes', 'Montant Remboursé', 'Base Remboursable', 'Coût/Boîte', 'Taux Remb.']
            st.dataframe(df_etabs_display[cols_display], width='stretch', hide_index=True)
            
            # Graphique si activé
            if show_charts:
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
            
            # Export
            csv_etabs = df_etabs_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger Top Établissements",
                data=csv_etabs,
                file_name=f"top_{top_n}_etablissements_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Aucun établissement trouvé avec les filtres sélectionnés")
    
    # TAB 2: Top Produits
    with tab2:
        st.subheader(f"💊 Top {top_n} Produits par Remboursement")
        
        if len(df_filtered) > 0:
            # Grouper par produit
            df_produits = df_filtered.groupby(['libelle_cip', 'L_ATC5']).agg({
                'BOITES': 'sum',
                'REM': 'sum', 
                'BSE': 'sum',
                'etablissement': 'nunique'
            }).reset_index()
            
            df_produits.rename(columns={'libelle_cip': 'produit', 'L_ATC5': 'molecule', 'etablissement': 'nb_etablissements'}, inplace=True)
            
            # Calculer les métriques dérivées
            df_produits['cout_moyen_boite'] = np.where(
                df_produits['BOITES'] > 0, 
                df_produits['REM'] / df_produits['BOITES'], 
                0
            )
            df_produits['taux_remb_moyen'] = np.where(
                df_produits['BSE'] > 0, 
                (df_produits['REM'] / df_produits['BSE'] * 100), 
                0
            )
            
            df_produits = df_produits.nlargest(top_n, 'REM')
            
            # Formatage pour affichage
            df_produits_display = df_produits.copy()
            df_produits_display['Total Boîtes'] = df_produits_display['BOITES'].apply(format_number)
            df_produits_display['Montant Remboursé'] = df_produits_display['REM'].apply(format_currency)
            df_produits_display['Base Remboursable'] = df_produits_display['BSE'].apply(format_currency)
            df_produits_display['Coût/Boîte'] = df_produits_display['cout_moyen_boite'].apply(format_currency)
            df_produits_display['Taux Remb.'] = df_produits_display['taux_remb_moyen'].apply(lambda x: f"{x:.1f}%")
            df_produits_display['Nb Étab.'] = df_produits_display['nb_etablissements'].apply(format_number)
            
            # Colonnes à afficher
            cols_display = ['produit', 'molecule', 'Total Boîtes', 'Montant Remboursé', 'Base Remboursable', 'Coût/Boîte', 'Taux Remb.', 'Nb Étab.']
            st.dataframe(df_produits_display[cols_display], width='stretch', hide_index=True)
            
            # Graphique si activé
            if show_charts:
                fig = px.bar(
                    df_produits.head(15), 
                    x='REM', 
                    y='produit',
                    orientation='h',
                    title=f"Top 15 Produits par Remboursement",
                    labels={'REM': 'Montant Remboursé (€)', 'produit': 'Produit'},
                    color='REM',
                    color_continuous_scale='Greens'
                )
                fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Export
            csv_produits = df_produits_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger Top Produits",
                data=csv_produits,
                file_name=f"top_{top_n}_produits_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Aucun produit trouvé avec les filtres sélectionnés")
    
    # TAB 3: Top Molécules
    with tab3:
        st.subheader(f"🧪 Top {top_n} Molécules par Remboursement")
        
        if len(df_filtered) > 0:
            # Grouper par molécule
            df_molecules = df_filtered.groupby(['L_ATC5', 'l_atc1']).agg({
                'BOITES': 'sum',
                'REM': 'sum', 
                'BSE': 'sum',
                'libelle_cip': 'nunique',
                'etablissement': 'nunique'
            }).reset_index()
            
            df_molecules.rename(columns={
                'L_ATC5': 'molecule', 
                'l_atc1': 'systeme_anatomique',
                'libelle_cip': 'nb_produits',
                'etablissement': 'nb_etablissements'
            }, inplace=True)
            
            # Calculer les métriques dérivées
            df_molecules['cout_moyen_boite'] = np.where(
                df_molecules['BOITES'] > 0, 
                df_molecules['REM'] / df_molecules['BOITES'], 
                0
            )
            df_molecules['taux_remb_moyen'] = np.where(
                df_molecules['BSE'] > 0, 
                (df_molecules['REM'] / df_molecules['BSE'] * 100), 
                0
            )
            
            # Filtrer les molécules nulles
            df_molecules = df_molecules[df_molecules['molecule'].notna() & (df_molecules['molecule'] != '')]
            df_molecules = df_molecules.nlargest(top_n, 'REM')
            
            # Formatage pour affichage
            df_molecules_display = df_molecules.copy()
            df_molecules_display['Total Boîtes'] = df_molecules_display['BOITES'].apply(format_number)
            df_molecules_display['Montant Remboursé'] = df_molecules_display['REM'].apply(format_currency)
            df_molecules_display['Base Remboursable'] = df_molecules_display['BSE'].apply(format_currency)
            df_molecules_display['Coût/Boîte'] = df_molecules_display['cout_moyen_boite'].apply(format_currency)
            df_molecules_display['Taux Remb.'] = df_molecules_display['taux_remb_moyen'].apply(lambda x: f"{x:.1f}%")
            df_molecules_display['Nb Produits'] = df_molecules_display['nb_produits'].apply(format_number)
            df_molecules_display['Nb Étab.'] = df_molecules_display['nb_etablissements'].apply(format_number)
            
            # Colonnes à afficher
            cols_display = ['molecule', 'systeme_anatomique', 'Total Boîtes', 'Montant Remboursé', 'Base Remboursable', 'Coût/Boîte', 'Taux Remb.', 'Nb Produits', 'Nb Étab.']
            st.dataframe(df_molecules_display[cols_display], width='stretch', hide_index=True)
            
            # Graphique si activé
            if show_charts:
                fig = px.bar(
                    df_molecules.head(15), 
                    x='REM', 
                    y='molecule',
                    orientation='h',
                    title=f"Top 15 Molécules par Remboursement",
                    labels={'REM': 'Montant Remboursé (€)', 'molecule': 'Molécule'},
                    color='REM',
                    color_continuous_scale='Reds'
                )
                fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Export
            csv_molecules = df_molecules_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger Top Molécules",
                data=csv_molecules,
                file_name=f"top_{top_n}_molecules_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Aucune molécule trouvée avec les filtres sélectionnés")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        🦆 <strong>PHMEV Analytics Pro - DuckDB Edition</strong><br>
        Optimisé pour la performance et la gestion mémoire<br>
        <em>Données PHMEV • Version {}</em>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
