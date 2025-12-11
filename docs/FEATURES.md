# CBT Enhanced Features Guide

## New Features Added

### 1. Comprehensive Requirements Management
- **File**: `requirements.txt`
- Complete dependency list with versions
- Includes optional AI/ML libraries
- Easy installation: `pip3 install -r requirements.txt`

### 2. Automated Vulnerability Scanner
- **Module**: `core/tools/scanner.py`
- Scans IP ranges for vulnerable services
- Supports: Memcached, SSDP, Chargen, NTP, DNS, SNMP, CoAP
- Automatically saves results to botnet files

**Usage:**
```bash
./ufonet --scan-all 192.168.1.0-192.168.1.255
./ufonet --scan-memcached 10.0.0.0-10.0.0.255
```

### 3. AI-Powered Attack Coordinator
- **Module**: `core/ai/coordinator.py`
- Intelligent attack strategy selection
- Multi-phase attack planning
- Success rate learning
- Adaptive attack patterns

**Usage:**
```bash
./ufonet -a http://target.com --ai-coordinate
```

### 4. AI-Powered Evasion System
- **Module**: `core/ai/evasion.py`
- WAF bypass techniques
- Header randomization
- URL obfuscation
- Adaptive timing
- Protocol mixing

**Usage:**
```bash
./ufonet -a http://target.com --ai-evade
```

### 5. AI Target Analysis
- Analyzes target characteristics
- Recommends optimal attacks
- Estimates success probability
- Suggests attack parameters

**Usage:**
```bash
./ufonet --ai-analyze http://target.com
```

## Enhanced Botnet Types

### New Botnet Types Added:
1. **MEMCACHEDs** - Memcached amplification reflectors
2. **SSDPs** - SSDP amplification devices
3. **CHARGENs** - Chargen amplification services
4. **HTTP2s** - HTTP/2 vulnerable servers
5. **RUDYs** - RUDY vulnerable servers
6. **COAPs** - CoAP amplification devices

### New Attack Modules:
1. **MEMCACHED** - Memcached amplification
2. **SSDP** - SSDP amplification
3. **CHARGEN** - Chargen amplification
4. **HTTP2RESET** - HTTP/2 Rapid Reset
5. **HTTP2ZEROWIN** - HTTP/2 Zero Window
6. **RUDY** - R U Dead Yet (slow POST)
7. **COAP** - CoAP amplification

## How Vulnerable Systems Interact

### Open Redirect Exploitation
- CBT finds servers with Open Redirect vulnerabilities
- Uses them to redirect traffic to target
- Target sees requests from vulnerable server IPs

### Amplification Attacks
- Small requests to vulnerable reflectors
- Reflectors send large responses to target
- Amplification factors: 10x to 50,000x

### Protocol-Specific Exploits
- HTTP/2 Rapid Reset (CVE-2023-44487)
- XML-RPC Pingback loops
- Slow connection attacks (RUDY, LORIS)

## AI Integration Benefits

1. **Intelligent Selection**: AI chooses best attacks based on target
2. **Adaptive Learning**: Learns from attack results
3. **Evasion**: Automatically bypasses security measures
4. **Optimization**: Optimizes attack parameters in real-time

## Complete Feature List

### Attack Capabilities (25 total)
- 18 Original attacks
- 7 New attacks (Memcached, SSDP, Chargen, HTTP2Reset, HTTP2ZeroWin, RUDY, CoAP)

### Botnet Types (14 total)
- 8 Original types
- 6 New types

### Tools
- Scanner (automated discovery)
- AI Coordinator (intelligent planning)
- AI Evasion (WAF bypass)
- Abductor (target analysis)
- Inspector (crawling)
- XRAY (port scanning)

## Installation

```bash
# Install all dependencies
pip3 install -r requirements.txt

# Or use setup script
python3 setup.py
```

## Configuration

AI features can be configured:
- Learning rate
- Evasion aggressiveness
- History size
- Adaptation rate

See `docs/AI_INTEGRATION.md` for details.
