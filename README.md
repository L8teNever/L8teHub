# L8teNever Website

Eine moderne, responsive Website mit Material You Design (Android 16 inspiriert).

## 🚀 Features

- **Material You Design**: Moderne UI mit dynamischen Farbschemata
- **Dark Mode**: Automatische Erkennung und manueller Toggle
- **Mehrsprachig**: Deutsch, Englisch, Japanisch
- **Responsive**: Optimiert für Desktop, Tablet und Mobile
- **Animationen**: Flüssige Übergänge und Micro-Interactions

## 📋 Voraussetzungen

- Python 3.11 oder höher
- Docker & Docker Compose (optional)

## 🔧 Installation & Start

### Methode 1: Direkt mit Python

```bash
# Repository klonen
git clone <repository-url>
cd L8teHubb

# Server starten
python server.py
```

Die Website ist dann unter `http://localhost:8000` erreichbar.

### Methode 2: Mit Docker

```bash
# Docker Image bauen und Container starten
docker-compose up -d

# Logs anzeigen
docker-compose logs -f

# Container stoppen
docker-compose down
```

### Methode 3: Docker ohne Compose

```bash
# Image bauen
docker build -t l8tenever-web .

# Container starten
docker run -d -p 8000:8000 --name l8tenever-website l8tenever-web

# Container stoppen
docker stop l8tenever-website
docker rm l8tenever-website
```

## 🌐 Zugriff

- **Lokal**: http://localhost:8000
- **Netzwerk**: http://<deine-ip>:8000

## 📁 Projektstruktur

```
L8teHubb/
├── index.html          # Haupt-HTML-Datei
├── server.py           # Python HTTP-Server
├── Dockerfile          # Docker-Konfiguration
├── docker-compose.yml  # Docker Compose Setup
├── .gitignore          # Git-Ausschlüsse
└── README.md           # Diese Datei
```

## 🎨 Technologien

- **Frontend**: HTML5, CSS3 (Tailwind CSS), Vanilla JavaScript
- **Backend**: Python 3.11 (http.server)
- **Design**: Material You / Material Design 3
- **Fonts**: Google Sans
- **Container**: Docker

## 🔒 Sicherheit

Der Server läuft standardmäßig auf `0.0.0.0:8000` und ist im Netzwerk erreichbar. Für Produktionsumgebungen sollte ein Reverse Proxy (nginx, Apache) mit SSL/TLS verwendet werden.

## 📝 Lizenz

© 2026 L8teNever - Alle Rechte vorbehalten

## 🤝 Kontakt

- GitHub: https://github.com
- Instagram: https://instagram.com
- E-Mail: hello@l8tenever.com
