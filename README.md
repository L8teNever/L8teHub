# 🌌 L8teHub - Modern Material You Hub

![L8teHub Banner](https://img.shields.io/badge/UI-Material_You-blue?style=for-the-badge&logo=android)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)

Eine moderne, hochgradig anpassbare Hub-Website mit **Material You Design** (Android 16 inspiriert). Perfekt für Portfolios, Link-Sammlungen oder als Schaltzentrale für deine digitalen Projekte.

---

## ✨ Features

- **🎨 Android 16 Visuals**: Modernstes UI-Design mit dynamischen Farbschemata (Material Design 3).
- **🌓 Adaptive Themes**: Automatischer Dark Mode mit manuellem Toggle für erstklassige Ästhetik.
- **📱 Responsive by Design**: Nahtlose Erfahrung auf Desktop, Tablet und Smartphone.
- **⚙️ Dynamic Content**: Zentrale Steuerung aller Inhalte über Umgebungsvariablen oder JSON.
- **🛡️ Secure & Lightweight**: Flask-Backend mit eingebauten Security Headers (CSP, HSTS, etc.) und Rate Limiting.

---

## 🚀 Schnellstart

### 🐳 Mit Docker (Empfohlen)

Das Projekt ist vollständig für Docker optimiert. Nutze das mitgelieferte Docker Compose für ein One-Click Setup:

```bash
# Starten des Hubs
docker-compose up -d
```

### 🐍 Mit Python

Falls du Docker nicht nutzen möchtest, kannst du den Server direkt mit Python starten:

```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# Server starten
python server.py
```
*Besuche anschließend `http://localhost:8000/` in deinem Browser.*

---

## 🛠️ Konfiguration

Alle wichtigen Informationen lassen sich einfach über die `docker-compose.yml` (Umgebungsvariablen) anpassen:

| Variable | Beschreibung | Standard |
| :--- | :--- | :--- |
| `ADMIN_USER` | Nutzername für den Admin-Bereich | `admin` |
| `ADMIN_PASS` | Passwort für den Admin-Bereich | `admin123` |
| `HUB_NAME` | Dein Name / Projektname | `L8teNever` |
| `HUB_LOCATION` | Dein Standort | `Deutschland` |
| `SECRET_KEY` | Schlüssel für Sessions | *Zufällig* |

---

## 📂 Projektstruktur

```text
L8teHub/
├── index.html          # Core UI (Material You Design System)
├── server.py           # Flask Backend & API
├── content.json        # Dynamische Inhalte (Optional)
├── Dockerfile          # Container-Definition
├── docker-compose.yml  # Deployment-Konfiguration
└── requirements.txt    # Python-Packages
```

---

## 📜 Lizenz & Kontakt

© 2026 **L8teNever** - Alle Rechte vorbehalten.

- **GitHub**: [@L8teNever](https://github.com)
- **Instagram**: [@L8teNever](https://instagram.com)
- **Email**: [hello@l8tenever.com](mailto:hello@l8tenever.com)

---
*Developed with ❤️ by L8teNever*
