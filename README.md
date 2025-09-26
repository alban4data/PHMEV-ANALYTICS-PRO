# 🏥 PHMEV Analytics Pro

Application d'analyse pharmaceutique avec BigQuery - Version Dynamique

## 🚀 Fonctionnalités

- **Filtres hiérarchiques dynamiques** : Mise à jour automatique et en temps réel
- **Noms commerciaux de médicaments** : Recherche par nom commercial (ex: Cabometyx)
- **Cache intelligent** : Chargement ultra-rapide (2-3 secondes)
- **Performance optimisée** : 2,5M lignes analysées instantanément
- **Interface moderne** : Design responsive avec Plotly

## 📊 Données

- **9,080 médicaments** distincts
- **1,116 établissements**
- **947 villes**
- **Classification ATC complète** (5 niveaux)

## 🔧 Installation locale

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## ⚡ Cache

Pour générer le cache des filtres (optionnel) :
```bash
python generate_filter_cache.py
```

## 🌐 Déploiement

Application déployée sur Streamlit Cloud avec authentification BigQuery sécurisée.

## 📈 Performance

- **Chargement initial** : 2-3 secondes (avec cache)
- **Filtres dynamiques** : Instantané
- **Recherche médicaments** : Temps réel
- **Génération graphiques** : < 1 seconde

## 🔍 Recherche intelligente

- Tapez "cabometyx" → trouve "CABOMETYX 20 MG CPR 30"
- Alias supportés : "cabome", "keytr", "opdi", etc.
- Recherche insensible à la casse

---
*PHMEV Analytics Pro - Version Dynamique avec cache intelligent*