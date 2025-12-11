#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

You should have received a copy of the GNU General Public License along
with CBT; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import socket, sys, threading, time, random
import requests
from urllib.parse import urlparse

# CBT Automated Scanner for Vulnerable Servers/Reflectors
class AutoScanner(object):
    def __init__(self, ufonet):
        self.ufonet = ufonet
        self.results = {
            'memcacheds': [],
            'ssdps': [],
            'chargens': [],
            'ntps': [],
            'dnss': [],
            'snmps': [],
            'coaps': []
        }
        
    def scan_memcached(self, ip, port=11211):
        """Scan for vulnerable Memcached servers"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            # Send stats command
            sock.sendto(b'stats\r\n', (ip, port))
            data, addr = sock.recvfrom(1024)
            if b'STAT' in data or b'END' in data:
                return True
        except:
            pass
        return False
    
    def scan_ssdp(self, ip, port=1900):
        """Scan for SSDP devices"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            payload = b'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nST: ssdp:all\r\nMX: 2\r\n\r\n'
            sock.sendto(payload, (ip, port))
            data, addr = sock.recvfrom(1024)
            if b'HTTP' in data or b'SSDP' in data:
                return True
        except:
            pass
        return False
    
    def scan_chargen(self, ip, port=19):
        """Scan for Chargen services"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            sock.sendto(b'\x00', (ip, port))
            data, addr = sock.recvfrom(1024)
            if len(data) > 0:
                return True
        except:
            pass
        return False
    
    def scan_ntp(self, ip, port=123):
        """Scan for NTP servers with monlist enabled"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            # NTP monlist request
            payload = b'\x17\x00\x03\x2a' + b'\x00' * 4
            sock.sendto(payload, (ip, port))
            data, addr = sock.recvfrom(1024)
            if len(data) > 48:  # Monlist response is larger
                return True
        except:
            pass
        return False
    
    def scan_dns(self, ip, port=53):
        """Scan for open DNS resolvers"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            # DNS query for amplification test
            query = b'\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01'
            sock.sendto(query, (ip, port))
            data, addr = sock.recvfrom(1024)
            if len(data) > len(query):
                return True
        except:
            pass
        return False
    
    def scan_snmp(self, ip, port=161):
        """Scan for SNMP services"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            # SNMP GET request
            payload = b'\x30\x26\x02\x01\x00\x04\x06public\xa0\x19\x02\x04\x00\x00\x00\x00\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00'
            sock.sendto(payload, (ip, port))
            data, addr = sock.recvfrom(1024)
            if b'\x30' in data:  # SNMP response
                return True
        except:
            pass
        return False
    
    def scan_coap(self, ip, port=5683):
        """Scan for CoAP devices"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2)
            # CoAP GET request
            payload = b'\x40\x01\x00\x00\x2e\x77\x65\x6c\x6c\x2d\x6b\x6e\x6f\x77\x6e\x04\x63\x6f\x72\x65'
            sock.sendto(payload, (ip, port))
            data, addr = sock.recvfrom(1024)
            if len(data) > 0:
                return True
        except:
            pass
        return False
    
    def scan_ip_range(self, start_ip, end_ip, scan_type='all'):
        """Scan IP range for vulnerable services"""
        print(f"[Info] [AI] [Scanner] Starting scan: {start_ip} to {end_ip}")
        start = self.ip_to_int(start_ip)
        end = self.ip_to_int(end_ip)
        
        for ip_int in range(start, end + 1):
            ip = self.int_to_ip(ip_int)
            if scan_type == 'all' or scan_type == 'memcached':
                if self.scan_memcached(ip):
                    self.results['memcacheds'].append(ip)
                    print(f"[Info] [AI] [Scanner] Found Memcached: {ip}")
            if scan_type == 'all' or scan_type == 'ssdp':
                if self.scan_ssdp(ip):
                    self.results['ssdps'].append(ip)
                    print(f"[Info] [AI] [Scanner] Found SSDP: {ip}")
            if scan_type == 'all' or scan_type == 'chargen':
                if self.scan_chargen(ip):
                    self.results['chargens'].append(ip)
                    print(f"[Info] [AI] [Scanner] Found Chargen: {ip}")
            if scan_type == 'all' or scan_type == 'ntp':
                if self.scan_ntp(ip):
                    self.results['ntps'].append(ip)
                    print(f"[Info] [AI] [Scanner] Found NTP: {ip}")
            if scan_type == 'all' or scan_type == 'dns':
                if self.scan_dns(ip):
                    self.results['dnss'].append(ip)
                    print(f"[Info] [AI] [Scanner] Found DNS: {ip}")
            if scan_type == 'all' or scan_type == 'snmp':
                if self.scan_snmp(ip):
                    self.results['snmps'].append(ip)
                    print(f"[Info] [AI] [Scanner] Found SNMP: {ip}")
            if scan_type == 'all' or scan_type == 'coap':
                if self.scan_coap(ip):
                    self.results['coaps'].append(ip)
                    print(f"[Info] [AI] [Scanner] Found CoAP: {ip}")
            time.sleep(0.1)  # Rate limiting
        
        return self.results
    
    def ip_to_int(self, ip):
        """Convert IP to integer"""
        return sum(int(octet) * (256 ** (3 - i)) for i, octet in enumerate(ip.split('.')))
    
    def int_to_ip(self, ip_int):
        """Convert integer to IP"""
        return '.'.join(str((ip_int >> (8 * (3 - i))) & 0xFF) for i in range(4))
    
    def save_results(self):
        """Save scan results to botnet files"""
        for botnet_type, ips in self.results.items():
            if ips:
                filename = f"botnet/{botnet_type}.txt"
                with open(filename, 'a') as f:
                    for ip in ips:
                        f.write(f"{ip}\n")
                print(f"[Info] [AI] [Scanner] Saved {len(ips)} {botnet_type} to {filename}")
