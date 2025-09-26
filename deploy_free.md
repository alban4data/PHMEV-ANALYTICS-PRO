# 🚀 Déploiement GRATUIT - Streamlit Community Cloud

## ⚡ Setup en 30 minutes

### Étape 1: Préparation (5 min)
```bash
# Créer un échantillon anonymisé plus petit
head -100000 OPEN_PHMEV_2024.CSV > OPEN_PHMEV_SAMPLE.CSV
```

### Étape 2: GitHub (10 min)
```bash
# Initialiser Git
git init
git add app_phmev_sexy.py requirements.txt README.md
git add OPEN_PHMEV_SAMPLE.CSV  # Version échantillon seulement
git commit -m "PHMEV Analytics - Version démo"

# Push sur GitHub
git remote add origin https://github.com/VOTRE_USERNAME/phmev-analytics
git push -u origin main
```

### Étape 3: Déploiement (15 min)
1. Aller sur **share.streamlit.io**
2. **"New app"** → Connect GitHub
3. Sélectionner le repo **phmev-analytics**
4. Main file: **app_phmev_sexy.py**
5. **Deploy!**

## 🔧 Optimisations Gratuites

### Réduire la taille des données
```python
# Dans app_phmev_sexy.py - Version échantillon
@st.cache_data(show_spinner=False, max_entries=1)
def load_data(nrows=100000):  # Limiter à 100k lignes
    csv_path = 'OPEN_PHMEV_SAMPLE.CSV'  # Fichier échantillon
    # ... reste du code
```

### Ajout disclaimer
```python
st.warning("⚠️ **Version Démo** - Données échantillonnées à des fins de démonstration")
```

## 📊 Limitations Acceptables
- **Données:** 100k lignes max (vs 3.5M)
- **Utilisateurs:** 50 simultanés
- **Uptime:** 99% (redémarrage auto)
- **Storage:** 1GB max

## 🎯 Résultat
- **URL:** https://votre-app.streamlit.app
- **Coût:** 0€
- **Maintenance:** 0
- **SSL:** Inclus
