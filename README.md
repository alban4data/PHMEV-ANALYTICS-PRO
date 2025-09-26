# 🚀 PHMEV Analytics Pro

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://phmev-analytics-pro.streamlit.app)

Une application Streamlit moderne pour l'analyse des données pharmaceutiques PHMEV avec interface ultra sexy et fonctionnalités avancées.

## ✨ Fonctionnalités

- 🎨 **Interface ultra moderne** avec thème sombre et animations
- 📊 **Analyses avancées** des délivrances pharmaceutiques
- 🔍 **Filtres intelligents** par ATC, CIP, établissement, région
- 💎 **KPIs en temps réel** avec métriques calculées automatiquement
- 📈 **Visualisations interactives** avec Plotly
- 📋 **Tableaux dynamiques** avec export multi-format
- ⚡ **Performance optimisée** pour les gros datasets

## 🚀 Déploiement Streamlit Cloud

Cette application est optimisée pour Streamlit Cloud :

1. **Données d'exemple** : L'app fonctionne avec des données d'exemple quand le fichier principal n'est pas disponible
2. **Auto-détection** : Détecte automatiquement si le fichier PHMEV complet est présent
3. **Interface adaptative** : S'adapte aux contraintes de mémoire du cloud

## 📊 Données

### Mode Production
- Fichier requis : `OPEN_PHMEV_2024.CSV`
- Format : CSV avec séparateur `;` et encodage `latin1`
- Taille : ~1.2GB avec 4+ millions de lignes

### Mode Démonstration
- Utilise `sample_data.py` pour générer 1000 lignes d'exemple
- Toutes les fonctionnalités disponibles
- Parfait pour tester l'interface

## 🛠️ Installation Locale

```bash
# Cloner le repository
git clone https://github.com/alban4data/PHMEV-ANALYTICS-PRO.git
cd PHMEV-ANALYTICS-PRO

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run streamlit_app.py
```

## 📁 Structure

```
PHMEV-ANALYTICS-PRO/
├── streamlit_app.py          # Point d'entrée pour Streamlit Cloud
├── app_phmev_sexy.py         # Application principale
├── sample_data.py            # Générateur de données d'exemple
├── requirements.txt          # Dépendances
├── launch_app.py             # Script de lancement local
├── lancer_app_sexy.bat       # Script Windows
└── README.md                 # Documentation
```

## 🎨 Interface

- **Design moderne** : Gradients, glassmorphism, animations CSS
- **Responsive** : S'adapte à tous les écrans
- **Intuitive** : Navigation simple et filtres intelligents
- **Performante** : Cache intelligent et optimisations mémoire

## 📈 Métriques Disponibles

- 📦 **Boîtes délivrées** par établissement/région
- 💰 **Montants remboursés** (REM)
- 🏦 **Base remboursable** (BSE)
- 💊 **Coût par boîte** calculé automatiquement
- 📊 **Taux de remboursement** REM/BSE
- 🗺️ **Analyses géographiques**
- 🧬 **Classifications ATC**

## ⚙️ Configuration Streamlit Cloud

L'application est prête pour Streamlit Cloud avec :
- Gestion automatique des dépendances
- Fallback sur données d'exemple
- Optimisations mémoire
- Interface adaptative

## 🔧 Développement

### Technologies utilisées
- **Streamlit** : Framework web
- **Pandas** : Manipulation des données
- **Plotly** : Visualisations interactives
- **NumPy** : Calculs numériques

### Contribution
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Distribué sous licence MIT. Voir `LICENSE` pour plus d'informations.

---

<div align="center">

**🚀 PHMEV Analytics Pro** - Analyse pharmaceutique de nouvelle génération

[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-red)](https://streamlit.io/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/downloads/)

</div>