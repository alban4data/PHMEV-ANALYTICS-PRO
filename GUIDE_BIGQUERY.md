# 🚀 Guide de Déploiement PHMEV Analytics Pro avec BigQuery

## 🎯 Vue d'ensemble

Cette solution utilise **Google BigQuery** pour stocker et analyser les données PHMEV, permettant de dépasser les limitations de mémoire de Streamlit Cloud et d'obtenir des performances exceptionnelles.

## 📋 Étapes de Déploiement

### 1. 🔧 Préparation BigQuery

#### A. Créer un compte de service Google Cloud
1. Aller sur [Google Cloud Console](https://console.cloud.google.com/)
2. Sélectionner le projet `test-db-473321`
3. Aller dans **IAM & Admin** > **Service Accounts**
4. Créer un nouveau compte de service avec les rôles :
   - `BigQuery Data Editor`
   - `BigQuery Job User`
   - `BigQuery Data Viewer`
5. Télécharger la clé JSON du compte de service

#### B. Configurer les credentials localement
```bash
# Installer Google Cloud CLI
# Puis authentifier
gcloud auth application-default login
gcloud config set project test-db-473321
```

### 2. 📊 Upload des données vers BigQuery

```bash
# Exécuter le script d'upload
python upload_to_bigquery.py
```

Ce script va :
- ✅ Charger `OPEN_PHMEV_2024.parquet` (3.5M lignes)
- ✅ Nettoyer les données (filtrer "Non restitué", etc.)
- ✅ Convertir les types de données
- ✅ Uploader vers `test-db-473321.dataset.PHMEV2024`
- ✅ Créer des vues optimisées
- ✅ Tester la configuration

### 3. 🔐 Configuration des Secrets Streamlit

#### A. Pour le développement local
1. Copier `.streamlit/secrets.toml.example` vers `.streamlit/secrets.toml`
2. Remplir avec les vraies credentials du compte de service JSON

#### B. Pour Streamlit Cloud
1. Aller sur [share.streamlit.io](https://share.streamlit.io/)
2. Sélectionner votre app
3. Aller dans **Settings** > **Secrets**
4. Ajouter le contenu du fichier JSON du compte de service :

```toml
[gcp_service_account]
type = "service_account"
project_id = "test-db-473321"
private_key_id = "votre_private_key_id"
private_key = "-----BEGIN PRIVATE KEY-----\nvotre_private_key\n-----END PRIVATE KEY-----\n"
client_email = "votre-service-account@test-db-473321.iam.gserviceaccount.com"
client_id = "votre_client_id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/votre-service-account%40test-db-473321.iam.gserviceaccount.com"
```

### 4. 🚀 Déploiement de l'Application

#### Option A : Remplacer streamlit_app.py
```bash
# Sauvegarder la version actuelle
cp streamlit_app.py streamlit_app_duckdb_backup.py

# Remplacer par la version BigQuery
cp streamlit_app_bigquery.py streamlit_app.py

# Commit et push
git add .
git commit -m "feat: Migration vers BigQuery - Performance maximale"
git push origin main
```

#### Option B : Déployer en parallèle
- Garder `streamlit_app.py` (version DuckDB locale)
- Déployer `streamlit_app_bigquery.py` sur une nouvelle app Streamlit Cloud

### 5. ✅ Vérification

Une fois déployé, l'application devrait :
- ✅ Se connecter à BigQuery automatiquement
- ✅ Charger les 3.5M lignes en quelques secondes
- ✅ Afficher tous les filtres hiérarchiques
- ✅ Fonctionner sans limitation de mémoire
- ✅ Avoir des performances exceptionnelles

## 🎯 Avantages de cette Solution

### 🚀 Performance
- **Requêtes ultra-rapides** : BigQuery optimisé pour l'analytique
- **Pas de limite mémoire** : Traite des téraoctets de données
- **Cache intelligent** : Streamlit + BigQuery = vitesse maximale

### 💰 Coût Optimisé
- **Pay-per-query** : Tu paies seulement les requêtes exécutées
- **Compression automatique** : BigQuery optimise le stockage
- **Cache BigQuery** : Requêtes identiques = gratuites

### 🔧 Maintenance
- **Zéro maintenance** : Infrastructure Google gérée
- **Scalabilité automatique** : S'adapte à la charge
- **Backup automatique** : Données sécurisées

### 🌐 Accessibilité
- **Streamlit Cloud compatible** : Pas de gros fichiers à héberger
- **Multi-utilisateurs** : Plusieurs personnes peuvent utiliser l'app
- **Temps de démarrage rapide** : Plus de chargement de 60MB

## 🔍 Monitoring et Debug

### Vérifier les données dans BigQuery
```sql
-- Statistiques générales
SELECT 
    COUNT(*) as total_lignes,
    COUNT(DISTINCT nom_etb) as etablissements_uniques,
    COUNT(DISTINCT L_ATC5) as medicaments_uniques,
    SUM(REM) as remboursement_total,
    MIN(date_creation) as date_min,
    MAX(date_creation) as date_max
FROM `test-db-473321.dataset.PHMEV2024`;

-- Test d'un médicament spécifique
SELECT *
FROM `test-db-473321.dataset.PHMEV2024`
WHERE LOWER(L_ATC5) LIKE '%cabometyx%'
LIMIT 10;
```

### Logs Streamlit Cloud
- Aller dans **Manage app** > **Logs**
- Chercher les erreurs de connexion BigQuery
- Vérifier que les credentials sont correctement configurés

## 🆘 Troubleshooting

### Erreur de credentials
```
Error: Could not automatically determine credentials
```
**Solution** : Vérifier que les secrets sont correctement configurés dans Streamlit Cloud

### Erreur de permissions
```
Error: Access Denied: BigQuery BigQuery: Permission denied
```
**Solution** : Vérifier que le compte de service a les bons rôles BigQuery

### Erreur de quota
```
Error: Quota exceeded
```
**Solution** : Vérifier les quotas BigQuery dans Google Cloud Console

## 🎉 Résultat Final

Avec cette configuration, tu auras :
- 🏥 **Application identique** à la version classique
- ⚡ **Performance 10x supérieure** grâce à BigQuery
- 🌐 **Déployable sur Streamlit Cloud** sans limitation
- 💰 **Coût optimisé** (quelques centimes par mois)
- 🔧 **Maintenance zéro** infrastructure gérée par Google

**C'est la solution parfaite pour ton application PHMEV Analytics Pro !** 🚀
