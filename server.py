#!/usr/bin/env python3
"""
L8teNever Website Server
Flask-basierter Server mit Login und Content-Management
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for, abort
import os
import json
import hashlib
import secrets
from datetime import timedelta, datetime
from functools import wraps
from collections import defaultdict
import time

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'l8tenever-secret-key-change-in-production-2026')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = False  # Setze auf True wenn HTTPS verwendet wird
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Fester Admin-Account (keine Registrierung möglich)
ADMIN_CREDENTIALS = {
    'username': os.environ.get('ADMIN_USER', 'admin'),
    'password_hash': hashlib.sha256(os.environ.get('ADMIN_PASS', 'admin123').encode()).hexdigest()
}

# Content-Datei
CONTENT_FILE = 'content.json'

# Unterstützte Sprachen
SUPPORTED_LANGUAGES = ['de', 'en']
DEFAULT_LANGUAGE = 'de'

# Rate Limiting
login_attempts = defaultdict(list)
MAX_LOGIN_ATTEMPTS = 5
LOGIN_TIMEOUT = 300  # 5 Minuten

# Standard-Content
DEFAULT_CONTENT = {
    'name': 'L8teNever',
    'subtitle_de': 'Digitaler Creator & Entwickler',
    'subtitle_en': 'Digital Creator & Developer',
    'age': '16',
    'status_de': 'Schüler',
    'status_en': 'Student',
    'vibe': 'Vibecoding',
    'location': 'Deutschland',
    'github_url': 'https://github.com',
    'instagram_url': 'https://instagram.com',
    'email': 'hello@l8tenever.com',
    'address': 'Musterstraße 123<br>12345 Berlin',
    
    # Hub-Buttons (editierbar)
    'hub_buttons': [
        {'id': 'L8teStudy', 'name_de': 'L8teStudy', 'name_en': 'L8teStudy', 'desc_de': 'Lernen', 'desc_en': 'Study', 'url': '#', 'icon': 'study'},
        {'id': 'L8teFuel', 'name_de': 'L8teFuel', 'name_en': 'L8teFuel', 'desc_de': 'Energie', 'desc_en': 'Energy', 'url': '#', 'icon': 'fuel'},
        {'id': 'L8teHabbit', 'name_de': 'L8teHabbit', 'name_en': 'L8teHabbit', 'desc_de': 'Routinen', 'desc_en': 'Habits', 'url': '#', 'icon': 'habbit'},
        {'id': 'L8teID', 'name_de': 'L8teID', 'name_en': 'L8teID', 'desc_de': 'Identität', 'desc_en': 'Identity', 'url': '#', 'icon': 'id'},
        {'id': 'L8teFlow', 'name_de': 'L8teFlow', 'name_en': 'L8teFlow', 'desc_de': 'Automatisierung', 'desc_en': 'Flows', 'url': '#', 'icon': 'flow'},
        {'id': 'L8teBot', 'name_de': 'L8teBot', 'name_en': 'L8teBot', 'desc_de': 'Assistent', 'desc_en': 'Bot', 'url': '#', 'icon': 'bot'}
    ],
    
    # Impressum Inhalte
    'impressum': {
        'company': 'L8teNever',
        'address_line1': 'Musterstraße 123',
        'address_line2': '12345 Berlin',
        'country': 'Deutschland',
        'email': 'hello@l8tenever.com',
        'responsible': 'L8teNever'
    },
    
    # Datenschutz Inhalte
    'privacy': {
        'intro_de': 'Diese Website verwendet keine Cookies und kein Tracking.',
        'intro_en': 'This website does not use cookies or tracking.',
        'data_processing_de': 'Wir verarbeiten keine personenbezogenen Daten. Die Website ist rein funktional und speichert keine Benutzerinformationen.',
        'data_processing_en': 'We do not process any personal data. This website is purely functional and does not store any user information.',
        'server_logs_de': 'Technisch bedingt werden beim Zugriff auf die Website temporäre Verbindungsdaten (IP-Adresse, Zeitstempel) im Server-Log gespeichert. Diese Daten werden nicht ausgewertet und nach 24 Stunden automatisch gelöscht.',
        'server_logs_en': 'For technical reasons, temporary connection data (IP address, timestamp) is stored in the server log when accessing the website. This data is not analyzed and is automatically deleted after 24 hours.'
    }
}


def load_content():
    """Lädt den Content aus der JSON-Datei"""
    if os.path.exists(CONTENT_FILE):
        try:
            with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return DEFAULT_CONTENT.copy()
    return DEFAULT_CONTENT.copy()


def save_content(content):
    """Speichert den Content in die JSON-Datei"""
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)


def check_rate_limit(ip):
    """Prüft Rate Limiting für Login-Versuche"""
    now = time.time()
    # Entferne alte Versuche
    login_attempts[ip] = [t for t in login_attempts[ip] if now - t < LOGIN_TIMEOUT]
    
    if len(login_attempts[ip]) >= MAX_LOGIN_ATTEMPTS:
        return False
    return True


def record_login_attempt(ip):
    """Zeichnet einen Login-Versuch auf"""
    login_attempts[ip].append(time.time())


def login_required(f):
    """Decorator für geschützte Routen"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({'error': 'Nicht angemeldet'}), 401
        return f(*args, **kwargs)
    return decorated_function


def validate_language(lang):
    """Validiert die Sprache"""
    return lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE


@app.after_request
def set_security_headers(response):
    """Setzt Sicherheits-Header"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
    )
    return response


@app.route('/')
def index_redirect():
    """Redirect zur deutschen Startseite"""
    return redirect(url_for('index', lang='de'))


@app.route('/<lang>/')
def index(lang):
    """Hauptseite mit Sprachunterstützung"""
    lang = validate_language(lang)
    content = load_content()
    
    # Lese die HTML-Datei
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Füge Login-Status, Content und Sprache als JavaScript-Variable hinzu
    inject_script = f"""
    <script>
        window.isLoggedIn = {'true' if session.get('logged_in') else 'false'};
        window.siteContent = {json.dumps(content)};
        window.currentLang = '{lang}';
        window.currentPage = 'overview';
    </script>
    """
    
    # Injiziere vor dem schließenden </head>
    html = html.replace('</head>', inject_script + '</head>')
    
    return render_template_string(html)


@app.route('/<lang>/hub/')
def hub(lang):
    """Hub-Seite mit Sprachunterstützung"""
    lang = validate_language(lang)
    content = load_content()
    
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    inject_script = f"""
    <script>
        window.isLoggedIn = {'true' if session.get('logged_in') else 'false'};
        window.siteContent = {json.dumps(content)};
        window.currentLang = '{lang}';
        window.currentPage = 'hub';
    </script>
    """
    
    html = html.replace('</head>', inject_script + '</head>')
    return render_template_string(html)


@app.route('/<lang>/about/')
def about(lang):
    """About-Seite mit Sprachunterstützung"""
    lang = validate_language(lang)
    content = load_content()
    
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    inject_script = f"""
    <script>
        window.isLoggedIn = {'true' if session.get('logged_in') else 'false'};
        window.siteContent = {json.dumps(content)};
        window.currentLang = '{lang}';
        window.currentPage = 'about';
    </script>
    """
    
    html = html.replace('</head>', inject_script + '</head>')
    return render_template_string(html)


@app.route('/<lang>/impressum/')
def impressum(lang):
    """Impressum-Seite im Material Design"""
    lang = validate_language(lang)
    content = load_content()
    
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Füge spezielle Marker für Impressum-Content hinzu
    inject_script = f"""
    <script>
        window.isLoggedIn = {'true' if session.get('logged_in') else 'false'};
        window.siteContent = {json.dumps(content)};
        window.currentLang = '{lang}';
        window.currentPage = 'impressum';
    </script>
    """
    
    html = html.replace('</head>', inject_script + '</head>')
    
    # Ersetze den Hauptinhalt mit Impressum
    impressum_content = f"""
    <div class="max-w-4xl mx-auto p-8 lg:p-16">
        <a href="/{lang}/" class="inline-flex items-center text-[var(--m3-primary)] hover:opacity-80 mb-8 font-semibold transition-opacity">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
            </svg>
            {'Zurück' if lang == 'de' else 'Back'}
        </a>
        
        <div class="android-card p-8 lg:p-12 bg-[var(--m3-surface-variant)] shadow-lg">
            <h1 class="text-4xl lg:text-5xl font-bold mb-8 text-[var(--m3-on-surface)]">
                {'Impressum' if lang == 'de' else 'Legal Notice'}
            </h1>
            
            <div class="space-y-6 text-[var(--m3-on-surface)]">
                <div class="android-card p-6 bg-[var(--m3-surface)] border border-transparent dark:border-[var(--m3-outline)]/20">
                    <p class="text-lg leading-relaxed">
                        <strong class="block mb-2">L8teNever</strong>
                        Musterstraße 123<br>
                        12345 Berlin<br>
                        Deutschland
                    </p>
                </div>
                
                <div class="android-card p-6 bg-[var(--m3-surface)] border border-transparent dark:border-[var(--m3-outline)]/20">
                    <p class="text-lg">
                        <strong class="block mb-2">E-Mail:</strong>
                        <a href="mailto:hello@l8tenever.com" class="text-[var(--m3-primary)] hover:opacity-80 transition-opacity">
                            hello@l8tenever.com
                        </a>
                    </p>
                </div>
                
                <div class="android-card p-6 bg-[var(--m3-surface)] border border-transparent dark:border-[var(--m3-outline)]/20">
                    <p class="text-lg">
                        <strong class="block mb-2">{'Verantwortlich für den Inhalt' if lang == 'de' else 'Responsible for content'}:</strong>
                        L8teNever
                    </p>
                </div>
            </div>
        </div>
    </div>
    """
    
    # Ersetze den page-overview Inhalt
    html = html.replace('<section id="page-overview"', f'<section id="page-overview" style="display:none;"')
    html = html.replace('</body>', impressum_content + '</body>')
    
    return render_template_string(html)


@app.route('/<lang>/datenschutz/')
def datenschutz(lang):
    """Datenschutz-Seite im Material Design"""
    lang = validate_language(lang)
    content = load_content()
    
    title = 'Datenschutz' if lang == 'de' else 'Privacy Policy'
    back_text = 'Zurück' if lang == 'de' else 'Back'
    
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    inject_script = f"""
    <script>
        window.isLoggedIn = {'true' if session.get('logged_in') else 'false'};
        window.siteContent = {json.dumps(content)};
        window.currentLang = '{lang}';
        window.currentPage = 'datenschutz';
    </script>
    """
    
    html = html.replace('</head>', inject_script + '</head>')
    
    datenschutz_content = f"""
    <div class="max-w-4xl mx-auto p-8 lg:p-16">
        <a href="/{lang}/" class="inline-flex items-center text-[var(--m3-primary)] hover:opacity-80 mb-8 font-semibold transition-opacity">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
            </svg>
            {back_text}
        </a>
        
        <div class="android-card p-8 lg:p-12 bg-[var(--m3-surface-variant)] shadow-lg">
            <h1 class="text-4xl lg:text-5xl font-bold mb-8 text-[var(--m3-on-surface)]">
                {title}
            </h1>
            
            <div class="space-y-6 text-[var(--m3-on-surface)]">
                <div class="android-card p-6 bg-[var(--m3-surface)] border border-transparent dark:border-[var(--m3-outline)]/20">
                    <p class="text-lg leading-relaxed">
                        {'Diese Website verwendet keine Cookies und kein Tracking.' if lang == 'de' else 'This website does not use cookies or tracking.'}
                    </p>
                </div>
                
                <div class="android-card p-6 bg-[var(--m3-surface)] border border-transparent dark:border-[var(--m3-outline)]/20">
                    <h2 class="text-2xl font-bold mb-4 text-[var(--m3-on-surface)]">
                        {'Datenverarbeitung' if lang == 'de' else 'Data Processing'}
                    </h2>
                    <p class="text-lg leading-relaxed opacity-80">
                        {'Wir verarbeiten keine personenbezogenen Daten. Die Website ist rein funktional und speichert keine Benutzerinformationen.' if lang == 'de' else 'We do not process any personal data. This website is purely functional and does not store any user information.'}
                    </p>
                </div>
                
                <div class="android-card p-6 bg-[var(--m3-surface)] border border-transparent dark:border-[var(--m3-outline)]/20">
                    <h2 class="text-2xl font-bold mb-4 text-[var(--m3-on-surface)]">
                        {'Server-Logs' if lang == 'de' else 'Server Logs'}
                    </h2>
                    <p class="text-lg leading-relaxed opacity-80">
                        {'Technisch bedingt werden beim Zugriff auf die Website temporäre Verbindungsdaten (IP-Adresse, Zeitstempel) im Server-Log gespeichert. Diese Daten werden nicht ausgewertet und nach 24 Stunden automatisch gelöscht.' if lang == 'de' else 'For technical reasons, temporary connection data (IP address, timestamp) is stored in the server log when accessing the website. This data is not analyzed and is automatically deleted after 24 hours.'}
                    </p>
                </div>
            </div>
        </div>
    </div>
    """
    
    html = html.replace('<section id="page-overview"', f'<section id="page-overview" style="display:none;"')
    html = html.replace('</body>', datenschutz_content + '</body>')
    
    return render_template_string(html)


@app.route('/admin.js')
def serve_admin_js():
    """Serviert die admin.js Datei"""
    with open('admin.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    return js_content, 200, {'Content-Type': 'application/javascript'}


@app.route('/api/login', methods=['POST'])
def login():
    """Login-Endpunkt mit Rate Limiting"""
    ip = request.remote_addr
    
    # Rate Limiting prüfen
    if not check_rate_limit(ip):
        return jsonify({
            'success': False, 
            'message': 'Zu viele Login-Versuche. Bitte warte 5 Minuten.'
        }), 429
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Ungültige Anfrage'}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    # Input-Validierung
    if not username or not password:
        record_login_attempt(ip)
        return jsonify({'success': False, 'message': 'Benutzername und Passwort erforderlich'}), 400
    
    if len(username) > 100 or len(password) > 100:
        record_login_attempt(ip)
        return jsonify({'success': False, 'message': 'Eingabe zu lang'}), 400
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if username == ADMIN_CREDENTIALS['username'] and password_hash == ADMIN_CREDENTIALS['password_hash']:
        session['logged_in'] = True
        session['username'] = username
        session.permanent = True
        # Login erfolgreich - Rate Limit zurücksetzen
        if ip in login_attempts:
            del login_attempts[ip]
        return jsonify({'success': True, 'message': 'Erfolgreich angemeldet'})
    
    # Fehlgeschlagener Login
    record_login_attempt(ip)
    return jsonify({'success': False, 'message': 'Ungültige Zugangsdaten'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout-Endpunkt"""
    session.clear()
    return jsonify({'success': True, 'message': 'Erfolgreich abgemeldet'})


@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    """Prüft ob User eingeloggt ist"""
    return jsonify({'logged_in': session.get('logged_in', False)})


@app.route('/api/content', methods=['GET'])
def get_content():
    """Gibt den aktuellen Content zurück"""
    return jsonify(load_content())


@app.route('/api/content', methods=['POST'])
@login_required
def update_content():
    """Aktualisiert den Content (nur für eingeloggte User)"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Keine Daten erhalten'}), 400
    
    # Validierung
    required_fields = ['name', 'subtitle_de', 'age', 'status_de', 'vibe', 'location']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Feld {field} fehlt'}), 400
    
    # Sanitize und validiere Eingaben
    sanitized_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            # Entferne gefährliche Zeichen (außer bei URLs und erlaubten HTML-Tags)
            if key.endswith('_url'):
                # URL-Validierung
                if not value.startswith(('http://', 'https://')):
                    return jsonify({'error': f'Ungültige URL: {key}'}), 400
            # Längen-Validierung
            if len(value) > 500:
                return jsonify({'error': f'Wert für {key} ist zu lang'}), 400
            sanitized_data[key] = value
        else:
            sanitized_data[key] = value
    
    save_content(sanitized_data)
    return jsonify({'success': True, 'message': 'Content erfolgreich aktualisiert'})


def run_server(port=8000, host='0.0.0.0'):
    """
    Startet den Flask-Server
    
    Args:
        port (int): Port-Nummer (Standard: 8000)
        host (str): Host-Adresse (Standard: 0.0.0.0 für alle Interfaces)
    """
    print(f"""
╔════════════════════════════════════════════════════════════╗
║           L8teNever Website Server gestartet              ║
╠════════════════════════════════════════════════════════════╣
║  Lokaler Zugriff:    http://localhost:{port}/de/           ║
║  Netzwerk-Zugriff:   http://{host}:{port}/de/              ║
╠════════════════════════════════════════════════════════════╣
║  Sprachen:                                                ║
║  - Deutsch:  /de/                                         ║
║  - English:  /en/                                         ║
╠════════════════════════════════════════════════════════════╣
║  Admin Login:                                             ║
║  Username: {ADMIN_CREDENTIALS['username']:<20}                           ║
║  Password: (siehe docker-compose.yml)                     ║
╠════════════════════════════════════════════════════════════╣
║  Sicherheitsfeatures:                                     ║
║  ✓ Rate Limiting (5 Versuche / 5 Min)                    ║
║  ✓ CSRF Protection                                        ║
║  ✓ Security Headers                                       ║
║  ✓ Input Validation                                       ║
╠════════════════════════════════════════════════════════════╣
║  Drücke STRG+C zum Beenden                                ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    # Port aus Umgebungsvariable oder Standard
    PORT = int(os.environ.get('PORT', 8000))
    HOST = os.environ.get('HOST', '0.0.0.0')
    
    run_server(port=PORT, host=HOST)
