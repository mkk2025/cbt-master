#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

Target Intelligence Gathering - OSINT and Reconnaissance
"""
import socket, ssl, re, json, time, random
import urllib.request, urllib.error, urllib.parse
from urllib.parse import urlparse
import dns.resolver
import subprocess

class IntelligenceGatherer(object):
    """Comprehensive target intelligence gathering"""
    
    def __init__(self, ufonet):
        self.ufonet = ufonet
        self.intel_data = {}
        
    def gather_all(self, target):
        """Gather all available intelligence"""
        print(f"[Info] [AI] [Intel] Gathering intelligence on {target}...\n")
        
        intel = {
            'target': target,
            'timestamp': time.time(),
            'subdomains': self.enumerate_subdomains(target),
            'tech_stack': self.detect_tech_stack(target),
            'ports': self.scan_ports(target),
            'vulnerabilities': self.scan_vulnerabilities(target),
            'dns_info': self.gather_dns_info(target),
            'whois_info': self.gather_whois(target),
            'ssl_info': self.analyze_ssl(target),
            'headers': self.analyze_headers(target),
            'cms': self.detect_cms(target),
            'waf': self.detect_waf(target)
        }
        
        self.intel_data[target] = intel
        return intel
    
    def enumerate_subdomains(self, domain):
        """Subdomain enumeration"""
        print("[Info] [AI] [Intel] Enumerating subdomains...")
        subdomains = []
        
        # Common subdomain wordlist
        wordlist = ['www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk', 
                   'admin', 'blog', 'dev', 'test', 'staging', 'api', 'cdn', 'static', 'media',
                   'secure', 'vpn', 'remote', 'portal', 'cpanel', 'whm', 'autodiscover']
        
        try:
            parsed = urlparse(domain if '://' in domain else f'http://{domain}')
            base_domain = parsed.netloc or parsed.path.split('/')[0]
            base_domain = base_domain.split(':')[0]  # Remove port
            
            for word in wordlist:
                subdomain = f"{word}.{base_domain}"
                try:
                    socket.gethostbyname(subdomain)
                    subdomains.append(subdomain)
                    print(f"  [+] Found: {subdomain}")
                except:
                    pass
        except Exception as e:
            print(f"[Error] [AI] [Intel] Subdomain enumeration failed: {e}")
        
        return subdomains
    
    def detect_tech_stack(self, target):
        """Detect technology stack"""
        print("[Info] [AI] [Intel] Detecting technology stack...")
        tech = {
            'server': None,
            'framework': None,
            'cms': None,
            'language': None,
            'cdn': None
        }
        
        try:
            if not target.startswith('http'):
                target = f'http://{target}'
            
            req = urllib.request.Request(target)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                headers = dict(response.headers)
                html = response.read().decode('utf-8', errors='ignore')
                
                # Server detection
                if 'Server' in headers:
                    tech['server'] = headers['Server']
                
                # Framework detection
                if 'X-Powered-By' in headers:
                    tech['framework'] = headers['X-Powered-By']
                
                # CMS detection
                if 'wp-content' in html or 'wp-includes' in html:
                    tech['cms'] = 'WordPress'
                elif 'Joomla' in html:
                    tech['cms'] = 'Joomla'
                elif 'Drupal' in html:
                    tech['cms'] = 'Drupal'
                
                # CDN detection
                cdn_headers = ['cf-ray', 'x-amz-cf-id', 'x-served-by', 'x-cache']
                for header in cdn_headers:
                    if header in headers:
                        tech['cdn'] = headers[header]
                        break
                
                print(f"  [+] Server: {tech['server']}")
                print(f"  [+] Framework: {tech['framework']}")
                print(f"  [+] CMS: {tech['cms']}")
                print(f"  [+] CDN: {tech['cdn']}")
        except Exception as e:
            print(f"[Error] [AI] [Intel] Tech stack detection failed: {e}")
        
        return tech
    
    def scan_ports(self, target):
        """Port scanning"""
        print("[Info] [AI] [Intel] Scanning ports...")
        ports = []
        common_ports = [80, 443, 8080, 8443, 22, 21, 25, 53, 3306, 5432, 6379, 27017]
        
        try:
            parsed = urlparse(target if '://' in target else f'http://{target}')
            host = parsed.netloc or parsed.path.split('/')[0]
            host = host.split(':')[0]
            
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((host, port))
                    if result == 0:
                        ports.append(port)
                        print(f"  [+] Port {port} open")
                    sock.close()
                except:
                    pass
        except Exception as e:
            print(f"[Error] [AI] [Intel] Port scanning failed: {e}")
        
        return ports
    
    def scan_vulnerabilities(self, target):
        """Vulnerability scanning"""
        print("[Info] [AI] [Intel] Scanning for vulnerabilities...")
        vulns = []
        
        # Check for common vulnerabilities
        common_paths = [
            '/.git/config',
            '/.env',
            '/phpinfo.php',
            '/admin',
            '/wp-admin',
            '/.well-known/security.txt'
        ]
        
        try:
            if not target.startswith('http'):
                target = f'http://{target}'
            
            for path in common_paths:
                try:
                    url = f"{target.rstrip('/')}{path}"
                    req = urllib.request.Request(url)
                    req.add_header('User-Agent', 'Mozilla/5.0')
                    
                    with urllib.request.urlopen(req, timeout=5) as response:
                        if response.status == 200:
                            vulns.append({
                                'path': path,
                                'status': response.status,
                                'severity': 'medium'
                            })
                            print(f"  [!] Found: {path}")
                except:
                    pass
        except Exception as e:
            print(f"[Error] [AI] [Intel] Vulnerability scanning failed: {e}")
        
        return vulns
    
    def gather_dns_info(self, target):
        """Gather DNS information"""
        print("[Info] [AI] [Intel] Gathering DNS information...")
        dns_info = {}
        
        try:
            parsed = urlparse(target if '://' in target else f'http://{target}')
            domain = parsed.netloc or parsed.path.split('/')[0]
            domain = domain.split(':')[0]
            
            resolver = dns.resolver.Resolver()
            resolver.nameservers = ['8.8.8.8', '8.8.4.4']
            
            # A records
            try:
                a_records = resolver.resolve(domain, 'A')
                dns_info['A'] = [str(r) for r in a_records]
            except:
                pass
            
            # MX records
            try:
                mx_records = resolver.resolve(domain, 'MX')
                dns_info['MX'] = [str(r) for r in mx_records]
            except:
                pass
            
            # TXT records
            try:
                txt_records = resolver.resolve(domain, 'TXT')
                dns_info['TXT'] = [str(r) for r in txt_records]
            except:
                pass
            
            print(f"  [+] A Records: {dns_info.get('A', [])}")
        except Exception as e:
            print(f"[Error] [AI] [Intel] DNS gathering failed: {e}")
        
        return dns_info
    
    def gather_whois(self, target):
        """Gather WHOIS information"""
        print("[Info] [AI] [Intel] Gathering WHOIS information...")
        try:
            import whois
            parsed = urlparse(target if '://' in target else f'http://{target}')
            domain = parsed.netloc or parsed.path.split('/')[0]
            domain = domain.split(':')[0]
            
            w = whois.whois(domain)
            return {
                'registrar': w.registrar,
                'creation_date': str(w.creation_date) if w.creation_date else None,
                'expiration_date': str(w.expiration_date) if w.expiration_date else None
            }
        except Exception as e:
            print(f"[Error] [AI] [Intel] WHOIS gathering failed: {e}")
            return {}
    
    def analyze_ssl(self, target):
        """Analyze SSL/TLS configuration"""
        print("[Info] [AI] [Intel] Analyzing SSL/TLS...")
        ssl_info = {}
        
        try:
            parsed = urlparse(target if '://' in target else f'https://{target}')
            hostname = parsed.netloc or parsed.path.split('/')[0]
            hostname = hostname.split(':')[0]
            port = parsed.port or 443
            
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    ssl_info['subject'] = dict(x[0] for x in cert['subject'])
                    ssl_info['issuer'] = dict(x[0] for x in cert['issuer'])
                    ssl_info['version'] = cert.get('version')
                    ssl_info['serialNumber'] = cert.get('serialNumber')
        except Exception as e:
            print(f"[Error] [AI] [Intel] SSL analysis failed: {e}")
        
        return ssl_info
    
    def analyze_headers(self, target):
        """Analyze HTTP headers"""
        print("[Info] [AI] [Intel] Analyzing HTTP headers...")
        try:
            if not target.startswith('http'):
                target = f'http://{target}'
            
            req = urllib.request.Request(target)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                return dict(response.headers)
        except Exception as e:
            print(f"[Error] [AI] [Intel] Header analysis failed: {e}")
            return {}
    
    def detect_cms(self, target):
        """Detect CMS and version"""
        print("[Info] [AI] [Intel] Detecting CMS...")
        try:
            if not target.startswith('http'):
                target = f'http://{target}'
            
            req = urllib.request.Request(target)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
                # WordPress
                if 'wp-content' in html:
                    version_match = re.search(r'wp-includes/js/wp-embed\.min\.js\?ver=([0-9.]+)', html)
                    return {'cms': 'WordPress', 'version': version_match.group(1) if version_match else 'Unknown'}
                
                # Joomla
                if 'joomla' in html.lower():
                    return {'cms': 'Joomla', 'version': 'Unknown'}
                
                # Drupal
                if 'drupal' in html.lower():
                    return {'cms': 'Drupal', 'version': 'Unknown'}
        except Exception as e:
            print(f"[Error] [AI] [Intel] CMS detection failed: {e}")
        
        return {'cms': None, 'version': None}
    
    def detect_waf(self, target):
        """Detect WAF"""
        print("[Info] [AI] [Intel] Detecting WAF...")
        try:
            if not target.startswith('http'):
                target = f'http://{target}'
            
            req = urllib.request.Request(target)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                headers = dict(response.headers)
                
                waf_indicators = {
                    'cloudflare': ['cf-ray', 'cloudflare'],
                    'akamai': ['akamai'],
                    'incapsula': ['incapsula'],
                    'sucuri': ['sucuri'],
                    'aws_waf': ['x-amzn-requestid']
                }
                
                for waf, indicators in waf_indicators.items():
                    for indicator in indicators:
                        if indicator.lower() in str(headers).lower():
                            print(f"  [+] WAF Detected: {waf}")
                            return waf
        except Exception as e:
            print(f"[Error] [AI] [Intel] WAF detection failed: {e}")
        
        return None
    
    def generate_report(self, target):
        """Generate intelligence report"""
        intel = self.intel_data.get(target, {})
        if not intel:
            intel = self.gather_all(target)
        
        report = f"""
=== Intelligence Report for {target} ===
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

[Subdomains]
{chr(10).join(intel.get('subdomains', []))}

[Technology Stack]
Server: {intel.get('tech_stack', {}).get('server', 'Unknown')}
Framework: {intel.get('tech_stack', {}).get('framework', 'Unknown')}
CMS: {intel.get('tech_stack', {}).get('cms', 'Unknown')}
CDN: {intel.get('tech_stack', {}).get('cdn', 'Unknown')}

[Open Ports]
{', '.join(map(str, intel.get('ports', [])))}

[Vulnerabilities]
{chr(10).join([f"- {v['path']} (Status: {v['status']})" for v in intel.get('vulnerabilities', [])])}

[WAF]
{intel.get('waf', 'Not detected')}

[CMS Detection]
{intel.get('cms', {}).get('cms', 'Unknown')} {intel.get('cms', {}).get('version', '')}
"""
        return report
