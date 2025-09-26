# 📊 Application PHMEV - Analyse des Délivrances Pharmaceutiques

## 🎯 Description

Application Streamlit interactive pour analyser les données de délivrances pharmaceutiques PHMEV 2024. 
Permet de filtrer et analyser les délivrances par médicament, catégorie d'établissement, et établissement.

## ✨ Fonctionnalités

### 🔍 Filtres disponibles
- **Médicaments** : Filtrage par classification ATC5
- **Catégories d'établissement** : Filtrage par type juridique d'établissement  
- **Établissements** : Filtrage par nom d'établissement (avec recherche)
- **Top N** : Sélection du nombre d'établissements à afficher (5-100)

### 📈 Métriques affichées
- **Nombre de boîtes délivrées** avec pourcentage du total
- **Montant remboursé** par l'Assurance Maladie
- **Montant remboursable** (base de remboursement)
- **Nombre d'établissements** uniques

### 📊 Visualisations
- Tableau détaillé des Top N établissements
- Graphique en barres des établissements par boîtes délivrées
- Graphiques en secteurs (répartition par catégorie, remboursé vs remboursable)
- Analyse détaillée des médicaments sélectionnés

### 💾 Export
- Export CSV du Top N établissements
- Export CSV des données filtrées (si < 100k lignes)
- Encodage UTF-8 avec BOM pour Excel

## 🚀 Installation et Lancement

### Méthode 1 : Lancement automatique
```bash
# Double-cliquez sur le fichier
lancer_app.bat
```

### Méthode 2 : Lancement manuel
```bash
# Installation des dépendances
pip install -r requirements.txt

# Lancement de l'application
streamlit run app_phmev.py
```

## 📁 Structure des fichiers

```
PHMEV/
├── OPEN_PHMEV_2024.CSV          # Données source (1.2GB)
├── app_phmev.py                 # Application Streamlit principale
├── requirements.txt             # Dépendances Python
├── lancer_app.bat              # Script de lancement Windows
└── README.md                   # Documentation
```

## 📊 Structure des données PHMEV

### Colonnes principales utilisées
- **ATC5/L_ATC5** : Classification ATC niveau 5 (médicament spécifique)
- **CIP13/l_cip13** : Code CIP 13 du médicament
- **nom_etb/raison_sociale_etb** : Nom de l'établissement
- **categorie_jur** : Catégorie juridique de l'établissement
- **BOITES** : Nombre de boîtes délivrées
- **REM** : Montant remboursé par l'Assurance Maladie (€)
- **BSE** : Montant remboursable - base de remboursement (€)

### Données techniques
- **Encodage** : Latin1 (ISO-8859-1)
- **Séparateur** : Point-virgule (;)
- **Taille** : ~1.2GB, millions de lignes
- **Performance** : Échantillon d'1M de lignes pour optimisation

## ⚡ Optimisations

### Performance
- Cache Streamlit pour le chargement des données
- Limitation à 1M de lignes pour la réactivité
- Formatage intelligent des nombres (K, M)
- Limitation de l'affichage des établissements (recherche)

### Mémoire
- Nettoyage automatique des données (conversion numérique)
- Gestion des valeurs manquantes
- Agrégation efficace par établissement

## 🔧 Configuration

### Paramètres modifiables dans le code
```python
# Nombre maximum de lignes à charger
nrows=1000000

# Limite pour l'affichage des établissements
if len(etablissements_uniques) > 1000:

# Limite pour l'export des données filtrées  
if len(df_filtered) <= 100000:
```

## 📝 Utilisation

1. **Lancement** : Exécutez `lancer_app.bat` ou la commande streamlit
2. **Filtrage** : Utilisez les filtres dans la barre latérale
3. **Analyse** : Consultez les métriques et visualisations
4. **Export** : Téléchargez les résultats en CSV

### Cas d'usage typiques

#### Analyse par médicament
1. Sélectionnez un ou plusieurs médicaments (ATC5)
2. Consultez les Top N établissements qui les délivrent
3. Analysez les montants remboursés

#### Analyse par catégorie d'établissement
1. Filtrez par catégorie juridique (hôpital, pharmacie, etc.)
2. Identifiez les plus gros délivreurs
3. Comparez les performances

#### Recherche d'établissement spécifique
1. Utilisez la recherche d'établissement
2. Sélectionnez l'établissement souhaité
3. Analysez ses délivrances par médicament

## ⚠️ Limitations

- **Données** : Échantillon d'1M de lignes (sur le fichier complet)
- **Export** : Limité à 100k lignes pour les données filtrées
- **Performance** : Temps de chargement initial (~10-30 secondes)
- **Mémoire** : Nécessite ~2-4GB de RAM disponible

## 🆘 Troubleshooting

### Erreurs courantes

#### "Module not found"
```bash
pip install -r requirements.txt
```

#### "Encoding error" 
- Le fichier CSV doit être en encodage Latin1
- Vérifiez que le fichier OPEN_PHMEV_2024.CSV est présent

#### "Memory error"
- Réduisez le paramètre `nrows` dans `load_data()`
- Fermez les autres applications pour libérer la mémoire

#### Application lente
- Vérifiez que le cache Streamlit fonctionne
- Réduisez le nombre de filtres actifs
- Diminuez le Top N affiché

### Support
- **Développeur** : Alban Duruisseau
- **Équipe** : Data & IA IQVIA
- **Version** : 1.0 - Septembre 2024

---

*Application développée avec Streamlit et optimisée pour l'analyse des données pharmaceutiques IQVIA*
