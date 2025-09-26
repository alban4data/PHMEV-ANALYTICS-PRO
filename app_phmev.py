"""
Application Streamlit pour l'analyse des données PHMEV
Analyse des délivrances pharmaceutiques par établissement
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

# Configuration de la page
st.set_page_config(
    page_title="Analyse PHMEV - Délivrances Pharmaceutiques",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .filter-section {
        background-color: #fafafa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(nrows=1000000):
    """Charge les données PHMEV avec cache"""
    try:
        df = pd.read_csv(
            'OPEN_PHMEV_2024.CSV', 
            nrows=nrows, 
            encoding='latin1', 
            sep=';',
            low_memory=False
        )
        
        # Nettoyage des données
        df['REM'] = pd.to_numeric(df['REM'].astype(str).str.replace(',', '.'), errors='coerce')
        df['BSE'] = pd.to_numeric(df['BSE'].astype(str).str.replace(',', '.'), errors='coerce')
        
        # Création de colonnes dérivées pour faciliter l'analyse
        df['etablissement'] = df['nom_etb'].fillna(df['raison_sociale_etb'])
        df['medicament'] = df['L_ATC5'].fillna('Non spécifié')
        df['categorie'] = df['categorie_jur'].fillna('Non spécifiée')
        
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return None

def format_number(value):
    """Formate les nombres avec des séparateurs de milliers"""
    if pd.isna(value):
        return "N/A"
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return f"{value:,.0f}"

def format_currency(value):
    """Formate les montants en euros"""
    if pd.isna(value):
        return "N/A"
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M€"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K€"
    else:
        return f"{value:,.2f}€"

def main():
    # En-tête principal
    st.markdown('<h1 class="main-header">📊 Analyse PHMEV - Délivrances Pharmaceutiques</h1>', 
                unsafe_allow_html=True)
    
    # Chargement des données
    with st.spinner("Chargement des données PHMEV..."):
        df = load_data()
    
    if df is None:
        st.stop()
    
    st.success(f"✅ Données chargées: {len(df):,} lignes")
    
    # Sidebar - Filtres
    st.sidebar.markdown("## 🔍 Filtres")
    
    # Filtre par médicament
    medicaments_uniques = sorted(df['medicament'].dropna().unique())
    medicament_filtre = st.sidebar.multiselect(
        "Sélectionner les médicaments (ATC5)",
        options=medicaments_uniques,
        default=[],
        help="Laissez vide pour inclure tous les médicaments"
    )
    
    # Filtre par catégorie d'établissement
    categories_uniques = sorted(df['categorie'].dropna().unique())
    categorie_filtre = st.sidebar.multiselect(
        "Sélectionner les catégories d'établissement",
        options=categories_uniques,
        default=[],
        help="Laissez vide pour inclure toutes les catégories"
    )
    
    # Filtre par établissement
    etablissements_uniques = sorted(df['etablissement'].dropna().unique())
    if len(etablissements_uniques) > 1000:  # Limiter si trop d'établissements
        st.sidebar.info("⚠️ Plus de 1000 établissements disponibles. Utilisez la recherche.")
        etablissement_search = st.sidebar.text_input(
            "Rechercher un établissement",
            help="Tapez pour filtrer les établissements"
        )
        if etablissement_search:
            etablissements_filtered = [e for e in etablissements_uniques 
                                     if etablissement_search.lower() in e.lower()][:50]
        else:
            etablissements_filtered = etablissements_uniques[:50]
    else:
        etablissements_filtered = etablissements_uniques
    
    etablissement_filtre = st.sidebar.multiselect(
        "Sélectionner les établissements",
        options=etablissements_filtered,
        default=[],
        help="Laissez vide pour inclure tous les établissements"
    )
    
    # Filtre Top N
    top_n = st.sidebar.slider(
        "Top N établissements à afficher",
        min_value=5,
        max_value=100,
        value=20,
        step=5,
        help="Nombre d'établissements à afficher dans le classement"
    )
    
    # Application des filtres
    df_filtered = df.copy()
    
    if medicament_filtre:
        df_filtered = df_filtered[df_filtered['medicament'].isin(medicament_filtre)]
    
    if categorie_filtre:
        df_filtered = df_filtered[df_filtered['categorie'].isin(categorie_filtre)]
    
    if etablissement_filtre:
        df_filtered = df_filtered[df_filtered['etablissement'].isin(etablissement_filtre)]
    
    if len(df_filtered) == 0:
        st.warning("⚠️ Aucune donnée ne correspond aux filtres sélectionnés.")
        st.stop()
    
    # Métriques globales
    st.markdown("## 📈 Métriques Globales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_boites = df_filtered['BOITES'].sum()
    total_rem = df_filtered['REM'].sum()
    total_bse = df_filtered['BSE'].sum()
    nb_etablissements = df_filtered['etablissement'].nunique()
    
    with col1:
        st.metric(
            "Total Boîtes Délivrées",
            format_number(total_boites),
            help="Nombre total de boîtes délivrées"
        )
    
    with col2:
        st.metric(
            "Montant Remboursé",
            format_currency(total_rem),
            help="Montant total remboursé par l'Assurance Maladie"
        )
    
    with col3:
        st.metric(
            "Montant Remboursable",
            format_currency(total_bse),
            help="Montant total remboursable"
        )
    
    with col4:
        st.metric(
            "Établissements",
            f"{nb_etablissements:,}",
            help="Nombre d'établissements uniques"
        )
    
    # Analyse par établissement
    st.markdown(f"## 🏥 Top {top_n} Établissements")
    
    # Agrégation par établissement
    df_etb = df_filtered.groupby(['etablissement', 'categorie']).agg({
        'BOITES': 'sum',
        'REM': 'sum',
        'BSE': 'sum'
    }).reset_index()
    
    # Calcul des pourcentages
    df_etb['pct_boites'] = (df_etb['BOITES'] / total_boites * 100).round(2)
    df_etb['pct_rem'] = (df_etb['REM'] / total_rem * 100).round(2)
    df_etb['pct_bse'] = (df_etb['BSE'] / total_bse * 100).round(2)
    
    # Tri et sélection du top N
    df_top = df_etb.nlargest(top_n, 'BOITES')
    
    # Tableau détaillé
    st.markdown("### 📋 Tableau détaillé")
    
    # Formatage du tableau
    df_display = df_top.copy()
    df_display['Boîtes'] = df_display['BOITES'].apply(format_number)
    df_display['% Boîtes'] = df_display['pct_boites'].apply(lambda x: f"{x}%")
    df_display['Remboursé'] = df_display['REM'].apply(format_currency)
    df_display['% Remboursé'] = df_display['pct_rem'].apply(lambda x: f"{x}%")
    df_display['Remboursable'] = df_display['BSE'].apply(format_currency)
    df_display['% Remboursable'] = df_display['pct_bse'].apply(lambda x: f"{x}%")
    
    table_display = df_display[['etablissement', 'categorie', 'Boîtes', '% Boîtes', 
                               'Remboursé', '% Remboursé', 'Remboursable', '% Remboursable']]
    table_display.columns = ['Établissement', 'Catégorie', 'Boîtes', '% Boîtes', 
                            'Remboursé', '% Remb.', 'Remboursable', '% Rembours.']
    
    st.dataframe(
        table_display,
        use_container_width=True,
        hide_index=True
    )
    
    # Visualisations
    st.markdown("### 📊 Visualisations")
    
    # Graphique en barres - Top établissements par boîtes
    fig_bars = px.bar(
        df_top.head(15),
        x='BOITES',
        y='etablissement',
        color='categorie',
        title=f"Top 15 Établissements par Nombre de Boîtes Délivrées",
        labels={'BOITES': 'Nombre de Boîtes', 'etablissement': 'Établissement'},
        orientation='h'
    )
    fig_bars.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_bars, use_container_width=True)
    
    # Graphiques en secteurs
    col1, col2 = st.columns(2)
    
    with col1:
        # Répartition par catégorie d'établissement
        df_cat = df_filtered.groupby('categorie')['BOITES'].sum().reset_index()
        df_cat = df_cat.nlargest(8, 'BOITES')  # Top 8 catégories
        
        fig_pie_cat = px.pie(
            df_cat,
            values='BOITES',
            names='categorie',
            title="Répartition des Boîtes par Catégorie d'Établissement"
        )
        st.plotly_chart(fig_pie_cat, use_container_width=True)
    
    with col2:
        # Répartition des montants (Remboursé vs Remboursable)
        montants_data = pd.DataFrame({
            'Type': ['Montant Remboursé', 'Montant Remboursable'],
            'Montant': [total_rem, total_bse]
        })
        
        fig_pie_montant = px.pie(
            montants_data,
            values='Montant',
            names='Type',
            title="Répartition Remboursé vs Remboursable",
            color_discrete_sequence=['#ff7f0e', '#1f77b4']
        )
        st.plotly_chart(fig_pie_montant, use_container_width=True)
    
    # Analyse des médicaments si filtrés
    if medicament_filtre:
        st.markdown("### 💊 Analyse des Médicaments Sélectionnés")
        
        df_med = df_filtered.groupby('medicament').agg({
            'BOITES': 'sum',
            'REM': 'sum',
            'BSE': 'sum',
            'etablissement': 'nunique'
        }).reset_index()
        df_med.columns = ['Médicament', 'Boîtes', 'Remboursé', 'Remboursable', 'Nb Établissements']
        
        st.dataframe(df_med, use_container_width=True, hide_index=True)
    
    # Section d'export
    st.markdown("## 💾 Export des Données")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export du tableau principal
        csv_data = df_top.to_csv(index=False, encoding='utf-8-sig', sep=';')
        st.download_button(
            label="📥 Télécharger Top Établissements (CSV)",
            data=csv_data,
            file_name=f"top_{top_n}_etablissements_phmev_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Export des données filtrées complètes
        if len(df_filtered) <= 100000:  # Limite pour éviter les gros fichiers
            csv_filtered = df_filtered.to_csv(index=False, encoding='utf-8-sig', sep=';')
            st.download_button(
                label="📥 Télécharger Données Filtrées (CSV)",
                data=csv_filtered,
                file_name=f"donnees_filtrees_phmev_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        else:
            st.info(f"⚠️ Données filtrées trop volumineuses ({len(df_filtered):,} lignes). Affinez les filtres pour l'export.")
    
    # Informations sur les données
    with st.expander("ℹ️ Informations sur les données"):
        st.markdown(f"""
        **Données chargées:** {len(df):,} lignes  
        **Données après filtrage:** {len(df_filtered):,} lignes  
        **Période:** 2024  
        **Source:** OPEN_PHMEV_2024.CSV  
        
        **Colonnes principales:**
        - **BOITES:** Nombre de boîtes délivrées
        - **REM:** Montant remboursé par l'Assurance Maladie
        - **BSE:** Montant remboursable (base de remboursement)
        - **ATC5/L_ATC5:** Classification ATC niveau 5 (médicament)
        - **categorie_jur:** Catégorie juridique de l'établissement
        
        **Note:** Cette application utilise un échantillon d'1 million de lignes pour des performances optimales.
        """)

if __name__ == "__main__":
    main()
