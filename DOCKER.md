# Docker Deployment

## 🐳 Zwei Deployment-Optionen

### Option 1: Lokale Entwicklung (Build lokal)

Verwendet `docker-compose.yml` - baut das Image lokal:

```bash
docker-compose up -d
```

### Option 2: Produktion (Image von Docker Hub)

Verwendet `docker-compose.prod.yml` - zieht das fertige Image von Docker Hub:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📋 Voraussetzungen für Produktion

Das Image muss auf Docker Hub verfügbar sein:
- **Image Name**: `l8tenever/l8tehub:latest`
- **Automatischer Build**: Via GitHub Actions bei jedem Push

## 🚀 Schnellstart (Produktion)

1. **Image von Docker Hub ziehen und starten**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Logs anzeigen**:
   ```bash
   docker-compose -f docker-compose.prod.yml logs -f
   ```

3. **Stoppen**:
   ```bash
   docker-compose -f docker-compose.prod.yml down
   ```

4. **Neueste Version ziehen**:
   ```bash
   docker-compose -f docker-compose.prod.yml pull
   docker-compose -f docker-compose.prod.yml up -d
   ```

## 🔧 Konfiguration anpassen

Bearbeite `docker-compose.prod.yml` und ändere die Umgebungsvariablen:

```yaml
environment:
  - ADMIN_USER=dein_username
  - ADMIN_PASS=dein_sicheres_passwort
  - SECRET_KEY=dein_geheimer_schlüssel
```

## 📊 Unterschiede

| Feature | docker-compose.yml | docker-compose.prod.yml |
|---------|-------------------|------------------------|
| **Verwendung** | Lokale Entwicklung | Produktion |
| **Image-Quelle** | Lokal gebaut | Docker Hub |
| **Build-Zeit** | Ja (bei jedem Start) | Nein (nur Download) |
| **Geschwindigkeit** | Langsamer | Schneller |
| **Updates** | Manuell | `docker-compose pull` |

## 🎯 Empfehlung

- **Entwicklung**: `docker-compose.yml` (lokaler Build)
- **Server/Produktion**: `docker-compose.prod.yml` (Docker Hub Image)

## 🔄 Update-Workflow (Produktion)

1. Code ändern und committen
2. GitHub Actions baut automatisch neues Image
3. Auf dem Server:
   ```bash
   docker-compose -f docker-compose.prod.yml pull
   docker-compose -f docker-compose.prod.yml up -d
   ```

Das war's! 🎉
