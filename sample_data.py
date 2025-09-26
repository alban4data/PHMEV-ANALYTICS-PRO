"""
Module pour générer des données d'exemple pour Streamlit Cloud
"""
import pandas as pd
import numpy as np
from datetime import datetime

def create_sample_data():
    """Crée un échantillon de données PHMEV pour la démonstration"""
    
    np.random.seed(42)  # Pour la reproductibilité
    
    # Générer 1000 lignes d'exemple
    n_rows = 1000
    
    # Données ATC
    atc1_codes = ['A', 'B', 'C', 'J', 'N']
    atc1_labels = ['Système digestif', 'Sang et organes', 'Système cardiovasculaire', 'Anti-infectieux', 'Système nerveux']
    
    # Établissements d'exemple
    etablissements = [
        'PHARMACIE CENTRALE', 'PHARMACIE DU CENTRE', 'PHARMACIE MODERNE',
        'PHARMACIE SAINT-MICHEL', 'PHARMACIE DE LA GARE', 'PHARMACIE DU MARCHE'
    ]
    
    villes = ['PARIS', 'LYON', 'MARSEILLE', 'TOULOUSE', 'NICE', 'NANTES']
    categories = ['PHARMACIE', 'HOPITAL', 'CLINIQUE']
    
    # Médicaments d'exemple
    medicaments = [
        'DOLIPRANE 1000MG CPR 8',
        'SPASFON 80MG CPR 30',
        'EFFERALGAN 1G CPR EFF 8',
        'SMECTA 3G PDR SAC 30',
        'GAVISCON MENTHE CPR 24'
    ]
    
    # Générer les données
    data = []
    for i in range(n_rows):
        atc1_idx = np.random.choice(len(atc1_codes))
        boites = np.random.randint(1, 100)
        prix_unitaire = np.random.uniform(5.0, 50.0)
        rem_base = boites * prix_unitaire
        bse_base = rem_base * np.random.uniform(1.0, 1.3)
        
        etb_name = np.random.choice(etablissements)
        medicament = np.random.choice(medicaments)
        
        row = {
            'atc1': atc1_codes[atc1_idx],
            'l_atc1': atc1_labels[atc1_idx],
            'atc2': f"{atc1_codes[atc1_idx]}0{np.random.randint(1,9)}",
            'L_ATC2': f"Sous-groupe {atc1_labels[atc1_idx]}",
            'atc3': f"{atc1_codes[atc1_idx]}0{np.random.randint(1,9)}A",
            'L_ATC3': f"Groupe thérapeutique",
            'atc4': f"{atc1_codes[atc1_idx]}0{np.random.randint(1,9)}A{np.random.randint(1,9)}",
            'L_ATC4': f"Sous-groupe thérapeutique",
            'ATC5': f"{atc1_codes[atc1_idx]}0{np.random.randint(1,9)}A{np.random.randint(1,9)}{np.random.randint(1,9)}",
            'L_ATC5': medicament,
            'CIP13': f"34009{np.random.randint(100000000, 999999999)}",
            'l_cip13': medicament,
            'BOITES': boites,
            'REM': f"{rem_base:.2f}".replace('.', ','),  # Format français
            'BSE': f"{bse_base:.2f}".replace('.', ','),  # Format français
            'nom_etb': etb_name,
            'raison_sociale_etb': etb_name,
            'nom_ville': np.random.choice(villes),
            'categorie_jur': np.random.choice(categories),
            'region_etb': np.random.randint(1, 13),
            'TOP_GEN': np.random.choice(['OUI', 'NON']),
            'GEN_NUM': np.random.randint(1, 5),
            'age': np.random.randint(18, 90),
            # Colonnes dérivées nécessaires pour l'application
            'etablissement': etb_name,
            'medicament': medicament,
            'categorie': np.random.choice(categories),
            'ville': np.random.choice(villes),
            'region': np.random.randint(1, 13),
            'code_cip': f"34009{np.random.randint(100000000, 999999999)}",
            'libelle_cip': medicament
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Conversion des colonnes financières françaises en numériques
    def convert_french_decimal(series):
        """Convertit les décimaux français (virgule) en float"""
        cleaned = series.astype(str).str.strip()
        cleaned = cleaned.replace(['', 'nan', 'NaN', 'NULL', 'null'], pd.NA)
        
        def clean_french_number(x):
            if pd.isna(x) or x == 'nan':
                return pd.NA
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
    
    # Appliquer les conversions
    df['BOITES'] = pd.to_numeric(df['BOITES'], errors='coerce')
    df['REM'] = convert_french_decimal(df['REM'])
    df['BSE'] = convert_french_decimal(df['BSE'])
    
    # Calculs des métriques dérivées
    df['cout_par_boite'] = np.where(df['BOITES'] > 0, df['REM'] / df['BOITES'], 0)
    df['taux_remboursement'] = np.where(df['BSE'] > 0, (df['REM'] / df['BSE'] * 100).round(2), 0)
    
    return df

def save_sample_data():
    """Sauvegarde les données d'exemple"""
    df = create_sample_data()
    df.to_csv('sample_PHMEV_data.csv', sep=';', index=False, encoding='latin1')
    return df

if __name__ == "__main__":
    df = save_sample_data()
    print(f"Données d'exemple créées: {len(df)} lignes")
    print(f"Colonnes: {list(df.columns)}")
