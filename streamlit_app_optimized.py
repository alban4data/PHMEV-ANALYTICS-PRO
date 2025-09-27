"""
🏥 PHMEV Analytics Pro - Version BigQuery Ultra-Optimisée
TOP N directement calculé dans BigQuery - Performance maximale
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

# Configuration de la page
st.set_page_config(
    page_title="🏥 PHMEV Analytics Pro - Optimisé",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS moderne
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.kpi-container {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    border-left: 5px solid #667eea;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

.kpi-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: #667eea;
    margin: 0;
}

.kpi-label {
    color: #666;
    font-size: 1rem;
    margin-top: 0.5rem;
}

[data-testid="stDataFrame"] th {
    background-color: #667eea !important;
    color: white !important;
    font-weight: bold !important;
}

[data-testid="stDataFrame"] td {
    background-color: white !important;
    color: black !important;
}

[data-testid="stDataFrame"] tr:nth-child(even) td {
    background-color: #f8f9fa !important;
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
    try:
        if "gcp_service_account" in st.secrets:
            credentials_info = st.secrets["gcp_service_account"]
            credentials = service_account.Credentials.from_service_account_info(credentials_info)
            client = bigquery.Client(credentials=credentials, project=credentials_info["project_id"])
            return client, credentials_info["project_id"]
        else:
            client = bigquery.Client(project='test-db-473321')
            return client, 'test-db-473321'
    except Exception as e:
        st.error(f"❌ Erreur de connexion BigQuery: {e}")
        return None, None

@st.cache_data(ttl=3600)
def get_filter_options():
    """Récupère les options de filtres de façon optimisée"""
    client, project_id = init_bigquery()
    if not client:
        return {}
    
    try:
        # Requêtes séparées pour chaque type d'option (plus rapide)
        
        # 1. Options ATC (hiérarchiques)
        atc_query = f"""
        SELECT DISTINCT atc1, l_atc1, atc2, L_ATC2, atc3, L_ATC3, atc4, L_ATC4, ATC5, L_ATC5
        FROM `{project_id}.dataset.PHMEV2024`
        WHERE l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')
        AND l_cip13 IS NOT NULL
        AND atc1 IS NOT NULL
        """
        
        # 2. Options géographiques et organisationnelles
        geo_query = f"""
        SELECT DISTINCT
            COALESCE(NULLIF(nom_ville, ''), 'Non spécifiée') as ville,
            COALESCE(NULLIF(categorie_jur, ''), 'Non spécifiée') as categorie,
            COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié') as etablissement
        FROM `{project_id}.dataset.PHMEV2024`
        WHERE l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')
        AND l_cip13 IS NOT NULL
        """
        
        # 3. Options médicaments
        med_query = f"""
        SELECT DISTINCT COALESCE(NULLIF(L_ATC5, ''), 'Non spécifié') as medicament
        FROM `{project_id}.dataset.PHMEV2024`
        WHERE l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')
        AND l_cip13 IS NOT NULL
        AND L_ATC5 IS NOT NULL
        """
        
        # Exécuter les requêtes en parallèle (conceptuellement)
        df_atc = client.query(atc_query).to_dataframe()
        df_geo = client.query(geo_query).to_dataframe()  
        df_med = client.query(med_query).to_dataframe()
        
        # Construire les options hiérarchiques
        options = {
            'atc1': sorted([(row['atc1'], row['l_atc1']) for _, row in df_atc[['atc1', 'l_atc1']].dropna().drop_duplicates().iterrows()]),
            'atc2': sorted([(row['atc2'], row['L_ATC2']) for _, row in df_atc[['atc2', 'L_ATC2']].dropna().drop_duplicates().iterrows()]) if 'atc2' in df_atc.columns else [],
            'atc3': sorted([(row['atc3'], row['L_ATC3']) for _, row in df_atc[['atc3', 'L_ATC3']].dropna().drop_duplicates().iterrows()]) if 'atc3' in df_atc.columns else [],
            'atc4': sorted([(row['atc4'], row['L_ATC4']) for _, row in df_atc[['atc4', 'L_ATC4']].dropna().drop_duplicates().iterrows()]) if 'atc4' in df_atc.columns else [],
            'atc5': sorted([(row['ATC5'], row['L_ATC5']) for _, row in df_atc[['ATC5', 'L_ATC5']].dropna().drop_duplicates().iterrows()]) if 'ATC5' in df_atc.columns else [],
            'villes': sorted(df_geo['ville'].dropna().unique().tolist()),
            'categories': sorted(df_geo['categorie'].dropna().unique().tolist()),
            'etablissements': sorted(df_geo['etablissement'].dropna().unique().tolist()),
            'medicaments': sorted(df_med['medicament'].dropna().unique().tolist())
        }
        
        return options
        
    except Exception as e:
        st.error(f"❌ Erreur options: {e}")
        return {}

def build_where_clause(filters):
    where_conditions = [
        "l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')",
        "l_cip13 IS NOT NULL"
    ]
    
    # Filtres ATC hiérarchiques
    if filters.get('atc1'):
        atc1_list = "', '".join(filters['atc1'])
        where_conditions.append(f"atc1 IN ('{atc1_list}')")
    
    if filters.get('atc2'):
        atc2_list = "', '".join(filters['atc2'])
        where_conditions.append(f"atc2 IN ('{atc2_list}')")
    
    if filters.get('atc3'):
        atc3_list = "', '".join(filters['atc3'])
        where_conditions.append(f"atc3 IN ('{atc3_list}')")
    
    if filters.get('atc4'):
        atc4_list = "', '".join(filters['atc4'])
        where_conditions.append(f"atc4 IN ('{atc4_list}')")
    
    if filters.get('atc5'):
        atc5_list = "', '".join(filters['atc5'])
        where_conditions.append(f"ATC5 IN ('{atc5_list}')")
    
    # Filtres géographiques et organisationnels
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
    
    return " AND ".join(where_conditions)

def get_kpis(filters):
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
            COUNT(DISTINCT COALESCE(NULLIF(L_ATC5, ''), 'Non spécifié')) as nb_medicaments,
            COUNT(DISTINCT COALESCE(NULLIF(nom_ville, ''), 'Non spécifiée')) as nb_villes
        FROM `{project_id}.dataset.PHMEV2024`
        WHERE {where_clause}
        """
        
        result = client.query(query).to_dataframe()
        return result.iloc[0].to_dict() if len(result) > 0 else {}
    except Exception as e:
        st.error(f"❌ Erreur KPIs: {e}")
        return {}

def get_top_etablissements(filters, limit=50):
    client, project_id = init_bigquery()
    if not client:
        return pd.DataFrame()
    
    try:
        where_clause = build_where_clause(filters)
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
        
        return client.query(query).to_dataframe()
    except Exception as e:
        st.error(f"❌ Erreur établissements: {e}")
        return pd.DataFrame()

def get_top_medicaments(filters, limit=50):
    client, project_id = init_bigquery()
    if not client:
        return pd.DataFrame()
    
    try:
        where_clause = build_where_clause(filters)
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
        st.error(f"❌ Erreur médicaments: {e}")
        return pd.DataFrame()

def get_top_molecules(filters, limit=50):
    client, project_id = init_bigquery()
    if not client:
        return pd.DataFrame()
    
    try:
        where_clause = build_where_clause(filters)
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
        st.error(f"❌ Erreur molécules: {e}")
        return pd.DataFrame()

def main():
    # En-tête
    st.markdown("""
    <div class="main-header">
        <h1>🏥 PHMEV Analytics Pro - Ultra-Optimisé</h1>
        <p>TOP N calculé directement dans BigQuery - Performance maximale</p>
        <p><small>⚡ Chaque filtre = requête SQL optimisée</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des options de filtres
    with st.spinner("🚀 Chargement des options de filtres..."):
        filter_options = get_filter_options()
    
    if not filter_options:
        st.error("❌ Impossible de charger les options")
        return
    
    # Sidebar - Filtres
    st.sidebar.header("🎛️ Filtres")
    
    filters = {}
    
    # Filtre ATC1
    atc1_options = filter_options.get('atc1', [])
    filters['atc1'] = st.sidebar.multiselect(
        "🧬 Classification ATC1", 
        options=[code for code, label in atc1_options],
        format_func=lambda x: f"{x} - {dict(atc1_options).get(x, x)}"
    )
    
    # Filtre Ville
    filters['villes'] = st.sidebar.multiselect(
        "🏙️ Villes", 
        options=filter_options.get('villes', [])
    )
    
    # Filtre Catégorie
    filters['categories'] = st.sidebar.multiselect(
        "🏥 Catégories", 
        options=filter_options.get('categories', [])
    )
    
    # Filtre Établissement
    filters['etablissements'] = st.sidebar.multiselect(
        "🏢 Établissements", 
        options=filter_options.get('etablissements', [])
    )
    
    # Recherche médicament
    search_term = st.sidebar.text_input("🔍 Rechercher un médicament", placeholder="Ex: cabome...")
    med_options = filter_options.get('medicaments', [])
    if search_term:
        med_options = [med for med in med_options if search_term.lower() in med.lower()]
    
    filters['medicaments'] = st.sidebar.multiselect(
        "💊 Médicaments", 
        options=med_options
    )
    
    # Filtre nombre de boîtes
    filters['min_boites'] = st.sidebar.number_input(
        "📦 Nombre minimum de boîtes", 
        min_value=0, 
        value=0
    )
    
    # Chargement des KPIs
    with st.spinner("📊 Calcul des KPIs..."):
        kpis = get_kpis(filters)
    
    # Affichage KPIs
    if kpis:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_currency(kpis.get('total_rem', 0))}</div>
                <div class="kpi-label">💰 Montant Total Remboursé</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{format_number(kpis.get('total_boites', 0))}</div>
                <div class="kpi-label">📦 Boîtes Totales</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{kpis.get('nb_etablissements', 0)}</div>
                <div class="kpi-label">🏥 Établissements</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{kpis.get('nb_medicaments', 0)}</div>
                <div class="kpi-label">💊 Médicaments</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.info(f"📊 **{kpis.get('total_lignes', 0):,}** lignes trouvées avec les filtres appliqués")
    
    # Onglets pour les 3 tableaux
    tab1, tab2, tab3 = st.tabs(["🏥 Top Établissements", "💊 Top Produits", "🧬 Top Molécules"])
    
    with tab1:
        st.subheader("🏥 Top Établissements par Remboursement")
        
        # Options
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            limit_etabs = st.selectbox("Nombre à afficher", [20, 50, 100], index=0, key="limit_etabs")
        with col_opt2:
            show_chart_etabs = st.checkbox("📊 Graphique", value=True, key="chart_etabs")
        
        # Chargement données
        with st.spinner("🏥 Chargement TOP établissements..."):
            df_etabs = get_top_etablissements(filters, limit_etabs)
        
        if len(df_etabs) > 0:
            # Formatage
            df_display = df_etabs.copy()
            df_display['REM'] = df_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['BSE'] = df_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['cout_par_boite'] = df_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['taux_remboursement'] = df_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            df_display['BOITES'] = df_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            df_display.columns = ['Établissement', 'Ville', 'Catégorie', 'Montant Remboursé', 'Base Remboursable', 'Boîtes', 'Coût/Boîte', 'Taux Remb.']
            
            st.dataframe(df_display, use_container_width=True)
            
            # Graphique
            if show_chart_etabs:
                fig = px.bar(
                    df_etabs.head(10), 
                    x='REM', 
                    y='etablissement',
                    orientation='h',
                    title=f"Top 10 Établissements"
                )
                fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Export
            csv = df_display.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger", csv, f"etablissements_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
        else:
            st.warning("Aucun établissement trouvé")
    
    with tab2:
        st.subheader("💊 Top Produits par Remboursement")
        
        # Options
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            limit_meds = st.selectbox("Nombre à afficher", [20, 50, 100], index=0, key="limit_meds")
        with col_opt2:
            show_chart_meds = st.checkbox("📊 Graphique", value=True, key="chart_meds")
        
        # Chargement données
        with st.spinner("💊 Chargement TOP médicaments..."):
            df_meds = get_top_medicaments(filters, limit_meds)
        
        if len(df_meds) > 0:
            # Formatage
            df_display = df_meds.copy()
            df_display['REM'] = df_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['BSE'] = df_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['cout_par_boite'] = df_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['taux_remboursement'] = df_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            df_display['BOITES'] = df_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            df_display.columns = ['Médicament', 'ATC1', 'Libellé ATC1', 'Montant Remboursé', 'Base Remboursable', 'Boîtes', 'Nb Établissements', 'Coût/Boîte', 'Taux Remb.']
            
            st.dataframe(df_display, use_container_width=True)
            
            # Graphique
            if show_chart_meds:
                fig = px.bar(
                    df_meds.head(10), 
                    x='REM', 
                    y='medicament',
                    orientation='h',
                    title=f"Top 10 Médicaments"
                )
                fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Export
            csv = df_display.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger", csv, f"medicaments_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", key="dl_meds")
        else:
            st.warning("Aucun médicament trouvé")
    
    with tab3:
        st.subheader("🧬 Top Molécules par Remboursement")
        
        # Options
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            limit_mols = st.selectbox("Nombre à afficher", [20, 50, 100], index=0, key="limit_mols")
        with col_opt2:
            show_chart_mols = st.checkbox("📊 Graphique", value=True, key="chart_mols")
        
        # Chargement données
        with st.spinner("🧬 Chargement TOP molécules..."):
            df_mols = get_top_molecules(filters, limit_mols)
        
        if len(df_mols) > 0:
            # Formatage
            df_display = df_mols.copy()
            df_display['REM'] = df_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['BSE'] = df_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['cout_par_boite'] = df_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_display['taux_remboursement'] = df_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            df_display['BOITES'] = df_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            df_display.columns = ['Molécule', 'ATC1', 'Libellé ATC1', 'Montant Remboursé', 'Base Remboursable', 'Boîtes', 'Nb Établissements', 'Coût/Boîte', 'Taux Remb.']
            
            st.dataframe(df_display, use_container_width=True)
            
            # Graphique
            if show_chart_mols:
                fig = px.bar(
                    df_mols.head(10), 
                    x='REM', 
                    y='molecule',
                    orientation='h',
                    title=f"Top 10 Molécules"
                )
                fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Export
            csv = df_display.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger", csv, f"molecules_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", key="dl_mols")
        else:
            st.warning("Aucune molécule trouvée")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🏥 <strong>PHMEV Analytics Pro - Ultra-Optimisé</strong></p>
        <p>⚡ TOP N calculé directement dans BigQuery | 🚀 Performance maximale</p>
        <p><small>Chaque filtre déclenche une requête SQL optimisée</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
