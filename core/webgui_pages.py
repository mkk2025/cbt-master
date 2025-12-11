#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

Additional GUI Pages for Enhanced Features
"""
import os, time

class EnhancedGUIPages(object):
    """Enhanced GUI pages for new features"""
    
    def __init__(self, pages_instance):
        self.p = pages_instance
    
    def html_intelligence(self):
        """Intelligence gathering page"""
        return self.p.pages["/header"] + """
<script>
function StartIntel(){
    target=document.getElementById("intel_target").value
    if(target.startsWith("http")){
        params="target="+escape(target)
        runCommandX("cmd_intelligence",params)
    }else{
        window.alert("You need to enter a valid url: http(s)://target.com");
    }
}
</script>
</head>
<body bgcolor="black" text="yellow" style="font-family:Courier, 'Courier New', monospace;">
<center>
<h2>AI.INTELLIGENCE - Target Intelligence Gathering</h2>
<pre>
Target Intelligence Gathering performs comprehensive OSINT and reconnaissance:
- Subdomain enumeration
- Technology stack detection
- Port scanning
- Vulnerability scanning
- DNS/WHOIS/SSL analysis
- CMS/WAF detection

Target URL: <input type="text" name="intel_target" id="intel_target" size="40" placeholder="http(s)://target.com" required>
<button onclick="StartIntel()" style="color:yellow; height:40px; width:240px; font-weight:bold; background-color:red; border: 2px solid yellow;">GATHER INTELLIGENCE</button>
</pre>
<div id="cmdOut"></div>
""" + self.p.pages["/footer"]
    
    def html_c2control(self):
        """C2 Control page"""
        return self.p.pages["/header"] + """
<script>
function StartC2Master(){
    port=document.getElementById("c2_port").value || "8888"
    params="port="+escape(port)
    runCommandX("cmd_c2_master",params)
}
function StartDashboard(){
    port=document.getElementById("dashboard_port").value || "8888"
    params="port="+escape(port)
    runCommandX("cmd_start_dashboard",params)
}
</script>
</head>
<body bgcolor="black" text="yellow" style="font-family:Courier, 'Courier New', monospace;">
<center>
<h2>AI.C2 - Distributed Command & Control</h2>
<pre>
Distributed C2 allows multi-node coordination:
- Master node: Coordinates attacks
- Slave nodes: Execute commands
- Encrypted communication (AES-256)
- Load balancing

<h3>Master Node</h3>
Port: <input type="text" name="c2_port" id="c2_port" size="5" value="8888">
<button onclick="StartC2Master()" style="color:yellow; height:40px; width:240px; font-weight:bold; background-color:red; border: 2px solid yellow;">START MASTER</button>

<h3>Analytics Dashboard</h3>
Port: <input type="text" name="dashboard_port" id="dashboard_port" size="5" value="8888">
<button onclick="StartDashboard()" style="color:yellow; height:40px; width:240px; font-weight:bold; background-color:red; border: 2px solid yellow;">START DASHBOARD</button>
</pre>
<div id="cmdOut"></div>
""" + self.p.pages["/footer"]
    
    def html_cloud(self):
        """Cloud attack page"""
        return self.p.pages["/header"] + """
<script>
function StartCloudAttack(){
    target=document.getElementById("cloud_target").value
    if(target.startsWith("http")){
        params="target="+escape(target)
        runCommandX("cmd_cloud_attack",params)
    }else{
        window.alert("You need to enter a valid url: http(s)://target.com");
    }
}
</script>
</head>
<body bgcolor="black" text="yellow" style="font-family:Courier, 'Courier New', monospace;">
<center>
<h2>AI.CLOUD - Cloud Infrastructure Targeting</h2>
<pre>
Cloud-specific attack vectors:
- AWS detection and attacks
- Azure detection and attacks
- GCP detection and attacks
- Cloudflare bypass
- Container escape
- Serverless abuse

Target URL: <input type="text" name="cloud_target" id="cloud_target" size="40" placeholder="http(s)://target.aws.com" required>
<button onclick="StartCloudAttack()" style="color:yellow; height:40px; width:240px; font-weight:bold; background-color:red; border: 2px solid yellow;">ANALYZE CLOUD</button>
</pre>
<div id="cmdOut"></div>
""" + self.p.pages["/footer"]
    
    def html_exploit(self):
        """Exploit chain builder page"""
        return self.p.pages["/header"] + """
<script>
function StartExploitChain(){
    target=document.getElementById("exploit_target").value
    if(target.startsWith("http")){
        params="target="+escape(target)
        runCommandX("cmd_exploit_chain",params)
    }else{
        window.alert("You need to enter a valid url: http(s)://target.com");
    }
}
</script>
</head>
<body bgcolor="black" text="yellow" style="font-family:Courier, 'Courier New', monospace;">
<center>
<h2>AI.EXPLOIT - Automated Exploit Chain Builder</h2>
<pre>
Automated exploit chain building:
- CVE database integration
- Vulnerability identification
- Chain building
- Multi-step execution

Target URL: <input type="text" name="exploit_target" id="exploit_target" size="40" placeholder="http(s)://target.com" required>
<button onclick="StartExploitChain()" style="color:yellow; height:40px; width:240px; font-weight:bold; background-color:red; border: 2px solid yellow;">BUILD CHAIN</button>
</pre>
<div id="cmdOut"></div>
""" + self.p.pages["/footer"]
    
    def html_reports(self):
        """Report generation page"""
        return self.p.pages["/header"] + """
<script>
function GenerateReport(){
    report_type=document.getElementById("report_type").value
    params="report_type="+escape(report_type)
    runCommandX("cmd_generate_report",params)
}
</script>
</head>
<body bgcolor="black" text="yellow" style="font-family:Courier, 'Courier New', monospace;">
<center>
<h2>AI.REPORTS - Automated Report Generation</h2>
<pre>
Generate professional penetration testing reports:
- HTML reports
- JSON reports
- Markdown reports
- Vulnerability assessment
- Compliance checking

Report Format: 
<select id="report_type">
    <option value="html">HTML</option>
    <option value="json">JSON</option>
    <option value="md">Markdown</option>
</select>
<button onclick="GenerateReport()" style="color:yellow; height:40px; width:240px; font-weight:bold; background-color:red; border: 2px solid yellow;">GENERATE REPORT</button>
</pre>
<div id="cmdOut"></div>
""" + self.p.pages["/footer"]
