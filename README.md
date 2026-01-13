# L8teNever Website

Eine moderne, responsive Website mit Material You Design (Android 16 inspiriert).

## 🚀 Features

- **Material You Design**: Moderne UI mit dynamischen Farbschemata
- **Dark Mode**: Automatische Erkennung und manueller Toggle
- **Mehrsprachig**: Deutsch & Englisch mit URL-basierter Navigation (/de/, /en/)
- **Responsive**: Optimiert für Desktop, Tablet und Mobile
- **Animationen**: Flüssige Übergänge und Micro-Interactions
- **Admin-Login**: Geschützter Bereich zum Bearbeiten der Inhalte (ohne Registrierung)
- **Content-Management**: Einfaches Bearbeiten von Texten, Links und Profil-Informationen
- **Sicherheit**: 
  - ✓ Rate Limiting (5 Login-Versuche / 5 Minuten)
  - ✓ CSRF Protection
  - ✓ Security Headers (CSP, X-Frame-Options, etc.)
  - ✓ Input Validation & Sanitization
  - ✓ Sichere Session-Cookies

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

- **Deutsch**: http://localhost:8000/de/
- **English**: http://localhost:8000/en/
- **Netzwerk**: http://<deine-ip>:8000/de/

Die Sprache wird über die URL gesteuert. Wechsle zwischen `/de/` und `/en/` für Deutsch und Englisch.

## 🔐 Admin-Login

Die Website verfügt über einen geschützten Admin-Bereich zum Bearbeiten der Inhalte.

### Standard-Zugangsdaten

- **Username**: `admin`
- **Password**: `admin123`

⚠️ **WICHTIG**: Ändere diese Zugangsdaten für Produktionsumgebungen!

### Zugangsdaten ändern

#### Für Docker (empfohlen):

Bearbeite die `docker-compose.yml` Datei und ändere die Umgebungsvariablen:

```yaml
environment:
  - ADMIN_USER=dein_username
  - ADMIN_PASS=dein_sicheres_passwort
  - SECRET_KEY=dein_geheimer_schlüssel
```

Dann starte den Container neu:
```bash
docker-compose down
docker-compose up -d
```

#### Für direkten Python-Start:

Setze die Umgebungsvariablen vor dem Start:

**Windows (PowerShell):**
```powershell
$env:ADMIN_USER="dein_username"
$env:ADMIN_PASS="dein_passwort"
$env:SECRET_KEY="dein_secret"
python server.py
```

**Linux/Mac:**
```bash
export ADMIN_USER="dein_username"
export ADMIN_PASS="dein_passwort"
export SECRET_KEY="dein_secret"
python server.py
```

### Content bearbeiten

1. Klicke auf "Login" im Footer
2. Melde dich mit deinen Zugangsdaten an
3. Klicke auf "Edit" im Footer
4. Bearbeite die Felder und klicke auf "Speichern"
5. Die Änderungen werden in `content.json` gespeichert und bleiben auch nach Container-Neustarts erhalten

## 📁 Projektstruktur

```
L8teHubb/
├── index.html          # Haupt-HTML-Datei
├── admin.js            # Admin-Login und Content-Management
├── server.py           # Flask-Server mit API-Endpunkten
├── requirements.txt    # Python-Abhängigkeiten
├── content.json        # Gespeicherte Inhalte (wird automatisch erstellt)
├── Dockerfile          # Docker-Konfiguration
├── docker-compose.yml  # Docker Compose Setup (enthält alle Konfigurationen)
├── .gitignore          # Git-Ausschlüsse
└── README.md           # Diese Datei
```

**Hinweis**: Alle Konfigurationen (Admin-Zugangsdaten, etc.) sind direkt in der `docker-compose.yml` definiert - keine separate `.env` Datei nötig!

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
