# 🚂 Déploiement Railway - 5€/mois

## ⚡ Setup en 15 minutes

### Étape 1: Préparation
```bash
# Créer railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run app_phmev_sexy.py --server.port $PORT --server.address 0.0.0.0"
  }
}
```

### Étape 2: Variables d'environnement
```bash
# Sur Railway Dashboard
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=$PORT
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Étape 3: Déploiement
1. **railway.app** → New Project
2. **Deploy from GitHub** → Sélectionner repo
3. **Auto-deploy** activé
4. **Custom domain** possible

## 💰 Tarification
- **Gratuit:** 500h/mois (16h/jour)
- **Pro:** 5€/mois = illimité
- **Scaling:** Automatique

## 🎯 Avantages Railway
- **Données complètes** (3.5M lignes)
- **100+ utilisateurs** simultanés
- **Uptime 99.9%**
- **Monitoring** inclus
- **SSL** automatique
- **Variables d'env** sécurisées
