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

# Content-Datei (optional, falls jemand doch eine Datei nutzen will, aber Env-Vars haben Vorrang)
CONTENT_FILE = 'content.json'

# Nur Deutsch
DEFAULT_LANGUAGE = 'de'

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
    """Lädt den Content aus Umgebungsvariablen oder der JSON-Datei"""
    content = DEFAULT_CONTENT.copy()
    
    # Versuche aus Datei zu laden (als Basis)
    if os.path.exists(CONTENT_FILE):
        try:
            with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
                content.update(json.load(f))
        except:
            pass

    # Umgebungsvariablen haben Vorrang
    # Basis-Infos
    content['name'] = os.environ.get('HUB_NAME', content['name'])
    content['subtitle_de'] = os.environ.get('HUB_SUBTITLE_DE', content['subtitle_de'])
    content['subtitle_en'] = os.environ.get('HUB_SUBTITLE_EN', content['subtitle_en'])
    content['age'] = os.environ.get('HUB_AGE', content['age'])
    content['status_de'] = os.environ.get('HUB_STATUS_DE', content['status_de'])
    content['status_en'] = os.environ.get('HUB_STATUS_EN', content['status_en'])
    content['vibe'] = os.environ.get('HUB_VIBE', content['vibe'])
    content['location'] = os.environ.get('HUB_LOCATION', content['location'])
    content['github_url'] = os.environ.get('HUB_GITHUB_URL', content['github_url'])
    content['instagram_url'] = os.environ.get('HUB_INSTAGRAM_URL', content['instagram_url'])
    content['email'] = os.environ.get('HUB_EMAIL', content['email'])
    content['address'] = os.environ.get('HUB_ADDRESS', content['address'])

    # Haupt-Links (z.B. GitHub, Instagram oder eigene)
    main_links = []
    
    # Standard-Links wenn vorhanden
    if os.environ.get('HUB_GITHUB_URL'):
        main_links.append({'id': 'link-github', 'name': 'GitHub', 'url': os.environ.get('HUB_GITHUB_URL'), 'icon': 'github', 'desc_de': 'Meine Projekte', 'desc_en': 'My Projects'})
    if os.environ.get('HUB_INSTAGRAM_URL'):
        main_links.append({'id': 'link-instagram', 'name': 'Instagram', 'url': os.environ.get('HUB_INSTAGRAM_URL'), 'icon': 'instagram', 'desc_de': 'Folge mir', 'desc_en': 'Follow me'})

    # Zusätzliche Links: HUB_MAIN_LINK_1=Name | URL | Icon | Desc DE | Desc EN
    for i in range(1, 6):
        link_val = os.environ.get(f'HUB_MAIN_LINK_{i}')
        if link_val:
            parts = [p.strip() for p in link_val.split('|')]
            if len(parts) >= 5:
                main_links.append({
                    'id': f'link-custom-{i}',
                    'name': parts[0],
                    'url': parts[1],
                    'icon': parts[2],
                    'desc_de': parts[3],
                    'desc_en': parts[4]
                })
    content['main_links'] = main_links

    # Hub Buttons als JSON String (mit Auto-ID falls fehlt)
    buttons_json = os.environ.get('HUB_BUTTONS')
    if buttons_json:
        try:
            btns = json.loads(buttons_json)
            if isinstance(btns, list):
                for i, b in enumerate(btns):
                    if 'id' not in b:
                        b['id'] = str(i + 1)
                content['hub_buttons'] = btns
        except:
            print("Error parsing HUB_BUTTONS environment variable")

    # Alternativ: Einzelne Buttons (viel einfacher zu schreiben)
    # Format: HUB_BUTTON_1=Name DE | Name EN | Desc DE | Desc EN | URL | Icon
    env_buttons = []
    for i in range(1, 21):  # Unterstütze bis zu 20 Buttons
        btn_val = os.environ.get(f'HUB_BUTTON_{i}')
        if btn_val:
            parts = [p.strip() for p in btn_val.split('|')]
            if len(parts) >= 6:
                env_buttons.append({
                    'id': str(i),
                    'name_de': parts[0],
                    'name_en': parts[1],
                    'desc_de': parts[2],
                    'desc_en': parts[3],
                    'url': parts[4],
                    'icon': parts[5]
                })
    
    if env_buttons:
        content['hub_buttons'] = env_buttons

    # Dynamische Info-Karten für "Über mich"
    about_info = []
    
    # Standard-Infos (nur hinzufügen wenn vorhanden)
    def add_info(label_de, label_en, val_de, val_en):
        if val_de or val_en:
            about_info.append({
                'label_de': label_de,
                'label_en': label_en,
                'value_de': val_de or val_en,
                'value_en': val_en or val_de
            })

    add_info('Alter', 'Age', os.environ.get('HUB_AGE'), os.environ.get('HUB_AGE'))
    add_info('Status', 'Status', os.environ.get('HUB_STATUS_DE'), os.environ.get('HUB_STATUS_EN'))
    add_info('Vibe', 'Vibe', os.environ.get('HUB_VIBE'), os.environ.get('HUB_VIBE'))
    add_info('Standort', 'Location', os.environ.get('HUB_LOCATION'), os.environ.get('HUB_LOCATION'))

    # Zusätzliche flexible Infos: HUB_INFO_1=Label DE | Label EN | Value DE | Value EN
    for i in range(1, 11):
        info_val = os.environ.get(f'HUB_INFO_{i}')
        if info_val:
            parts = [p.strip() for p in info_val.split('|')]
            if len(parts) >= 4:
                add_info(parts[0], parts[1], parts[2], parts[3])

    content['about_info'] = about_info

    # Interessen (Komma-getrennte Liste)
    interests_str = os.environ.get('HUB_INTERESTS')
    if interests_str:
        content['interests'] = [i.strip() for i in interests_str.split(',')]
    elif 'interests' not in content:
        content['interests'] = ['UI/UX', 'Branding', 'Coding']

    # Impressum
    content['impressum']['company'] = os.environ.get('HUB_IMPRESSUM_COMPANY', content['impressum']['company'])
    content['impressum']['address_line1'] = os.environ.get('HUB_IMPRESSUM_ADDR1', content['impressum']['address_line1'])
    content['impressum']['address_line2'] = os.environ.get('HUB_IMPRESSUM_ADDR2', content['impressum']['address_line2'])
    content['impressum']['country'] = os.environ.get('HUB_IMPRESSUM_COUNTRY', content['impressum']['country'])
    content['impressum']['email'] = os.environ.get('HUB_IMPRESSUM_EMAIL', content['impressum']['email'])
    content['impressum']['responsible'] = os.environ.get('HUB_IMPRESSUM_RESPONSIBLE', content['impressum']['responsible'])

    # Datenschutz
    content['privacy']['intro_de'] = os.environ.get('HUB_PRIVACY_INTRO_DE', content['privacy']['intro_de'])
    content['privacy']['intro_en'] = os.environ.get('HUB_PRIVACY_INTRO_EN', content['privacy']['intro_en'])
    content['privacy']['data_processing_de'] = os.environ.get('HUB_PRIVACY_PROCESSING_DE', content['privacy']['data_processing_de'])
    content['privacy']['data_processing_en'] = os.environ.get('HUB_PRIVACY_PROCESSING_EN', content['privacy']['data_processing_en'])
    content['privacy']['server_logs_de'] = os.environ.get('HUB_PRIVACY_LOGS_DE', content['privacy']['server_logs_de'])
    content['privacy']['server_logs_en'] = os.environ.get('HUB_PRIVACY_LOGS_EN', content['privacy']['server_logs_en'])

    return content


@app.after_request
def set_security_headers(response):
    """Setzt Sicherheits-Header"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    # Content Security Policy - Etwas gelockert für bessere Kompatibilität
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "connect-src 'self' *; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
    )
    return response


@app.route('/')
def index():
    """Hauptseite (nur Deutsch)"""
    content = load_content()
    
    # Lese die HTML-Datei
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            html = f.read()
    else:
        return "index.html not found", 404
    
    # Füge Content als JavaScript-Variable hinzu
    inject_script = f"""
    <script>
        window.isLoggedIn = false;
        window.siteContent = {json.dumps(content)};
        window.currentPage = 'overview';
    </script>
    """
    
    # Injiziere vor dem schließenden </head>
    html = html.replace('</head>', inject_script + '</head>')
    
    return render_template_string(html)


@app.route('/hub/')
@app.route('/h/')
@app.route('/L8teHub/')
def hub():
    """Hub-Seite (nur Deutsch) - erreichbar unter /hub/, /h/ oder /L8teHub/"""
    content = load_content()
    
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    inject_script = f"""
    <script>
        window.isLoggedIn = false;
        window.siteContent = {json.dumps(content)};
        window.currentPage = 'hub';
    </script>
    """
    
    html = html.replace('</head>', inject_script + '</head>')
    return render_template_string(html)


@app.route('/about/')
def about():
    """About-Seite (nur Deutsch)"""
    content = load_content()
    
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    inject_script = f"""
    <script>
        window.isLoggedIn = false;
        window.siteContent = {json.dumps(content)};
        window.currentPage = 'about';
    </script>
    """
    
    html = html.replace('</head>', inject_script + '</head>')
    return render_template_string(html)


@app.route('/impressum/')
def impressum():
    """Impressum-Seite (Client-side rendering)"""
    content = load_content()
    
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    inject_script = f"""
    <script>
        window.isLoggedIn = false;
        window.siteContent = {json.dumps(content)};
        window.currentPage = 'impressum';
    </script>
    """
    html = html.replace('</head>', inject_script + '</head>')
    return render_template_string(html)


@app.route('/datenschutz/')
def datenschutz():
    """Datenschutz-Seite (Client-side rendering)"""
    content = load_content()
    
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    inject_script = f"""
    <script>
        window.isLoggedIn = false;
        window.siteContent = {json.dumps(content)};
        window.currentPage = 'datenschutz';
    </script>
    """
    html = html.replace('</head>', inject_script + '</head>')
    return render_template_string(html)


@app.route('/api/content', methods=['GET'])
def get_content():
    """Gibt den aktuellen Content zurück"""
    return jsonify(load_content())


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
    ║  Lokaler Zugriff:    http://localhost:{port}/              ║
    ║  Netzwerk-Zugriff:   http://{host}:{port}/                 ║
    ╠════════════════════════════════════════════════════════════╣
    ║  Konfiguration:                                           ║
    ║  Inhalte über Umgebungsvariablen in der docker-compose    ║
    ╠════════════════════════════════════════════════════════════╣
    ║  Sicherheitsfeatures:                                     ║
    ║  ✓ Security Headers                                       ║
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
