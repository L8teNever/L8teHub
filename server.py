#!/usr/bin/env python3
"""
L8teNever Website Server
Ein einfacher HTTP-Server zum Hosten der L8teNever Website
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP Request Handler mit verbessertem Logging"""
    
    def __init__(self, *args, **kwargs):
        # Setze das Verzeichnis, aus dem Dateien serviert werden
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def log_message(self, format, *args):
        """Überschreibe Log-Format für bessere Lesbarkeit"""
        sys.stdout.write("%s - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format % args))
    
    def end_headers(self):
        """Füge CORS-Header hinzu für bessere Kompatibilität"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()


def run_server(port=8000, host='0.0.0.0'):
    """
    Startet den HTTP-Server
    
    Args:
        port (int): Port-Nummer (Standard: 8000)
        host (str): Host-Adresse (Standard: 0.0.0.0 für alle Interfaces)
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
    
    print(f"""
╔════════════════════════════════════════════════════════════╗
║           L8teNever Website Server gestartet              ║
╠════════════════════════════════════════════════════════════╣
║  Lokaler Zugriff:    http://localhost:{port}               ║
║  Netzwerk-Zugriff:   http://{host}:{port}                  ║
╠════════════════════════════════════════════════════════════╣
║  Drücke STRG+C zum Beenden                                ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n[INFO] Server wird beendet...")
        httpd.shutdown()
        print("[INFO] Server erfolgreich beendet.")


if __name__ == "__main__":
    # Port aus Umgebungsvariable oder Standard
    PORT = int(os.environ.get('PORT', 8000))
    HOST = os.environ.get('HOST', '0.0.0.0')
    
    run_server(port=PORT, host=HOST)
