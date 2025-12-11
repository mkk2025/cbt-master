#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
Modern Unified Dashboard for CBT
Integrates all features into a single modern interface
"""
import os, time

class ModernDashboard(object):
    """Modern unified dashboard with all features integrated"""
    
    def __init__(self, pages_instance):
        self.p = pages_instance
    
    def html_dashboard(self):
        """Main unified dashboard page"""
        # Get stats
        try:
            total_botnet = self.p.total_botnet
            num_zombies = self.p.num_zombies
            num_aliens = self.p.num_aliens
            num_droids = self.p.num_droids
            num_ucavs = self.p.num_ucavs
            num_rpcs = self.p.num_rpcs
            num_ntps = self.p.num_ntps
            num_dnss = self.p.num_dnss
            num_snmps = self.p.num_snmps
            try:
                num_memcacheds = str(self.p.file_len('botnet/memcacheds.txt'))
            except:
                num_memcacheds = "0"
            try:
                num_ssdps = str(self.p.file_len('botnet/ssdps.txt'))
            except:
                num_ssdps = "0"
            try:
                num_chargens = str(self.p.file_len('botnet/chargens.txt'))
            except:
                num_chargens = "0"
            try:
                num_http2s = str(self.p.file_len('botnet/http2s.txt'))
            except:
                num_http2s = "0"
            try:
                num_rudys = str(self.p.file_len('botnet/rudys.txt'))
            except:
                num_rudys = "0"
            try:
                num_coaps = str(self.p.file_len('botnet/coaps.txt'))
            except:
                num_coaps = "0"
        except:
            total_botnet = "0"
            num_zombies = num_aliens = num_droids = num_ucavs = num_rpcs = "0"
            num_ntps = num_dnss = num_snmps = "0"
            num_memcacheds = num_ssdps = num_chargens = num_http2s = num_rudys = num_coaps = "0"
        
        return self.p.pages["/header"] + """
<script>
// Ensure jQuery is loaded first
if (typeof $ === 'undefined') {
    var jqScript = document.createElement('script');
    jqScript.src = '/js/jquery-1.10.2.min.js';
    document.head.appendChild(jqScript);
    // Wait for jQuery to load
    jqScript.onload = function() {
        initializeDashboard();
    };
} else {
    initializeDashboard();
}

function initializeDashboard() {
    // Dashboard is ready
    console.log('Dashboard initialized');
}

function toggleSidebar() {
    document.querySelector('.sidebar').classList.toggle('collapsed');
    document.querySelector('.main-content').classList.toggle('expanded');
}

function loadFeature(feature) {
    var content = document.getElementById('main-content-area');
    content.innerHTML = '<div class="spinner"></div>';
    
    // Update active nav item
    document.querySelectorAll('.sidebar-nav a').forEach(a => a.classList.remove('active'));
    event.target.classList.add('active');
    
    // Load feature content via AJAX
    $.get('/dashboard/' + feature, function(data) {
        content.innerHTML = data;
    }).fail(function() {
        content.innerHTML = '<div class="alert alert-danger">Failed to load feature. Please try again.</div>';
    });
}

function startAttack() {
    var target = document.getElementById('attack_target').value;
    var path = document.getElementById('attack_path').value || '/';
    var rounds = document.getElementById('attack_rounds').value || '1';
    
    if (!target || !target.startsWith('http')) {
        alert('Please enter a valid URL starting with http:// or https://');
        return;
    }
    
    var params = 'target=' + encodeURIComponent(target) + 
                 '&path=' + encodeURIComponent(path) + 
                 '&rounds=' + encodeURIComponent(rounds);
    
    runCommandX('cmd_attack', params);
}

function gatherIntelligence() {
    var target = document.getElementById('intel_target').value;
    if (!target || !target.startsWith('http')) {
        alert('Please enter a valid URL');
        return;
    }
    runCommandX('cmd_intelligence', 'target=' + encodeURIComponent(target));
}

function startC2Master() {
    var port = document.getElementById('c2_port').value || '8888';
    runCommandX('cmd_c2_master', 'port=' + encodeURIComponent(port));
}

function startDashboard() {
    var port = document.getElementById('dashboard_port').value || '8888';
    window.open('http://127.0.0.1:' + port, '_blank');
    runCommandX('cmd_start_dashboard', 'port=' + encodeURIComponent(port));
}

function generateReport() {
    var format = document.getElementById('report_format').value;
    runCommandX('cmd_generate_report', 'report_type=' + encodeURIComponent(format));
}

// Auto-refresh stats every 5 seconds
setInterval(function() {
    if (typeof $ !== 'undefined') {
        $.get('/dashboard/stats', function(data) {
            try {
                var stats = JSON.parse(data);
                var totalEl = document.getElementById('stat-total-botnet');
                var activeEl = document.getElementById('stat-active-attacks');
                var rateEl = document.getElementById('stat-success-rate');
                if (totalEl) totalEl.textContent = stats.total_botnet || '0';
                if (activeEl) activeEl.textContent = stats.active_attacks || '0';
                if (rateEl) rateEl.textContent = stats.success_rate || '0%';
            } catch(e) {
                console.error('Failed to parse stats:', e);
            }
        }).fail(function() {
            // Silently fail - stats update is not critical
        });
    }
}, 5000);

// Ensure jQuery is loaded
if (typeof $ === 'undefined') {
    var jqScript = document.createElement('script');
    jqScript.src = '/js/jquery-1.10.2.min.js';
    jqScript.onload = function() {
        console.log('jQuery loaded');
    };
    document.head.appendChild(jqScript);
}
</script>
</head>
<body>
<div class="sidebar">
    <div class="sidebar-header">
        <img src="/cbt.jpg" alt="CBT Logo" style="width: 60px; height: 60px; border-radius: 8px; margin-bottom: 10px; object-fit: cover; border: 2px solid var(--border);">
        <h1>⚡ CBT</h1>
        <p style="color: var(--text-secondary); font-size: 12px;">Core Brim Tech</p>
    </div>
    <ul class="sidebar-nav">
        <li><a href="#" onclick="loadFeature('home'); return false;" class="active"><i>🏠</i> Dashboard</a></li>
        <li><a href="#" onclick="loadFeature('attack'); return false;"><i>⚔️</i> Attack</a></li>
        <li><a href="#" onclick="loadFeature('botnet'); return false;"><i>🤖</i> Botnet</a></li>
        <li><a href="#" onclick="loadFeature('intelligence'); return false;"><i>🔍</i> Intelligence</a></li>
        <li><a href="#" onclick="loadFeature('ai'); return false;"><i>🧠</i> AI Features</a></li>
        <li><a href="#" onclick="loadFeature('c2'); return false;"><i>🎮</i> C2 Control</a></li>
        <li><a href="#" onclick="loadFeature('cloud'); return false;"><i>☁️</i> Cloud</a></li>
        <li><a href="#" onclick="loadFeature('exploit'); return false;"><i>💣</i> Exploit Chain</a></li>
        <li><a href="#" onclick="loadFeature('reports'); return false;"><i>📊</i> Reports</a></li>
        <li><a href="/gui" target="_blank"><i>🌐</i> Legacy GUI</a></li>
    </ul>
</div>

<div class="main-content">
    <div class="top-bar">
        <div style="display: flex; align-items: center; gap: 15px;">
            <img src="/cbt.jpg" alt="CBT Logo" style="width: 50px; height: 50px; border-radius: 8px; object-fit: cover; border: 2px solid var(--border);">
            <div>
                <h2>Dashboard</h2>
                <p style="color: var(--text-secondary); margin-top: 5px;">Welcome back, Commander</p>
            </div>
        </div>
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-value" id="stat-total-botnet">""" + total_botnet + """</div>
                <div class="stat-label">Total Botnet</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="stat-active-attacks">0</div>
                <div class="stat-label">Active Attacks</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="stat-success-rate">0%</div>
                <div class="stat-label">Success Rate</div>
            </div>
        </div>
    </div>

    <div id="main-content-area">
        """ + self.dashboard_home() + """
    </div>
    
    <!-- Command Output Area (for runCommandX) -->
    <div id="cmdOut" style="position: fixed; bottom: 0; left: 0; right: 0; background: var(--bg-card); border-top: 1px solid var(--border); padding: 15px; max-height: 300px; overflow-y: auto; display: none; z-index: 1000; box-shadow: 0 -2px 10px rgba(0,0,0,0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h3 style="margin: 0; color: var(--text-primary);">Command Output</h3>
            <button onclick="document.getElementById('cmdOut').style.display='none'" class="btn btn-secondary btn-sm">Close</button>
        </div>
        <div id="cmdOutContent" style="color: var(--text-secondary); font-family: monospace; font-size: 12px; white-space: pre-wrap; word-wrap: break-word;"></div>
    </div>
</div>
<script>
// Load lib.js to get runCommandX function
(function() {
    var script = document.createElement('script');
    script.src = '/lib.js';
    script.onload = function() {
        // Override runCommandX to show output in dashboard
        if (typeof runCommandX !== 'undefined') {
            var originalRunCommandX = runCommandX;
            window.runCommandX = function(cmd, params) {
                // Show output area
                var cmdOut = document.getElementById('cmdOut');
                var cmdOutContent = document.getElementById('cmdOutContent');
                if (cmdOut && cmdOutContent) {
                    cmdOut.style.display = 'block';
                    cmdOutContent.innerHTML = '<div style="color: var(--accent-cyan);">Executing: ' + cmd + '...</div>';
                }
                // Call original function
                originalRunCommandX(cmd, params);
            };
            console.log('runCommandX loaded and overridden');
        }
    };
    document.head.appendChild(script);
})();
</script>
""" + self.p.pages["/footer"]
    
    def dashboard_home(self):
        """Home dashboard view"""
        try:
            num_memcacheds = str(self.p.file_len('botnet/memcacheds.txt'))
        except:
            num_memcacheds = "0"
        try:
            num_ssdps = str(self.p.file_len('botnet/ssdps.txt'))
        except:
            num_ssdps = "0"
        try:
            num_chargens = str(self.p.file_len('botnet/chargens.txt'))
        except:
            num_chargens = "0"
        try:
            num_http2s = str(self.p.file_len('botnet/http2s.txt'))
        except:
            num_http2s = "0"
        try:
            num_rudys = str(self.p.file_len('botnet/rudys.txt'))
        except:
            num_rudys = "0"
        try:
            num_coaps = str(self.p.file_len('botnet/coaps.txt'))
        except:
            num_coaps = "0"
        
        return """
<div class="grid grid-3">
    <div class="card">
        <div class="card-header">
            <div class="card-title">Quick Attack</div>
        </div>
        <div class="card-body">
            <div class="form-group">
                <label class="form-label">Target URL</label>
                <input type="text" id="quick_target" class="form-input" placeholder="https://target.com">
            </div>
            <button class="btn btn-primary" onclick="startQuickAttack()" style="width: 100%;">Launch Attack</button>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <div class="card-title">Botnet Status</div>
        </div>
        <div class="card-body">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div><strong>Zombies:</strong> <span class="badge badge-info">""" + self.p.num_zombies + """</span></div>
                <div><strong>Aliens:</strong> <span class="badge badge-info">""" + self.p.num_aliens + """</span></div>
                <div><strong>Droids:</strong> <span class="badge badge-info">""" + self.p.num_droids + """</span></div>
                <div><strong>UCAVs:</strong> <span class="badge badge-info">""" + self.p.num_ucavs + """</span></div>
                <div><strong>X-RPCs:</strong> <span class="badge badge-info">""" + self.p.num_rpcs + """</span></div>
                <div><strong>NTPs:</strong> <span class="badge badge-info">""" + self.p.num_ntps + """</span></div>
                <div><strong>DNSs:</strong> <span class="badge badge-info">""" + self.p.num_dnss + """</span></div>
                <div><strong>SNMPs:</strong> <span class="badge badge-info">""" + self.p.num_snmps + """</span></div>
                <div><strong>MEMCACHEDs:</strong> <span class="badge badge-info">""" + num_memcacheds + """</span></div>
                <div><strong>SSDPs:</strong> <span class="badge badge-info">""" + num_ssdps + """</span></div>
                <div><strong>CHARGENs:</strong> <span class="badge badge-info">""" + num_chargens + """</span></div>
                <div><strong>HTTP2s:</strong> <span class="badge badge-info">""" + num_http2s + """</span></div>
                <div><strong>RUDYs:</strong> <span class="badge badge-info">""" + num_rudys + """</span></div>
                <div><strong>COAPs:</strong> <span class="badge badge-info">""" + num_coaps + """</span></div>
            </div>
            <a href="#" onclick="loadFeature('botnet'); return false;" class="btn btn-secondary" style="width: 100%; margin-top: 15px;">Manage Botnets</a>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <div class="card-title">AI Features</div>
        </div>
        <div class="card-body">
            <div style="margin-bottom: 15px;">
                <label><input type="checkbox" id="ai_coord"> AI Coordination</label><br>
                <label><input type="checkbox" id="ai_evade"> AI Evasion</label><br>
                <label><input type="checkbox" id="adv_evade"> Advanced Evasion</label><br>
                <label><input type="checkbox" id="ml_opt"> ML Optimization</label>
            </div>
            <a href="#" onclick="loadFeature('ai'); return false;" class="btn btn-secondary" style="width: 100%;">Configure AI</a>
        </div>
    </div>
</div>

<div class="grid grid-2">
    <div class="card">
        <div class="card-header">
            <div class="card-title">World Map</div>
        </div>
        <div class="card-body">
            <div class="map-container" id="dashboard-map" style="height: 500px; width: 100%; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; background: var(--bg-primary); position: relative;">
                <iframe src="/cmd_view_army" style="width: 100%; height: 100%; border: none;" id="map-iframe" onload="mapLoaded()"></iframe>
                <div id="map-loading" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: var(--text-secondary);">
                    <div class="spinner"></div>
                    <p>Loading map...</p>
                </div>
            </div>
            <div style="margin-top: 15px; display: flex; gap: 10px;">
                <a href="/cmd_view_army" target="_blank" class="btn btn-secondary" style="flex: 1;">Open Full Map</a>
                <button onclick="refreshMap()" class="btn btn-primary" style="flex: 1;">Refresh Map</button>
            </div>
        </div>
    </div>
    
    <script>
    function mapLoaded() {
        var loading = document.getElementById('map-loading');
        if (loading) {
            loading.style.display = 'none';
        }
    }
    
    function refreshMap() {
        var iframe = document.getElementById('map-iframe');
        var loading = document.getElementById('map-loading');
        if (iframe) {
            if (loading) loading.style.display = 'block';
            iframe.src = iframe.src.split('?')[0] + '?t=' + new Date().getTime(); // Force reload
        }
    }
    
    // If map doesn't load in 10 seconds, show error
    setTimeout(function() {
        var loading = document.getElementById('map-loading');
        var iframe = document.getElementById('map-iframe');
        if (loading && loading.style.display !== 'none') {
            loading.innerHTML = '<p style="color: var(--accent-red);">Map failed to load. <a href="/cmd_view_army" target="_blank">Open in new window</a></p>';
        }
    }, 10000);
    </script>
    
    <div class="card">
        <div class="card-header">
            <div class="card-title">Recent Activity</div>
        </div>
        <div class="card-body">
            <div id="recent-activity">
                <p style="color: var(--text-muted);">No recent activity</p>
            </div>
        </div>
    </div>
</div>

<script>
function startQuickAttack() {
    var target = document.getElementById('quick_target').value;
    if (!target) {
        alert('Please enter a target URL');
        return;
    }
    loadFeature('attack');
    setTimeout(function() {
        document.getElementById('attack_target').value = target;
    }, 100);
}
</script>
"""
    
    def dashboard_attack(self):
        """Attack page for dashboard"""
        return """
<div class="card">
    <div class="card-header">
        <div class="card-title">Launch Attack</div>
    </div>
    <div class="card-body">
        <div class="form-group">
            <label class="form-label">Target URL</label>
            <input type="text" id="attack_target" class="form-input" placeholder="https://target.com" required>
        </div>
        <div class="form-group">
            <label class="form-label">Path</label>
            <input type="text" id="attack_path" class="form-input" placeholder="/path/to/resource" value="/">
        </div>
        <div class="form-group">
            <label class="form-label">Rounds</label>
            <input type="number" id="attack_rounds" class="form-input" value="1" min="1">
        </div>
        
        <div class="tabs" style="margin-top: 20px;">
            <button class="tab active" onclick="showAttackTab('basic')">Basic Attacks</button>
            <button class="tab" onclick="showAttackTab('advanced')">Advanced Attacks</button>
            <button class="tab" onclick="showAttackTab('amplification')">Amplification</button>
        </div>
        
        <div id="attack-tab-basic" class="tab-content">
            <div class="grid grid-4" style="margin-top: 20px;">
                <label><input type="checkbox" id="attack_loic"> LOIC</label>
                <label><input type="checkbox" id="attack_loris"> LORIS</label>
                <label><input type="checkbox" id="attack_ufosyn"> UFOSYN</label>
                <label><input type="checkbox" id="attack_xmas"> XMAS</label>
            </div>
        </div>
        
        <div id="attack-tab-advanced" class="tab-content" style="display: none;">
            <div class="grid grid-4" style="margin-top: 20px;">
                <label><input type="checkbox" id="attack_http2reset"> HTTP/2 Reset</label>
                <label><input type="checkbox" id="attack_http2zerowin"> HTTP/2 Zero Window</label>
                <label><input type="checkbox" id="attack_rudy"> RUDY</label>
                <label><input type="checkbox" id="attack_dbstress"> DB Stress</label>
            </div>
        </div>
        
        <div id="attack-tab-amplification" class="tab-content" style="display: none;">
            <div class="grid grid-4" style="margin-top: 20px;">
                <label><input type="checkbox" id="attack_memcached"> Memcached</label>
                <label><input type="checkbox" id="attack_ssdp"> SSDP</label>
                <label><input type="checkbox" id="attack_chargen"> Chargen</label>
                <label><input type="checkbox" id="attack_coap"> CoAP</label>
                <label><input type="checkbox" id="attack_ntp"> NTP</label>
                <label><input type="checkbox" id="attack_dns"> DNS</label>
                <label><input type="checkbox" id="attack_snmp"> SNMP</label>
            </div>
        </div>
        
        <div style="margin-top: 30px;">
            <button class="btn btn-danger" onclick="startAttack()" style="width: 100%; font-size: 16px; padding: 15px;">
                ⚔️ LAUNCH ATTACK
            </button>
        </div>
    </div>
</div>

<script>
function showAttackTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
    event.target.classList.add('active');
    document.getElementById('attack-tab-' + tab).style.display = 'block';
}
</script>
"""
    
    def dashboard_botnet(self):
        """Botnet management page"""
        try:
            num_memcacheds = str(self.p.file_len('botnet/memcacheds.txt'))
        except:
            num_memcacheds = "0"
        try:
            num_ssdps = str(self.p.file_len('botnet/ssdps.txt'))
        except:
            num_ssdps = "0"
        try:
            num_chargens = str(self.p.file_len('botnet/chargens.txt'))
        except:
            num_chargens = "0"
        try:
            num_http2s = str(self.p.file_len('botnet/http2s.txt'))
        except:
            num_http2s = "0"
        try:
            num_rudys = str(self.p.file_len('botnet/rudys.txt'))
        except:
            num_rudys = "0"
        try:
            num_coaps = str(self.p.file_len('botnet/coaps.txt'))
        except:
            num_coaps = "0"
        
        return """
<div class="card">
    <div class="card-header">
        <div class="card-title">Botnet Management</div>
    </div>
    <div class="card-body">
        <div class="tabs">
            <button class="tab active" onclick="showBotnetTab('list')">Botnet List</button>
            <button class="tab" onclick="showBotnetTab('discover')">Discover</button>
            <button class="tab" onclick="showBotnetTab('test')">Test</button>
        </div>
        
        <div id="botnet-tab-list" class="tab-content">
            <table class="table">
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Count</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Zombies</td><td>""" + self.p.num_zombies + """</td><td><span class="badge badge-success">Active</span></td><td><a href='javascript:runCommandX("cmd_list_zombies")' class="btn btn-secondary btn-sm">View</a></td></tr>
                    <tr><td>Aliens</td><td>""" + self.p.num_aliens + """</td><td><span class="badge badge-success">Active</span></td><td><a href='javascript:runCommandX("cmd_list_aliens")' class="btn btn-secondary btn-sm">View</a></td></tr>
                    <tr><td>Droids</td><td>""" + self.p.num_droids + """</td><td><span class="badge badge-success">Active</span></td><td><a href='javascript:runCommandX("cmd_list_droids")' class="btn btn-secondary btn-sm">View</a></td></tr>
                    <tr><td>UCAVs</td><td>""" + self.p.num_ucavs + """</td><td><span class="badge badge-success">Active</span></td><td><a href='javascript:runCommandX("cmd_list_ucavs")' class="btn btn-secondary btn-sm">View</a></td></tr>
                    <tr><td>X-RPCs</td><td>""" + self.p.num_rpcs + """</td><td><span class="badge badge-success">Active</span></td><td><a href='javascript:runCommandX("cmd_list_rpcs")' class="btn btn-secondary btn-sm">View</a></td></tr>
                    <tr><td>NTPs</td><td>""" + self.p.num_ntps + """</td><td><span class="badge badge-success">Active</span></td><td><a href='javascript:runCommandX("cmd_list_ntps")' class="btn btn-secondary btn-sm">View</a></td></tr>
                    <tr><td>DNSs</td><td>""" + self.p.num_dnss + """</td><td><span class="badge badge-success">Active</span></td><td><a href='javascript:runCommandX("cmd_list_dnss")' class="btn btn-secondary btn-sm">View</a></td></tr>
                    <tr><td>SNMPs</td><td>""" + self.p.num_snmps + """</td><td><span class="badge badge-success">Active</span></td><td><a href='javascript:runCommandX("cmd_list_snmps")' class="btn btn-secondary btn-sm">View</a></td></tr>
                </tbody>
            </table>
        </div>
        
        <div id="botnet-tab-discover" class="tab-content" style="display: none;">
            <div class="form-group">
                <label class="form-label">Shodan API Key</label>
                <input type="text" id="shodan_key" class="form-input" placeholder="Your Shodan API Key">
            </div>
            <div class="form-group">
                <label class="form-label">Service Type</label>
                <select id="service_type" class="form-input">
                    <option value="memcached">Memcached</option>
                    <option value="ssdp">SSDP</option>
                    <option value="ntp">NTP</option>
                    <option value="dns">DNS</option>
                    <option value="snmp">SNMP</option>
                    <option value="coap">CoAP</option>
                </select>
            </div>
            <button class="btn btn-primary" onclick="searchShodan()" style="width: 100%;">Search Shodan</button>
        </div>
        
        <div id="botnet-tab-test" class="tab-content" style="display: none;">
            <div class="grid grid-3">
                <button class="btn btn-secondary" onclick='runCommandX("cmd_test_offline")'>Test Offline</button>
                <button class="btn btn-secondary" onclick='runCommandX("cmd_test_all")'>Test All</button>
                <button class="btn btn-secondary" onclick='runCommandX("cmd_test_army")'>Test Zombies</button>
            </div>
        </div>
    </div>
</div>

<script>
function showBotnetTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
    event.target.classList.add('active');
    document.getElementById('botnet-tab-' + tab).style.display = 'block';
}

function searchShodan() {
    var key = document.getElementById('shodan_key').value;
    var service = document.getElementById('service_type').value;
    if (!key) {
        alert('Please enter Shodan API key');
        return;
    }
    runCommandX('cmd_shodan_search', 'shodan_key=' + encodeURIComponent(key) + '&service_type=' + encodeURIComponent(service));
}
</script>
"""
    
    def dashboard_intelligence(self):
        """Intelligence gathering page"""
        return """
<div class="card">
    <div class="card-header">
        <div class="card-title">Target Intelligence Gathering</div>
    </div>
    <div class="card-body">
        <div class="alert alert-info">
            <strong>OSINT & Reconnaissance:</strong> Subdomain enumeration, tech stack detection, port scanning, vulnerability scanning, DNS/WHOIS/SSL analysis, CMS/WAF detection
        </div>
        
        <div class="form-group">
            <label class="form-label">Target URL</label>
            <input type="text" id="intel_target" class="form-input" placeholder="https://target.com" required>
        </div>
        
        <button class="btn btn-primary" onclick="gatherIntelligence()" style="width: 100%; padding: 15px; font-size: 16px;">
            🔍 Gather Intelligence
        </button>
        
        <div id="intel-results" style="margin-top: 30px;"></div>
    </div>
</div>
"""
    
    def dashboard_ai(self):
        """AI features page"""
        return """
<div class="grid grid-2">
    <div class="card">
        <div class="card-header">
            <div class="card-title">AI Coordination</div>
        </div>
        <div class="card-body">
            <p>Intelligent attack planning and coordination</p>
            <ul style="color: var(--text-secondary); margin: 15px 0; padding-left: 20px;">
                <li>Target analysis</li>
                <li>Adaptive strategy selection</li>
                <li>Success rate optimization</li>
            </ul>
            <label><input type="checkbox" id="enable_ai_coord"> Enable AI Coordination</label>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <div class="card-title">AI Evasion</div>
        </div>
        <div class="card-body">
            <p>WAF bypass and evasion techniques</p>
            <ul style="color: var(--text-secondary); margin: 15px 0; padding-left: 20px;">
                <li>URL obfuscation</li>
                <li>Header randomization</li>
                <li>Request fragmentation</li>
            </ul>
            <label><input type="checkbox" id="enable_ai_evade"> Enable AI Evasion</label>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <div class="card-title">Advanced Evasion Engine</div>
        </div>
        <div class="card-body">
            <p>Sophisticated WAF response analysis</p>
            <ul style="color: var(--text-secondary); margin: 15px 0; padding-left: 20px;">
                <li>Behavioral analysis</li>
                <li>Dynamic payload generation</li>
                <li>Protocol-level obfuscation</li>
            </ul>
            <label><input type="checkbox" id="enable_adv_evade"> Enable Advanced Evasion</label>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <div class="card-title">ML Optimization</div>
        </div>
        <div class="card-body">
            <p>Machine learning-based attack optimization</p>
            <ul style="color: var(--text-secondary); margin: 15px 0; padding-left: 20px;">
                <li>Success prediction</li>
                <li>Feature extraction</li>
                <li>Reinforcement learning</li>
            </ul>
            <label><input type="checkbox" id="enable_ml_opt"> Enable ML Optimization</label>
        </div>
    </div>
</div>
"""
    
    def dashboard_c2(self):
        """C2 control page"""
        return """
<div class="grid grid-2">
    <div class="card">
        <div class="card-header">
            <div class="card-title">C2 Master Node</div>
        </div>
        <div class="card-body">
            <p style="color: var(--text-secondary); margin-bottom: 20px;">
                Coordinate distributed attacks across multiple nodes
            </p>
            <div class="form-group">
                <label class="form-label">Port</label>
                <input type="number" id="c2_port" class="form-input" value="8888">
            </div>
            <button class="btn btn-primary" onclick="startC2Master()" style="width: 100%;">Start Master Node</button>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <div class="card-title">Analytics Dashboard</div>
        </div>
        <div class="card-body">
            <p style="color: var(--text-secondary); margin-bottom: 20px;">
                Real-time analytics and monitoring
            </p>
            <div class="form-group">
                <label class="form-label">Port</label>
                <input type="number" id="dashboard_port" class="form-input" value="8888">
            </div>
            <button class="btn btn-success" onclick="startDashboard()" style="width: 100%;">Start Dashboard</button>
        </div>
    </div>
</div>
"""
    
    def dashboard_cloud(self):
        """Cloud attack page"""
        return """
<div class="card">
    <div class="card-header">
        <div class="card-title">Cloud Infrastructure Targeting</div>
    </div>
    <div class="card-body">
        <div class="alert alert-info">
            <strong>Cloud-Specific Attacks:</strong> AWS, Azure, GCP detection and attacks, Cloudflare bypass, container escape, serverless abuse
        </div>
        
        <div class="form-group">
            <label class="form-label">Target URL</label>
            <input type="text" id="cloud_target" class="form-input" placeholder="https://target.aws.com" required>
        </div>
        
        <button class="btn btn-primary" onclick="startCloudAttack()" style="width: 100%; padding: 15px; font-size: 16px;">
            ☁️ Analyze Cloud Infrastructure
        </button>
        
        <div id="cloud-results" style="margin-top: 30px;"></div>
    </div>
</div>

<script>
function startCloudAttack() {
    var target = document.getElementById('cloud_target').value;
    if (!target || !target.startsWith('http')) {
        alert('Please enter a valid URL');
        return;
    }
    runCommandX('cmd_cloud_attack', 'target=' + encodeURIComponent(target));
}
</script>
"""
    
    def dashboard_exploit(self):
        """Exploit chain builder page"""
        return """
<div class="card">
    <div class="card-header">
        <div class="card-title">Automated Exploit Chain Builder</div>
    </div>
    <div class="card-body">
        <div class="alert alert-info">
            <strong>Features:</strong> CVE database integration, vulnerability identification, chain building, multi-step execution
        </div>
        
        <div class="form-group">
            <label class="form-label">Target URL</label>
            <input type="text" id="exploit_target" class="form-input" placeholder="https://target.com" required>
        </div>
        
        <button class="btn btn-danger" onclick="buildExploitChain()" style="width: 100%; padding: 15px; font-size: 16px;">
            💣 Build Exploit Chain
        </button>
        
        <div id="exploit-results" style="margin-top: 30px;"></div>
    </div>
</div>

<script>
function buildExploitChain() {
    var target = document.getElementById('exploit_target').value;
    if (!target || !target.startsWith('http')) {
        alert('Please enter a valid URL');
        return;
    }
    runCommandX('cmd_exploit_chain', 'target=' + encodeURIComponent(target));
}
</script>
"""
    
    def dashboard_reports(self):
        """Report generation page"""
        return """
<div class="card">
    <div class="card-header">
        <div class="card-title">Report Generation</div>
    </div>
    <div class="card-body">
        <div class="form-group">
            <label class="form-label">Report Format</label>
            <select id="report_format" class="form-input">
                <option value="html">HTML Report</option>
                <option value="json">JSON Report</option>
                <option value="md">Markdown Report</option>
            </select>
        </div>
        
        <button class="btn btn-primary" onclick="generateReport()" style="width: 100%; padding: 15px; font-size: 16px;">
            📊 Generate Report
        </button>
        
        <div class="alert alert-info" style="margin-top: 20px;">
            Reports include: Vulnerability assessment, attack statistics, recommendations, compliance checking
        </div>
    </div>
</div>
"""
