"""
Lightweight local launcher for the Annotation Interface.
Starts a local HTTP server on port 8000 and opens the browser.
No external network connection, telemetry, or third-party service required.
"""
import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

PORT = 8000
APP_DIR = Path(__file__).resolve().parent

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)

def launch():
    print(f"==================================================")
    print(f"Translation Fidelity Annotation Interface Launcher")
    print(f"Serving locally from: {APP_DIR}")
    print(f"Access URL: http://localhost:{PORT}/index.html")
    print(f"Press Ctrl+C to terminate the local server.")
    print(f"==================================================")
    
    webbrowser.open(f"http://localhost:{PORT}/index.html")
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down local server.")

if __name__ == "__main__":
    launch()
