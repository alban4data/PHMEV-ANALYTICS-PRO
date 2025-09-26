# 🚀 PHMEV Analytics Pro

Une application Streamlit moderne pour l'analyse des données pharmaceutiques PHMEV avec interface ultra sexy et fonctionnalités avancées.

## 📊 Fonctionnalités

- ✨ **Interface moderne** avec thème sombre et animations
- 📈 **Analyses avancées** des délivrances pharmaceutiques
- 🔍 **Filtres intelligents** par ATC, CIP, établissement, région
- 💎 **KPIs en temps réel** avec métriques calculées automatiquement
- 📊 **Visualisations interactives** avec Plotly
- 📋 **Tableaux dynamiques** avec export multi-format
- ⚡ **Performance optimisée** pour les gros datasets

## 🛠️ Installation

### Prérequis
- Python 3.8+
- pip
- Fichier de données `OPEN_PHMEV_2024.CSV`

### Installation rapide

```bash
# Cloner le repository
git clone <url-du-repo>
cd PHMEV

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app_phmev_sexy.py
```

### Installation avec script de lancement

```bash
# Windows
python launch_app.py
# ou
.\lancer_app_sexy.bat

# L'application s'ouvrira automatiquement sur http://localhost:8501
```

## 📁 Structure du projet

```
PHMEV/
├── app_phmev_sexy.py          # Application principale (interface moderne)
├── app_phmev.py               # Version standard
├── launch_app.py              # Script de lancement Python
├── lancer_app_sexy.bat        # Script de lancement Windows
├── requirements.txt           # Dépendances Python
├── requirements_prod.txt      # Dépendances production
├── Dockerfile                 # Configuration Docker
├── deploy_*.md               # Guides de déploiement
└── OPEN_PHMEV_2024.CSV       # Données (non incluses dans Git)
```

## 🚀 Déploiement

### Local
```bash
streamlit run app_phmev_sexy.py
```

### Docker
```bash
docker build -t phmev-analytics .
docker run -p 8501:8501 phmev-analytics
```

### Cloud (Railway, DigitalOcean, etc.)
Voir les guides de déploiement dans les fichiers `deploy_*.md`

## 📊 Données

L'application nécessite le fichier `OPEN_PHMEV_2024.CSV` qui doit être placé dans le répertoire racine du projet.

**Format attendu :**
- Séparateur : `;`
- Encodage : `latin1`
- Colonnes principales : ATC, CIP, BOITES, REM, BSE, établissements, etc.

## ⚙️ Configuration

### Paramètres principaux
- **Chargement des données** : Complet par défaut (modifiable dans le code)
- **Cache** : Activé pour les performances
- **Interface** : Thème sombre avec animations

### Personnalisation
- Modifier les couleurs dans les variables CSS du fichier principal
- Ajuster les filtres et métriques selon vos besoins
- Configurer les options d'export

## 🎨 Interface

- **Design moderne** : Gradient backgrounds, glassmorphism, animations
- **Responsive** : S'adapte à tous les écrans
- **Intuitive** : Navigation simple et filtres intelligents
- **Performance** : Chargement optimisé et mise en cache

## 📈 Métriques disponibles

- **Boîtes délivrées** : Nombre total et par établissement
- **Montants remboursés** : REM (Assurance Maladie)
- **Base remboursable** : BSE
- **Coût par boîte** : Calculé automatiquement
- **Taux de remboursement** : Pourcentage REM/BSE
- **Analyses géographiques** : Par région, ville
- **Analyses produits** : Par ATC, CIP, génériques

## 🔧 Développement

### Structure du code
- **app_phmev_sexy.py** : Application principale avec interface moderne
- **Fonctions principales** : `load_data()`, `get_all_filter_options()`, `main()`
- **CSS intégré** : Styles modernes avec variables CSS
- **Cache intelligent** : Optimisation des performances

### Contributions
1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence [MIT](LICENSE) - voir le fichier LICENSE pour plus de détails.

## 🆘 Support

- **Issues** : Utiliser les GitHub/GitLab Issues
- **Documentation** : README et guides de déploiement
- **Contact** : [Votre contact]

## 🚀 Version

**Version actuelle** : 2.0 (Interface Sexy)
- Interface ultra moderne
- Performances optimisées
- Fonctionnalités avancées

---

<div align="center">
<strong>🚀 PHMEV Analytics Pro</strong> - Analyse pharmaceutique de nouvelle génération
</div>
