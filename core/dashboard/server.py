#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

Real-Time Analytics Dashboard Server
"""
import json, time, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP handler for dashboard"""
    
    def __init__(self, *args, dashboard_data=None, **kwargs):
        self.dashboard_data = dashboard_data
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_dashboard_html().encode())
        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.dashboard_data.get_stats()).encode())
        elif self.path == '/api/attacks':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.dashboard_data.get_attacks()).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def get_dashboard_html(self):
        """Generate dashboard HTML"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>CBT Real-Time Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #fff; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: #2a2a2a; padding: 20px; border-radius: 8px; }
        .stat { font-size: 2em; color: #4CAF50; }
        canvas { max-height: 300px; }
    </style>
</head>
<body>
    <h1>CBT Real-Time Analytics Dashboard</h1>
    <div class="dashboard">
        <div class="card">
            <h3>Total Attacks</h3>
            <div class="stat" id="total-attacks">0</div>
        </div>
        <div class="card">
            <h3>Success Rate</h3>
            <div class="stat" id="success-rate">0%</div>
        </div>
        <div class="card">
            <h3>Active Botnets</h3>
            <div class="stat" id="active-botnets">0</div>
        </div>
        <div class="card">
            <h3>Attack Timeline</h3>
            <canvas id="timeline-chart"></canvas>
        </div>
        <div class="card">
            <h3>Attack Types</h3>
            <canvas id="types-chart"></canvas>
        </div>
    </div>
    <script>
        function updateDashboard() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('total-attacks').textContent = data.total_attacks || 0;
                    document.getElementById('success-rate').textContent = (data.success_rate * 100).toFixed(1) + '%';
                    document.getElementById('active-botnets').textContent = data.active_botnets || 0;
                });
            
            fetch('/api/attacks')
                .then(r => r.json())
                .then(data => {
                    updateCharts(data);
                });
        }
        
        function updateCharts(data) {
            // Update charts with data
        }
        
        setInterval(updateDashboard, 2000);
        updateDashboard();
    </script>
</body>
</html>
"""

class DashboardData(object):
    """Dashboard data manager"""
    
    def __init__(self, ufonet):
        self.ufonet = ufonet
        self.stats = {
            'total_attacks': 0,
            'success_rate': 0.0,
            'active_botnets': 0,
            'timestamp': time.time()
        }
        self.attacks = []
    
    def update_stats(self):
        """Update statistics"""
        self.stats['total_attacks'] = getattr(self.ufonet, 'total_zombie', 0)
        self.stats['active_botnets'] = len(getattr(self.ufonet, 'herd', {}).get('active', []))
        self.stats['timestamp'] = time.time()
    
    def get_stats(self):
        """Get current statistics"""
        self.update_stats()
        return self.stats
    
    def get_attacks(self):
        """Get attack history"""
        return self.attacks
    
    def add_attack(self, attack_data):
        """Add attack to history"""
        self.attacks.append({
            **attack_data,
            'timestamp': time.time()
        })
        # Keep only last 100
        if len(self.attacks) > 100:
            self.attacks = self.attacks[-100:]

class DashboardServer(object):
    """Dashboard server"""
    
    def __init__(self, ufonet, port=8888):
        self.ufonet = ufonet
        self.port = port
        self.dashboard_data = DashboardData(ufonet)
        self.server = None
        self.running = False
    
    def start(self):
        """Start dashboard server"""
        def handler_factory(*args, **kwargs):
            return DashboardHandler(*args, dashboard_data=self.dashboard_data, **kwargs)
        
        self.server = ThreadingHTTPServer(('0.0.0.0', self.port), handler_factory)
        self.running = True
        
        print(f"[Info] [AI] [Dashboard] Dashboard started on http://0.0.0.0:{self.port}")
        
        thread = threading.Thread(target=self.server.serve_forever)
        thread.daemon = True
        thread.start()
    
    def stop(self):
        """Stop dashboard server"""
        if self.server:
            self.server.shutdown()
            self.running = False
