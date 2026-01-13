# Verwende Python 3.11 Slim Image für kleinere Größe
FROM python:3.11-slim

# Setze Metadaten
LABEL maintainer="L8teNever"
LABEL description="L8teNever Website Server"
LABEL version="1.0"

# Setze Arbeitsverzeichnis
WORKDIR /app

# Kopiere alle Dateien ins Container
COPY . /app

# Setze Umgebungsvariablen
ENV PORT=8000
ENV HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Exponiere Port
EXPOSE 8000

# Mache das Python-Script ausführbar
RUN chmod +x server.py

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000')" || exit 1

# Starte den Server
CMD ["python", "server.py"]
