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
    """📊 Obtient les options de filtres avec DuckDB"""
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
                
            if current_filters.get('ville_filtre'):
                placeholders = ','.join(['?' for _ in current_filters['ville_filtre']])
                where_clauses.append(f"ville IN ({placeholders})")
                params.extend(current_filters['ville_filtre'])
        
        # Ajouter les conditions spécifiques au type de filtre
        if filter_type == 'atc1':
            where_clauses.append("atc1 IS NOT NULL AND l_atc1 IS NOT NULL")
        elif filter_type == 'atc5':
            where_clauses.append("ATC5 IS NOT NULL AND L_ATC5 IS NOT NULL")
        elif filter_type == 'villes':
            where_clauses.append("ville IS NOT NULL AND ville != 'Non spécifiée'")
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
        elif filter_type == 'atc5':
            query = f"""
                SELECT DISTINCT ATC5, L_ATC5 
                FROM phmev 
                {where_sql}
                ORDER BY L_ATC5
            """
        elif filter_type == 'villes':
            query = f"""
                SELECT DISTINCT ville 
                FROM phmev 
                {where_sql}
                ORDER BY ville
            """
        elif filter_type == 'etablissements':
            query = f"""
                SELECT DISTINCT etablissement 
                FROM phmev 
                {where_sql}
                ORDER BY etablissement
            """
        elif filter_type == 'medicaments':
            query = f"""
                SELECT DISTINCT libelle_cip 
                FROM phmev 
                {where_sql}
                ORDER BY libelle_cip
            """
        else:
            return []
        
        result = conn.execute(query, params).fetchall()
        
        if filter_type in ['atc1', 'atc5']:
            return [(row[0], row[1]) for row in result]
        else:
            return [row[0] for row in result]
            
    except Exception as e:
        st.error(f"Erreur lors de la récupération des options {filter_type}: {e}")
        return []

def get_filtered_data_duckdb(conn, filters):
    """🔄 Applique les filtres et retourne les données"""
    if conn is None:
        return pd.DataFrame()
    
    try:
        where_clauses = []
        params = []
        
        # Construire les clauses WHERE
        if filters.get('atc1_filtre'):
            placeholders = ','.join(['?' for _ in filters['atc1_filtre']])
            where_clauses.append(f"l_atc1 IN ({placeholders})")
            params.extend(filters['atc1_filtre'])
            
        if filters.get('atc5_filtre'):
            placeholders = ','.join(['?' for _ in filters['atc5_filtre']])
            where_clauses.append(f"L_ATC5 IN ({placeholders})")
            params.extend(filters['atc5_filtre'])
            
        if filters.get('ville_filtre'):
            placeholders = ','.join(['?' for _ in filters['ville_filtre']])
            where_clauses.append(f"ville IN ({placeholders})")
            params.extend(filters['ville_filtre'])
            
        if filters.get('etablissement_filtre'):
            placeholders = ','.join(['?' for _ in filters['etablissement_filtre']])
            where_clauses.append(f"etablissement IN ({placeholders})")
            params.extend(filters['etablissement_filtre'])
            
        if filters.get('libelle_filtre'):
            placeholders = ','.join(['?' for _ in filters['libelle_filtre']])
            where_clauses.append(f"libelle_cip IN ({placeholders})")
            params.extend(filters['libelle_filtre'])
        
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
    
    # Sidebar pour les filtres
    with st.sidebar:
        st.header("🔍 Filtres")
        
        # Initialiser les filtres dans session_state
        if 'filters' not in st.session_state:
            st.session_state.filters = {}
        
        # Filtre ATC1
        st.subheader("🧬 Classification ATC")
        atc1_options = get_filter_options_duckdb(conn, 'atc1')
        if atc1_options:
            atc1_labels = [f"{code} - {label}" for code, label in atc1_options]
            atc1_selected = st.multiselect(
                "Niveau ATC 1:",
                options=atc1_labels,
                key="atc1_select"
            )
            st.session_state.filters['atc1_filtre'] = [
                label.split(' - ')[1] for label in atc1_selected
            ] if atc1_selected else []
        
        # Filtre Ville
        st.subheader("🏙️ Géographie")
        ville_options = get_filter_options_duckdb(conn, 'villes', st.session_state.filters)
        if ville_options:
            ville_selected = st.multiselect(
                "Villes:",
                options=ville_options[:100],  # Limiter pour performance
                key="ville_select"
            )
            st.session_state.filters['ville_filtre'] = ville_selected
        
        # Recherche de médicaments
        st.subheader("💊 Médicaments")
        search_term = st.text_input("🔍 Rechercher un médicament:", key="med_search")
        
        if search_term:
            med_results = search_medications_duckdb(conn, search_term)
            if med_results:
                med_selected = st.multiselect(
                    f"Résultats pour '{search_term}':",
                    options=med_results,
                    key="med_select"
                )
                st.session_state.filters['libelle_filtre'] = med_selected
            else:
                st.warning(f"❌ Aucun médicament trouvé pour '{search_term}'")
    
    # Obtenir les données filtrées
    with st.spinner("🔄 Application des filtres..."):
        df_filtered = get_filtered_data_duckdb(conn, st.session_state.filters)
    
    if df_filtered.empty:
        st.warning("⚠️ Aucune donnée ne correspond aux filtres sélectionnés")
        st.stop()
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📊 Lignes filtrées",
            f"{len(df_filtered):,}",
            delta=f"{len(df_filtered):,} lignes"
        )
    
    with col2:
        total_rem = df_filtered['REM'].sum()
        st.metric(
            "💰 Montant Total Remboursé",
            f"{total_rem:,.2f}€",
            delta=f"{total_rem/1000000:.1f}M€"
        )
    
    with col3:
        total_boites = df_filtered['BOITES'].sum()
        st.metric(
            "📦 Total Boîtes",
            f"{total_boites:,.0f}",
            delta=f"{total_boites/1000:.0f}K boîtes"
        )
    
    with col4:
        if total_boites > 0:
            cout_moyen = total_rem / total_boites
            st.metric(
                "💊 Coût Moyen/Boîte",
                f"{cout_moyen:.2f}€",
                delta=f"Par boîte"
            )
    
    # Graphiques
    st.header("📈 Analyses")
    
    tab1, tab2, tab3 = st.tabs(["🏆 Top Médicaments", "🏙️ Répartition Géographique", "📊 Évolution Temporelle"])
    
    with tab1:
        if len(df_filtered) > 0:
            # Top 10 médicaments par remboursement
            top_meds = (df_filtered.groupby('libelle_cip')
                       .agg({'REM': 'sum', 'BOITES': 'sum'})
                       .sort_values('REM', ascending=False)
                       .head(10))
            
            fig = px.bar(
                x=top_meds.index,
                y=top_meds['REM'],
                title="🏆 Top 10 Médicaments par Remboursement",
                labels={'x': 'Médicament', 'y': 'Montant Remboursé (€)'}
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Tableau détaillé
            st.subheader("📋 Détail des Top Médicaments")
            top_meds['Coût/Boîte'] = top_meds['REM'] / top_meds['BOITES']
            st.dataframe(
                top_meds.round(2),
                use_container_width=True
            )
    
    with tab2:
        if len(df_filtered) > 0:
            # Répartition par ville (top 15)
            ville_stats = (df_filtered.groupby('ville')
                          .agg({'REM': 'sum', 'BOITES': 'sum'})
                          .sort_values('REM', ascending=False)
                          .head(15))
            
            fig = px.pie(
                values=ville_stats['REM'],
                names=ville_stats.index,
                title="🏙️ Répartition du Remboursement par Ville (Top 15)"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.info("📅 Évolution temporelle - Nécessite des données de date")
        st.write("Cette section sera développée avec des données temporelles")
    
    # Tableau des données filtrées (échantillon)
    st.header("📋 Données Détaillées")
    
    if len(df_filtered) > 1000:
        st.info(f"📊 Affichage d'un échantillon de 1000 lignes sur {len(df_filtered):,} total")
        sample_df = df_filtered.head(1000)
    else:
        sample_df = df_filtered
    
    # Colonnes importantes à afficher
    display_cols = ['libelle_cip', 'ville', 'etablissement', 'REM', 'BSE', 'BOITES', 'taux_remboursement']
    available_cols = [col for col in display_cols if col in sample_df.columns]
    
    st.dataframe(
        sample_df[available_cols].round(2),
        use_container_width=True
    )
    
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
