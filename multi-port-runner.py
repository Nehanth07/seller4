#!/usr/bin/env python3
"""
Multi-Port HTML Page Runner
Serves all HTML pages and projects on different ports
"""

import os
import subprocess
import sys
import time
from pathlib import Path
import glob
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import signal

WORKSPACE_ROOT = Path(__file__).parent
PORT_BASE = 8000
SERVERS = []
PORTS_USED = {}

# Define project mappings
PROJECTS = {
    # Subdirectory projects with their own entry points
    "247artists": {
        "path": "247artists",
        "entry": "index.html",
        "port": 8001,
        "name": "247 Artists"
    },
    "generous-branding": {
        "path": "generous branding",
        "entry": "index.html", 
        "port": 8095,
        "name": "Generous Branding"
    },
    "interrent-cars": {
        "path": "interent-cars",
        "entry": "index.html",
        "port": 8090,
        "name": "Interrent Cars"
    },
    "smart-prehospital": {
        "path": "smart-prehospital",
        "entry": "index.html",
        "port": 8092,
        "name": "Smart Prehospital"
    },
    "sydney-telugu-badi": {
        "path": "sydney-telugu-badi",
        "entry": "index.html",
        "port": 8097,
        "name": "Sydney Telugu Badi"
    },
}

# Root level HTML files (main entry points)
ROOT_PAGES = [
    ("index.html", 8002, "Home Index"),
    ("2nd page.html", 8003, "2nd Page"),
    ("page-runner.html", 8004, "Page Runner"),
    ("reelongo.html", 8005, "Reelongo"),
    ("book.html", 8006, "Book"),
    ("services.html", 8007, "Services"),
    ("locations.html", 8008, "Locations"),
    ("fleet.html", 8009, "Fleet"),
    ("how-it-works.html", 8010, "How It Works"),
]

class CustomHTTPHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress logging

def start_server(path, port, description):
    """Start an HTTP server for a specific directory"""
    original_dir = os.getcwd()
    try:
        os.chdir(path)
        
        class Handler(CustomHTTPHandler):
            pass
        
        server = HTTPServer(('127.0.0.1', port), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        
        SERVERS.append(server)
        PORTS_USED[port] = {
            "description": description,
            "path": str(path),
            "url": f"http://127.0.0.1:{port}/"
        }
        
        print(f"✓ {description:30} → http://127.0.0.1:{port}/")
        return server
    except Exception as e:
        print(f"✗ Failed to start server for {description} on port {port}: {e}")
        return None
    finally:
        os.chdir(original_dir)

def create_dashboard():
    """Create an HTML dashboard listing all servers"""
    dashboard_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Comparison Dashboard</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }
        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        .card h2 {
            margin: 0 0 10px 0;
            font-size: 18px;
            color: #333;
        }
        .card p {
            margin: 8px 0;
            color: #666;
            font-size: 14px;
        }
        .port-badge {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 8px;
        }
        .path-badge {
            display: inline-block;
            background: #f0f0f0;
            color: #333;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-top: 10px;
        }
        .open-btn {
            display: inline-block;
            margin-top: 12px;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            transition: background 0.2s;
            border: none;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
        }
        .open-btn:hover {
            background: #764ba2;
        }
        .stats {
            background: white;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            margin-top: 30px;
        }
        .stats p {
            margin: 8px 0;
            color: #666;
        }
        .info-message {
            background: rgba(255,255,255,0.1);
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Page Comparison Dashboard</h1>
        <div class="info-message">
            Click any "Open" button below to preview a page in a new tab. You can open multiple pages side-by-side to compare them.
        </div>
        <div class="projects-grid">
"""
    
    # Add projects from PORTS_USED
    ports_sorted = sorted(PORTS_USED.items())
    for port, info in ports_sorted:
        dashboard_html += f"""
            <div class="card">
                <h2>{info['description']}</h2>
                <p>
                    <span class="port-badge">Port {port}</span>
                </p>
                <div class="path-badge">{info['path']}</div>
                <button class="open-btn" onclick="window.open('{info['url']}', '_blank')">
                    Open Page →
                </button>
            </div>
"""
    
    dashboard_html += """
        </div>
        <div class="stats">
            <h2>Server Status</h2>
            <p>✓ All servers are running</p>
"""
    dashboard_html += f"            <p>{len(PORTS_USED)} pages available for comparison</p>\n"
    dashboard_html += """
        </div>
    </div>
</body>
</html>"""
    
    dashboard_path = WORKSPACE_ROOT / "dashboard.html"
    with open(dashboard_path, 'w') as f:
        f.write(dashboard_html)
    
    return dashboard_path

def signal_handler(sig, frame):
    """Handle shutdown gracefully"""
    print("\n\nShutting down servers...")
    for server in SERVERS:
        server.shutdown()
    sys.exit(0)

def main():
    print("\n" + "="*60)
    print("Multi-Port HTML Page Runner")
    print("="*60 + "\n")
    
    os.chdir(WORKSPACE_ROOT)
    
    # Start project servers
    print("Starting project servers...")
    for key, project in PROJECTS.items():
        project_path = WORKSPACE_ROOT / project['path']
        if project_path.exists():
            start_server(project_path, project['port'], project['name'])
        else:
            print(f"✗ {project['name']:30} → Path not found: {project['path']}")
    
    # Start root level page servers
    print("\nStarting root page servers...")
    for filename, port, description in ROOT_PAGES:
        file_path = WORKSPACE_ROOT / filename
        if file_path.exists():
            # For root pages, we serve from root but with a unique handler
            start_server(WORKSPACE_ROOT, port, description)
        else:
            print(f"✗ {description:30} → File not found: {filename}")
    
    # Create and serve dashboard
    print("\nGenerating dashboard...")
    dashboard_path = create_dashboard()
    start_server(WORKSPACE_ROOT, 7999, "Dashboard")
    
    print("\n" + "="*60)
    print("📊 Dashboard: http://127.0.0.1:7999/dashboard.html")
    print("="*60)
    print("\nAll servers are running! Press Ctrl+C to stop all servers.\n")
    
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == '__main__':
    main()
