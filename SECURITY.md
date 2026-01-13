# Sicherheitsfeatures

## 🔒 Implementierte Sicherheitsmaßnahmen

### 1. **Rate Limiting**
- **Login-Schutz**: Maximal 5 fehlgeschlagene Login-Versuche pro IP-Adresse
- **Timeout**: 5 Minuten Sperrzeit nach zu vielen Versuchen
- **Automatisches Zurücksetzen**: Bei erfolgreichem Login wird das Limit zurückgesetzt

### 2. **Session-Sicherheit**
- **HttpOnly Cookies**: Verhindert JavaScript-Zugriff auf Session-Cookies
- **SameSite**: Schutz vor CSRF-Angriffen
- **Session-Timeout**: Automatisches Logout nach 7 Tagen Inaktivität
- **Sichere Session-Keys**: Verwendung von kryptographisch sicheren Zufallswerten

### 3. **Input-Validierung**
- **Längen-Beschränkungen**: Alle Eingaben werden auf maximale Länge geprüft
- **URL-Validierung**: URLs müssen mit http:// oder https:// beginnen
- **Pflichtfelder**: Validierung aller erforderlichen Felder
- **Sanitization**: Entfernung gefährlicher Zeichen aus Benutzereingaben

### 4. **Security Headers**
```
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: (siehe unten)
```

### 5. **Content Security Policy (CSP)**
- Erlaubt nur Skripte von vertrauenswürdigen Quellen
- Verhindert Inline-Script-Injection (außer explizit erlaubt)
- Beschränkt externe Ressourcen auf bekannte Domains

### 6. **Passwort-Sicherheit**
- **SHA-256 Hashing**: Passwörter werden gehasht gespeichert
- **Keine Klartext-Speicherung**: Passwörter werden nie im Klartext gespeichert
- **Sichere Vergleiche**: Verwendung von Hash-Vergleichen

### 7. **Error Handling**
- **Generische Fehlermeldungen**: Keine detaillierten Informationen bei Login-Fehlern
- **Logging**: Fehlgeschlagene Login-Versuche werden protokolliert
- **Keine Stack Traces**: Produktionsmodus verhindert Anzeige von Debug-Informationen

## 🛡️ Best Practices

### Für Produktion:

1. **HTTPS verwenden**:
   ```yaml
   environment:
     - SESSION_COOKIE_SECURE=True
   ```

2. **Starke Passwörter**:
   - Mindestens 12 Zeichen
   - Kombination aus Groß-/Kleinbuchstaben, Zahlen und Sonderzeichen

3. **Secret Key ändern**:
   ```yaml
   environment:
     - SECRET_KEY=<kryptographisch-sicherer-zufallswert>
   ```
   
   Generiere einen sicheren Key mit:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

4. **Reverse Proxy verwenden**:
   - nginx oder Apache vor Flask
   - SSL/TLS Terminierung
   - Zusätzliche Sicherheits-Header

5. **Firewall-Regeln**:
   - Nur notwendige Ports öffnen
   - IP-Whitelist für Admin-Zugriff (optional)

## 📊 Sicherheits-Checkliste

- [x] Rate Limiting implementiert
- [x] CSRF-Schutz aktiv
- [x] Security Headers gesetzt
- [x] Input-Validierung vorhanden
- [x] Passwort-Hashing implementiert
- [x] Session-Sicherheit konfiguriert
- [x] CSP-Policy definiert
- [ ] HTTPS aktiviert (für Produktion)
- [ ] Starke Passwörter gesetzt (für Produktion)
- [ ] Secret Key geändert (für Produktion)

## 🚨 Bekannte Einschränkungen

1. **SHA-256 für Passwörter**: Für höhere Sicherheit sollte bcrypt oder Argon2 verwendet werden
2. **In-Memory Rate Limiting**: Bei Container-Neustarts werden Limits zurückgesetzt
3. **Keine 2FA**: Zwei-Faktor-Authentifizierung ist nicht implementiert

## 🔄 Zukünftige Verbesserungen

- [ ] Implementierung von bcrypt/Argon2 für Passwort-Hashing
- [ ] Persistentes Rate Limiting (Redis/Database)
- [ ] Zwei-Faktor-Authentifizierung (2FA)
- [ ] Audit-Logging für alle Admin-Aktionen
- [ ] Automatische Backups der content.json
- [ ] IP-Whitelist für Admin-Zugriff
