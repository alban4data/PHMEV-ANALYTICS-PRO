# Dockerfile optimisé pour production PHMEV Analytics Pro
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="IQVIA Data&IA Team"
LABEL version="1.0"
LABEL description="PHMEV Analytics Pro - Production Ready"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_MAX_UPLOAD_SIZE=1024

# Créer utilisateur non-root pour sécurité
RUN groupadd -r streamlit && useradd -r -g streamlit streamlit

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copier et installer les requirements
COPY requirements_prod.txt .
RUN pip install --no-cache-dir -r requirements_prod.txt

# Copier le code de l'application
COPY app_phmev_sexy.py .
COPY OPEN_PHMEV_2024.CSV .

# Créer répertoires pour logs et cache
RUN mkdir -p /app/logs /app/cache && \
    chown -R streamlit:streamlit /app

# Changer vers utilisateur non-root
USER streamlit

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Exposer le port
EXPOSE 8501

# Commande de démarrage
CMD ["streamlit", "run", "app_phmev_sexy.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.maxUploadSize=1024", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=true"]
