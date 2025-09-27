"""
🏥 PHMEV Analytics Pro - Version Cloud Optimisée
Application d'analyse des données pharmaceutiques PHMEV avec DuckDB
Version allégée pour Streamlit Cloud
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
import gc
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="🏥 PHMEV Analytics Pro - Cloud",
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
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 0.5rem 0;
}

.kpi-value {
    font-size: 2rem;
    font-weight: bold;
    color: #667eea;
}

.kpi-label {
    color: #666;
    font-size: 0.9rem;
}

.metric-card {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    margin: 0.5rem;
}

.stDataFrame {
    background: white;
    border-radius: 8px;
    overflow: hidden;
}

[data-testid="stDataFrame"] {
    background-color: white !important;
}

[data-testid="stDataFrame"] table {
    background-color: white !important;
    color: black !important;
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

@st.cache_data
def load_sample_data():
    """🚀 Charge un échantillon de données pour démonstration"""
    
    # Créer des données de démonstration réalistes
    np.random.seed(42)
    n_rows = 50000  # Échantillon plus petit pour le cloud
    
    # Listes de données réalistes
    etablissements = [
        "CHU de Lyon", "Hôpital Saint-Antoine", "Clinique des Lilas",
        "CHR de Lille", "Hôpital Européen", "Clinique du Parc",
        "CHU de Bordeaux", "Hôpital Tenon", "Clinique Pasteur",
        "CHU de Toulouse", "Hôpital Bichat", "Clinique Mozart"
    ] * 100
    
    medicaments = [
        "Cabometyx", "Keytruda", "Opdivo", "Tecfidera", "Humira",
        "Enbrel", "Remicade", "Avastin", "Herceptin", "Rituxan",
        "Lucentis", "Eylea", "Xarelto", "Eliquis", "Pradaxa"
    ] * 100
    
    molecules = [
        "cabozantinib", "pembrolizumab", "nivolumab", "dimethyl fumarate",
        "adalimumab", "etanercept", "infliximab", "bevacizumab",
        "trastuzumab", "rituximab", "ranibizumab", "aflibercept"
    ] * 100
    
    villes = [
        "Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes",
        "Strasbourg", "Montpellier", "Bordeaux", "Lille", "Rennes", "Reims"
    ] * 100
    
    categories = [
        "CHU", "CHR", "Clinique Privée", "Hôpital Public", "ESPIC"
    ] * 200
    
    # Générer les données
    data = {
        'etablissement': np.random.choice(etablissements, n_rows),
        'medicament': np.random.choice(medicaments, n_rows),
        'molecule': np.random.choice(molecules, n_rows),
        'ville': np.random.choice(villes, n_rows),
        'categorie': np.random.choice(categories, n_rows),
        'BOITES': np.random.exponential(50, n_rows).astype(int) + 1,
        'REM': np.random.exponential(5000, n_rows),
        'BSE': np.random.exponential(6000, n_rows),
        'atc1': np.random.choice(['A', 'B', 'C', 'D', 'G', 'H', 'J', 'L', 'M', 'N'], n_rows),
        'L_ATC1': np.random.choice([
            'Système digestif et métabolisme', 'Sang et organes hématopoïétiques',
            'Système cardiovasculaire', 'Médicaments dermatologiques',
            'Système génito-urinaire', 'Hormones systémiques',
            'Anti-infectieux généraux', 'Antinéoplasiques', 'Système musculo-squelettique',
            'Système nerveux'
        ], n_rows)
    }
    
    df = pd.DataFrame(data)
    
    # Calculer les colonnes dérivées
    df['cout_par_boite'] = df['REM'] / df['BOITES']
    df['taux_remboursement'] = (df['REM'] / df['BSE']) * 100
    
    # Nettoyer les valeurs infinies
    df = df.replace([np.inf, -np.inf], 0)
    df = df.fillna(0)
    
    return df

def get_filtered_data(df, filters):
    """Applique les filtres aux données"""
    df_filtered = df.copy()
    
    if filters.get('atc1'):
        df_filtered = df_filtered[df_filtered['atc1'].isin(filters['atc1'])]
    
    if filters.get('ville'):
        df_filtered = df_filtered[df_filtered['ville'].isin(filters['ville'])]
    
    if filters.get('categorie'):
        df_filtered = df_filtered[df_filtered['categorie'].isin(filters['categorie'])]
    
    if filters.get('etablissement'):
        df_filtered = df_filtered[df_filtered['etablissement'].isin(filters['etablissement'])]
    
    if filters.get('medicament'):
        df_filtered = df_filtered[df_filtered['medicament'].isin(filters['medicament'])]
    
    if filters.get('min_boites', 0) > 0:
        df_filtered = df_filtered[df_filtered['BOITES'] >= filters['min_boites']]
    
    return df_filtered

def main():
    """Application principale"""
    
    # En-tête
    st.markdown("""
    <div class="main-header">
        <h1>🏥 PHMEV Analytics Pro - Cloud</h1>
        <p>Analyse des données pharmaceutiques PHMEV - Version démo optimisée</p>
        <p><small>⚡ Version allégée pour Streamlit Cloud (50K lignes échantillon)</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données
    with st.spinner("🚀 Chargement des données de démonstration..."):
        df = load_sample_data()
    
    # Sidebar - Filtres
    st.sidebar.header("🎛️ Filtres")
    
    filters = {}
    
    # Filtre ATC1
    atc1_options = sorted(df['atc1'].unique())
    filters['atc1'] = st.sidebar.multiselect(
        "🧬 Classification ATC1", 
        options=atc1_options,
        help="Classification thérapeutique niveau 1"
    )
    
    # Filtre Ville
    ville_options = sorted(df['ville'].unique())
    filters['ville'] = st.sidebar.multiselect(
        "🏙️ Villes", 
        options=ville_options
    )
    
    # Filtre Catégorie
    cat_options = sorted(df['categorie'].unique())
    filters['categorie'] = st.sidebar.multiselect(
        "🏥 Catégories", 
        options=cat_options
    )
    
    # Filtre Établissement
    etab_options = sorted(df['etablissement'].unique())
    filters['etablissement'] = st.sidebar.multiselect(
        "🏢 Établissements", 
        options=etab_options
    )
    
    # Filtre Médicament
    med_options = sorted(df['medicament'].unique())
    filters['medicament'] = st.sidebar.multiselect(
        "💊 Médicaments", 
        options=med_options
    )
    
    # Filtre nombre de boîtes
    filters['min_boites'] = st.sidebar.number_input(
        "📦 Nombre minimum de boîtes", 
        min_value=0, 
        value=0,
        help="Filtrer par nombre minimum de boîtes"
    )
    
    # Appliquer les filtres
    df_filtered = get_filtered_data(df, filters)
    
    # KPIs
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
        total_boites = df_filtered['BOITES'].sum()
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-value">{format_number(total_boites)}</div>
            <div class="kpi-label">📦 Boîtes Totales</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        nb_etabs = df_filtered['etablissement'].nunique()
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-value">{nb_etabs}</div>
            <div class="kpi-label">🏥 Établissements</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        nb_medicaments = df_filtered['medicament'].nunique()
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-value">{nb_medicaments}</div>
            <div class="kpi-label">💊 Médicaments</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Onglets pour les 3 tableaux
    tab1, tab2, tab3 = st.tabs(["🏥 Top Établissements", "💊 Top Produits", "🧬 Top Molécules"])
    
    with tab1:
        st.subheader("🏥 Top Établissements par Remboursement")
        
        if len(df_filtered) > 0:
            df_etabs = df_filtered.groupby('etablissement').agg({
                'REM': 'sum',
                'BOITES': 'sum',
                'BSE': 'sum'
            }).reset_index()
            
            df_etabs['cout_par_boite'] = df_etabs['REM'] / df_etabs['BOITES']
            df_etabs['taux_remboursement'] = (df_etabs['REM'] / df_etabs['BSE']) * 100
            
            df_etabs = df_etabs.sort_values('REM', ascending=False).head(20)
            
            # Formatage pour affichage
            df_etabs_display = df_etabs.copy()
            df_etabs_display['REM'] = df_etabs_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_etabs_display['BSE'] = df_etabs_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_etabs_display['cout_par_boite'] = df_etabs_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_etabs_display['taux_remboursement'] = df_etabs_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            df_etabs_display['BOITES'] = df_etabs_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            df_etabs_display.columns = ['Établissement', 'Montant Remboursé', 'Boîtes', 'Base Remboursable', 'Coût/Boîte', 'Taux Remb.']
            
            st.dataframe(df_etabs_display, use_container_width=True)
            
            # Graphique
            if st.checkbox("📊 Afficher le graphique - Établissements"):
                fig = px.bar(
                    df_etabs.head(10), 
                    x='REM', 
                    y='etablissement',
                    orientation='h',
                    title="Top 10 Établissements par Remboursement"
                )
                fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Aucune donnée disponible avec les filtres sélectionnés")
    
    with tab2:
        st.subheader("💊 Top Produits par Remboursement")
        
        if len(df_filtered) > 0:
            df_produits = df_filtered.groupby('medicament').agg({
                'REM': 'sum',
                'BOITES': 'sum',
                'BSE': 'sum'
            }).reset_index()
            
            df_produits['cout_par_boite'] = df_produits['REM'] / df_produits['BOITES']
            df_produits['taux_remboursement'] = (df_produits['REM'] / df_produits['BSE']) * 100
            
            df_produits = df_produits.sort_values('REM', ascending=False).head(20)
            
            # Formatage pour affichage
            df_produits_display = df_produits.copy()
            df_produits_display['REM'] = df_produits_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_produits_display['BSE'] = df_produits_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_produits_display['cout_par_boite'] = df_produits_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_produits_display['taux_remboursement'] = df_produits_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            df_produits_display['BOITES'] = df_produits_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            df_produits_display.columns = ['Produit', 'Montant Remboursé', 'Boîtes', 'Base Remboursable', 'Coût/Boîte', 'Taux Remb.']
            
            st.dataframe(df_produits_display, use_container_width=True)
            
            # Graphique
            if st.checkbox("📊 Afficher le graphique - Produits"):
                fig = px.bar(
                    df_produits.head(10), 
                    x='REM', 
                    y='medicament',
                    orientation='h',
                    title="Top 10 Produits par Remboursement"
                )
                fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Aucune donnée disponible avec les filtres sélectionnés")
    
    with tab3:
        st.subheader("🧬 Top Molécules par Remboursement")
        
        if len(df_filtered) > 0:
            df_molecules = df_filtered.groupby('molecule').agg({
                'REM': 'sum',
                'BOITES': 'sum',
                'BSE': 'sum'
            }).reset_index()
            
            df_molecules['cout_par_boite'] = df_molecules['REM'] / df_molecules['BOITES']
            df_molecules['taux_remboursement'] = (df_molecules['REM'] / df_molecules['BSE']) * 100
            
            df_molecules = df_molecules.sort_values('REM', ascending=False).head(20)
            
            # Formatage pour affichage
            df_molecules_display = df_molecules.copy()
            df_molecules_display['REM'] = df_molecules_display['REM'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_molecules_display['BSE'] = df_molecules_display['BSE'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_molecules_display['cout_par_boite'] = df_molecules_display['cout_par_boite'].apply(lambda x: f"{x:,.2f}€".replace(',', ' ').replace('.', ',').replace(' ', '.'))
            df_molecules_display['taux_remboursement'] = df_molecules_display['taux_remboursement'].apply(lambda x: f"{x:.1f}%")
            df_molecules_display['BOITES'] = df_molecules_display['BOITES'].apply(lambda x: f"{x:,}".replace(',', ' '))
            
            df_molecules_display.columns = ['Molécule', 'Montant Remboursé', 'Boîtes', 'Base Remboursable', 'Coût/Boîte', 'Taux Remb.']
            
            st.dataframe(df_molecules_display, use_container_width=True)
            
            # Graphique
            if st.checkbox("📊 Afficher le graphique - Molécules"):
                fig = px.bar(
                    df_molecules.head(10), 
                    x='REM', 
                    y='molecule',
                    orientation='h',
                    title="Top 10 Molécules par Remboursement"
                )
                fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Aucune donnée disponible avec les filtres sélectionnés")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🏥 <strong>PHMEV Analytics Pro - Cloud Edition</strong></p>
        <p>Version démo optimisée pour Streamlit Cloud | Données synthétiques pour démonstration</p>
        <p><small>⚡ Pour accéder aux données complètes (3.5M lignes), utilisez la version locale avec DuckDB</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
