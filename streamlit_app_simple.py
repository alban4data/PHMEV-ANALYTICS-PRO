import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="📊 PHMEV Analytics Pro",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS simplifié pour le thème sombre
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    .main .block-container {
        background-color: #0e1117;
        color: white;
    }
    [data-testid="stAppViewContainer"] {
        background: #0e1117 !important;
    }
    [data-testid="stMainBlockContainer"] {
        background: #0e1117 !important;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour créer des données d'exemple simples
@st.cache_data
def create_simple_sample_data():
    """Créer des données d'exemple ultra-simples"""
    np.random.seed(42)
    
    etablissements = ['Pharmacie Central', 'Pharmacie du Marché', 'Pharmacie Saint-Jean', 'Pharmacie Moderne']
    medicaments = ['DOLIPRANE 1000MG', 'EFFERALGAN 500MG', 'DAFALGAN 1G', 'PARACETAMOL 500MG']
    villes = ['Paris', 'Lyon', 'Marseille', 'Toulouse']
    
    n_rows = 500  # Données très réduites
    
    data = {
        'etablissement': np.random.choice(etablissements, n_rows),
        'medicament': np.random.choice(medicaments, n_rows),
        'ville': np.random.choice(villes, n_rows),
        'BOITES': np.random.randint(1, 100, n_rows),
        'REM': np.random.uniform(10, 500, n_rows).round(2),
        'BSE': np.random.uniform(5, 400, n_rows).round(2),
        'region': np.random.randint(1, 13, n_rows)
    }
    
    df = pd.DataFrame(data)
    df['cout_par_boite'] = (df['REM'] / df['BOITES']).round(2)
    df['taux_remboursement'] = ((df['BSE'] / df['REM']) * 100).round(2)
    
    return df

# Interface principale
def main():
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0;">📊 PHMEV Analytics Pro</h1>
        <p style="color: white; margin: 0.5rem 0 0 0;">Analyse pharmaceutique avancée</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Chargement des données
        with st.spinner("🔄 Chargement des données d'exemple..."):
            df = create_simple_sample_data()
        
        st.success(f"✅ Données chargées avec succès ! ({len(df)} lignes)")
        
        # Sidebar pour les filtres
        st.sidebar.header("🎛️ Filtres")
        
        # Filtres
        selected_etabs = st.sidebar.multiselect(
            "Établissements",
            options=df['etablissement'].unique(),
            default=df['etablissement'].unique()[:2]
        )
        
        selected_meds = st.sidebar.multiselect(
            "Médicaments", 
            options=df['medicament'].unique(),
            default=df['medicament'].unique()[:2]
        )
        
        # Filtrer les données
        if selected_etabs and selected_meds:
            df_filtered = df[
                (df['etablissement'].isin(selected_etabs)) &
                (df['medicament'].isin(selected_meds))
            ]
        else:
            df_filtered = df
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📦 Total Boîtes", f"{df_filtered['BOITES'].sum():,}")
        
        with col2:
            st.metric("💰 Remboursé", f"{df_filtered['REM'].sum():.2f}€")
        
        with col3:
            st.metric("🏥 Base Sécurité Sociale", f"{df_filtered['BSE'].sum():.2f}€")
        
        with col4:
            st.metric("📊 Lignes", f"{len(df_filtered):,}")
        
        # Graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Répartition par Établissement")
            fig1 = px.bar(
                df_filtered.groupby('etablissement')['BOITES'].sum().reset_index(),
                x='etablissement',
                y='BOITES',
                title="Nombre de boîtes par établissement"
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.subheader("💊 Répartition par Médicament")
            fig2 = px.pie(
                df_filtered.groupby('medicament')['REM'].sum().reset_index(),
                values='REM',
                names='medicament',
                title="Remboursements par médicament"
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Tableau des données
        st.subheader("📋 Données détaillées")
        st.dataframe(df_filtered.head(50), use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Erreur: {str(e)}")
        st.info("🔧 Application en mode démo avec données simplifiées")

if __name__ == "__main__":
    main()
