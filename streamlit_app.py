import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuration de la page
st.set_page_config(
    page_title="📊 PHMEV Analytics Pro",
    page_icon="💊",
    layout="wide"
)

# Fonction pour charger les données depuis Google Drive avec fallback
@st.cache_data(show_spinner=False)
def load_phmev_data():
    """Charge les données PHMEV depuis Google Drive ou utilise les données d'exemple"""
    
    # URL Google Drive de votre fichier Parquet
    drive_url = "https://drive.google.com/uc?export=download&id=16gIMMzbqIHG65DNlV9RYps1NzlHsulfM"
    
    try:
        # Tentative de chargement depuis Google Drive
        st.info("☁️ Chargement des données complètes depuis Google Drive...")
        
        # Charger le fichier Parquet directement depuis Google Drive
        df = pd.read_parquet(drive_url, engine='pyarrow')
        
        # Créer les colonnes enrichies si elles n'existent pas
        if 'etablissement' not in df.columns:
            st.info("🔧 Création des colonnes enrichies...")
            
            # Colonnes dérivées
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
        
        st.success(f"🚀 Données complètes chargées avec succès ! ({len(df):,} lignes)")
        return df
        
    except Exception as e:
        st.warning(f"⚠️ Impossible de charger depuis Google Drive: {str(e)}")
        st.info("🔄 Utilisation des données d'exemple...")
        
        # Fallback vers les données d'exemple
        return create_demo_data()

# Import de l'application principale
try:
    # Essayer d'importer l'app principale si elle existe
    from app_phmev_sexy import main as main_app
    USE_FULL_APP = True
except ImportError:
    USE_FULL_APP = False

# CSS pour le thème sombre
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117 !important;
        color: white !important;
    }
    .main .block-container {
        background-color: #0e1117 !important;
        color: white !important;
    }
    [data-testid="stAppViewContainer"] {
        background: #0e1117 !important;
    }
    [data-testid="stMainBlockContainer"] {
        background: #0e1117 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour créer des données d'exemple
@st.cache_data
def create_demo_data():
    """Créer des données d'exemple pour la démonstration"""
    np.random.seed(42)
    
    # Données simplifiées
    etablissements = ['Pharmacie Central', 'Pharmacie du Marché', 'Pharmacie Saint-Jean', 'Pharmacie Moderne', 'Pharmacie de la Paix']
    medicaments = ['DOLIPRANE 1000MG', 'EFFERALGAN 500MG', 'DAFALGAN 1G', 'PARACETAMOL 500MG', 'IBUPROFENE 400MG']
    villes = ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice']
    regions = ['Île-de-France', 'Auvergne-Rhône-Alpes', 'Provence-Alpes-Côte d\'Azur', 'Occitanie', 'Nouvelle-Aquitaine']
    
    n_rows = 1000
    
    data = []
    for i in range(n_rows):
        boites = np.random.randint(1, 100)
        rem = round(np.random.uniform(10, 500), 2)
        bse = round(rem * np.random.uniform(0.1, 0.8), 2)
        
        data.append({
            'etablissement': np.random.choice(etablissements),
            'medicament': np.random.choice(medicaments),
            'ville': np.random.choice(villes),
            'region': np.random.choice(regions),
            'categorie': np.random.choice(['Prescription', 'Automédication']),
            'BOITES': boites,
            'REM': rem,
            'BSE': bse,
            'cout_par_boite': round(rem / boites, 2),
            'taux_remboursement': round((bse / rem) * 100, 2) if rem > 0 else 0
        })
    
    return pd.DataFrame(data)

# Interface principale
def main():
    # Essayer d'utiliser l'app complète d'abord
    if USE_FULL_APP:
        try:
            # Patcher la fonction de chargement de données dans l'app principale
            import app_phmev_sexy
            
            # Remplacer la fonction de chargement par notre version optimisée
            app_phmev_sexy.load_data_background = load_phmev_data
            app_phmev_sexy.load_data = load_phmev_data
            
            # Lancer l'app principale
            st.info("🚀 Lancement de la version complète PHMEV Analytics Pro")
            main_app()
            return
            
        except Exception as e:
            st.error(f"❌ Erreur avec l'app complète: {str(e)}")
            st.info("🔄 Basculement vers la version simplifiée...")
    
    # Version simplifiée en fallback
    # Header avec style
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 3rem;">📊 PHMEV Analytics Pro</h1>
        <p style="color: white; margin: 0.5rem 0 0 0; font-size: 1.2rem;">Analyse pharmaceutique avancée - Version Simplifiée</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données
    try:
        with st.spinner("🔄 Chargement des données de démonstration..."):
            df = create_demo_data()
        
        st.success(f"✅ Données chargées avec succès ! ({len(df):,} lignes de démonstration)")
        
        # Sidebar pour les filtres
        st.sidebar.header("🎛️ Filtres")
        
        # Filtres
        selected_etabs = st.sidebar.multiselect(
            "📍 Établissements",
            options=sorted(df['etablissement'].unique()),
            default=sorted(df['etablissement'].unique())[:3]
        )
        
        selected_meds = st.sidebar.multiselect(
            "💊 Médicaments", 
            options=sorted(df['medicament'].unique()),
            default=sorted(df['medicament'].unique())[:3]
        )
        
        selected_regions = st.sidebar.multiselect(
            "🗺️ Régions",
            options=sorted(df['region'].unique()),
            default=sorted(df['region'].unique())[:3]
        )
        
        # Filtrer les données
        df_filtered = df.copy()
        if selected_etabs:
            df_filtered = df_filtered[df_filtered['etablissement'].isin(selected_etabs)]
        if selected_meds:
            df_filtered = df_filtered[df_filtered['medicament'].isin(selected_meds)]
        if selected_regions:
            df_filtered = df_filtered[df_filtered['region'].isin(selected_regions)]
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📦 Total Boîtes", f"{df_filtered['BOITES'].sum():,}")
        
        with col2:
            st.metric("💰 Remboursé Total", f"{df_filtered['REM'].sum():,.2f}€")
        
        with col3:
            st.metric("🏥 Base Sécu. Sociale", f"{df_filtered['BSE'].sum():,.2f}€")
        
        with col4:
            st.metric("📊 Lignes Filtrées", f"{len(df_filtered):,}")
        
        # Graphiques
        if len(df_filtered) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Répartition par Établissement")
                etab_data = df_filtered.groupby('etablissement')['BOITES'].sum().reset_index()
                fig1 = px.bar(
                    etab_data,
                    x='etablissement',
                    y='BOITES',
                    title="Nombre de boîtes par établissement",
                    color='BOITES',
                    color_continuous_scale='viridis'
                )
                fig1.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                st.subheader("💊 Répartition par Médicament")
                med_data = df_filtered.groupby('medicament')['REM'].sum().reset_index()
                fig2 = px.pie(
                    med_data,
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
            
            # Graphique régional
            st.subheader("🗺️ Analyse par Région")
            region_data = df_filtered.groupby('region').agg({
                'BOITES': 'sum',
                'REM': 'sum',
                'BSE': 'sum'
            }).reset_index()
            
            fig3 = px.bar(
                region_data,
                x='region',
                y=['BOITES', 'REM', 'BSE'],
                title="Comparaison par région",
                barmode='group'
            )
            fig3.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig3, use_container_width=True)
            
            # Tableau des données
            st.subheader("📋 Données détaillées")
            st.dataframe(
                df_filtered.head(100),
                use_container_width=True,
                height=400
            )
            
        else:
            st.warning("⚠️ Aucune donnée ne correspond aux filtres sélectionnés.")
        
        # Informations sur la démo
        st.info("💡 Cette version de démonstration utilise 1000 lignes de données synthétiques pour illustrer toutes les fonctionnalités de l'application.")
        
    except Exception as e:
        st.error(f"❌ Erreur: {str(e)}")
        st.info("🔧 Si vous voyez cette erreur, veuillez contacter le support.")

if __name__ == "__main__":
    main()