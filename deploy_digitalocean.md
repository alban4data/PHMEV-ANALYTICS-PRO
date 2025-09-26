# 🌊 Déploiement DigitalOcean - 6€/mois

## ⚡ Setup Droplet (1-2h)

### Étape 1: Créer Droplet
```bash
# Specs recommandées
- OS: Ubuntu 22.04
- Plan: Basic (6€/mois)
- CPU: 1 vCPU
- RAM: 1GB
- SSD: 25GB
- Bandwidth: 1000GB
```

### Étape 2: Configuration serveur
```bash
# Connexion SSH
ssh root@votre_ip

# Installation Python + dépendances
apt update && apt upgrade -y
apt install python3 python3-pip nginx -y
pip3 install -r requirements.txt

# Configuration Nginx (reverse proxy)
nano /etc/nginx/sites-available/phmev
```

### Étape 3: Configuration Nginx
```nginx
server {
    listen 80;
    server_name votre_domaine.com;
    
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Étape 4: Service systemd
```bash
# Créer service auto-start
nano /etc/systemd/system/phmev.service

[Unit]
Description=PHMEV Analytics
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/phmev
ExecStart=/usr/bin/python3 -m streamlit run app_phmev_sexy.py --server.port 8501
Restart=always

[Install]
WantedBy=multi-user.target

# Activer service
systemctl enable phmev
systemctl start phmev
```

## 🎯 Avantages DigitalOcean
- **Contrôle total** du serveur
- **Données complètes** (3.5M lignes)
- **SSL gratuit** avec Let's Encrypt
- **Monitoring** inclus
- **Backup** automatique (+1€/mois)
- **Scalable** (upgrade facile)
