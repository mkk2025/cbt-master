# GUI Features - Complete Guide

## Enhanced Web Interface

The CBT GUI now includes all advanced features accessible through the web interface.

## Accessing the GUI

```bash
./ufonet --gui
```

This will:
- Start web server on port 9999
- Open browser automatically
- Display main interface

## New GUI Pages

### 1. AI.INTELLIGENCE
**Access**: Click "AI.INTELLIGENCE" from main menu

**Features**:
- Target intelligence gathering
- Subdomain enumeration
- Technology stack detection
- Port scanning
- Vulnerability scanning
- DNS/WHOIS/SSL analysis
- CMS/WAF detection

**Usage**:
1. Enter target URL
2. Click "GATHER INTELLIGENCE"
3. View comprehensive report

### 2. AI.C2 - Distributed Command & Control
**Access**: Click "AI.C2" from main menu

**Features**:
- Start C2 master node
- Start analytics dashboard
- Monitor distributed attacks
- Real-time statistics

**Usage**:
1. Set port (default: 8888)
2. Click "START MASTER" or "START DASHBOARD"
3. Monitor in real-time

### 3. AI.CLOUD - Cloud Infrastructure Targeting
**Access**: Click "AI.CLOUD" from main menu

**Features**:
- AWS/Azure/GCP detection
- Cloud-specific attack vectors
- Container escape techniques
- Serverless abuse

**Usage**:
1. Enter cloud target URL
2. Click "ANALYZE CLOUD"
3. View detected provider and attack vectors

### 4. AI.DASHBOARD - Real-Time Analytics
**Access**: Click "AI.DASHBOARD" from main menu

**Features**:
- Live attack statistics
- Performance metrics
- Attack timeline
- Success rates

**Usage**:
- Automatically opens dashboard
- Updates in real-time
- Accessible at http://localhost:8888

### 5. AI.EXPLOIT - Exploit Chain Builder
**Access**: Click "AI.EXPLOIT" from main menu

**Features**:
- CVE database integration
- Vulnerability identification
- Automatic chain building
- Multi-step execution

**Usage**:
1. Enter target URL
2. Click "BUILD CHAIN"
3. View generated exploit chain

### 6. AI.REPORTS - Report Generation
**Access**: Click "AI.REPORTS" from main menu

**Features**:
- HTML/JSON/Markdown reports
- Vulnerability assessment
- Compliance checking
- Professional formatting

**Usage**:
1. Select report format
2. Click "GENERATE REPORT"
3. Download generated report

## Enhanced Attack Page

The Attack page now includes:

### New Attack Types
- MEMCACHED
- SSDP
- CHARGEN
- HTTP2RESET
- HTTP2ZEROWIN
- RUDY
- COAP

### AI Features
- AI Coordination checkbox
- AI Evasion checkbox
- Advanced Evasion Engine checkbox
- ML Optimization checkbox

### Usage
1. Enter target URL
2. Configure attack parameters
3. Enable AI features (optional)
4. Select attack types
5. Click "ATTACK!"

## Enhanced Botnet Page

### New Botnet Types Displayed
- MEMCACHEDs count
- SSDPs count
- CHARGENs count
- HTTP2s count
- RUDYs count
- COAPs count

### Shodan Integration
- Enter Shodan API key
- Select service type
- Click "SEARCH SHODAN"
- Automatically populates botnet lists

## Main Menu Enhancements

New menu items added:
- **AI.INTELLIGENCE** - Target intelligence
- **AI.C2** - Distributed C2
- **AI.CLOUD** - Cloud attacks
- **AI.DASHBOARD** - Analytics
- **AI.EXPLOIT** - Exploit chains
- **AI.REPORTS** - Report generation

## Complete Workflow Example

### 1. Gather Intelligence
- Click "AI.INTELLIGENCE"
- Enter target
- View comprehensive report

### 2. Discover Botnets
- Go to "Botnet" page
- Enter Shodan API key
- Search for vulnerable servers

### 3. Launch Attack
- Go to "Attack" page
- Enter target
- Enable AI features
- Select attack types
- Launch attack

### 4. Monitor Progress
- Click "AI.DASHBOARD"
- View real-time statistics
- Monitor success rates

### 5. Generate Report
- Click "AI.REPORTS"
- Select format
- Generate professional report

## All Features Available in GUI

✅ All 25 attack types
✅ All 14 botnet types
✅ AI coordination
✅ AI evasion
✅ Advanced evasion engine
✅ ML optimization
✅ Intelligence gathering
✅ Cloud attacks
✅ Exploit chain building
✅ Report generation
✅ C2 coordination
✅ Real-time dashboard
✅ Shodan integration

## GUI Navigation

**Main Menu** (Ring Menu):
- **Wormhole** - IRC chat
- **Botnet** - Botnet management
- **Explore** - Target exploration
- **Attack** - Launch attacks
- **Globalnet** - P2P network

**Additional Features** (Bottom menu):
- AI.INTELLIGENCE
- AI.C2
- AI.CLOUD
- AI.DASHBOARD
- AI.EXPLOIT
- AI.REPORTS

## Tips

1. **Use AI Features**: Enable AI coordination and evasion for better results
2. **Discover First**: Use Shodan to populate botnet lists before attacking
3. **Monitor**: Keep dashboard open to track attack progress
4. **Generate Reports**: Always generate reports after testing

## Status: ✅ GUI FULLY ENHANCED

All advanced features are now accessible through the web GUI!
