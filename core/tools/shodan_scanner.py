#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

Shodan/Censys Integration for Real Vulnerable Server Discovery
"""
import sys, os, json
try:
    import shodan
    SHODAN_AVAILABLE = True
except:
    SHODAN_AVAILABLE = False
    print("[Warning] Shodan library not installed. Install with: pip3 install shodan")

try:
    from censys.search import CensysHosts
    CENSYS_AVAILABLE = True
except:
    CENSYS_AVAILABLE = False
    print("[Warning] Censys library not installed. Install with: pip3 install censys")

class ShodanScanner(object):
    """Shodan API integration for finding vulnerable servers"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('SHODAN_API_KEY')
        if not self.api_key and SHODAN_AVAILABLE:
            print("[Warning] Shodan API key not found. Set SHODAN_API_KEY environment variable or use --shodan-key")
        self.api = None
        if SHODAN_AVAILABLE and self.api_key:
            try:
                self.api = shodan.Shodan(self.api_key)
            except:
                pass
    
    def search_memcached(self, limit=100):
        """Search for exposed Memcached servers"""
        if not self.api:
            return []
        results = []
        try:
            query = 'product:"Memcached" port:11211'
            print(f"[Info] [AI] [Shodan] Searching for Memcached servers...")
            for result in self.api.search_cursor(query):
                if len(results) >= limit:
                    break
                ip = result.get('ip_str', '')
                if ip:
                    results.append(ip)
                    print(f"[Info] [AI] [Shodan] Found Memcached: {ip}")
        except Exception as e:
            print(f"[Error] [AI] [Shodan] Search failed: {e}")
        return results
    
    def search_ssdp(self, limit=100):
        """Search for SSDP devices"""
        if not self.api:
            return []
        results = []
        try:
            query = 'port:1900 "M-SEARCH"'
            print(f"[Info] [AI] [Shodan] Searching for SSDP devices...")
            for result in self.api.search_cursor(query):
                if len(results) >= limit:
                    break
                ip = result.get('ip_str', '')
                if ip:
                    results.append(ip)
                    print(f"[Info] [AI] [Shodan] Found SSDP: {ip}")
        except Exception as e:
            print(f"[Error] [AI] [Shodan] Search failed: {e}")
        return results
    
    def search_ntp(self, limit=100):
        """Search for NTP servers with monlist"""
        if not self.api:
            return []
        results = []
        try:
            query = 'product:"NTP" port:123'
            print(f"[Info] [AI] [Shodan] Searching for NTP servers...")
            for result in self.api.search_cursor(query):
                if len(results) >= limit:
                    break
                ip = result.get('ip_str', '')
                if ip:
                    results.append(ip)
                    print(f"[Info] [AI] [Shodan] Found NTP: {ip}")
        except Exception as e:
            print(f"[Error] [AI] [Shodan] Search failed: {e}")
        return results
    
    def search_dns(self, limit=100):
        """Search for open DNS resolvers"""
        if not self.api:
            return []
        results = []
        try:
            query = 'product:"DNS" port:53'
            print(f"[Info] [AI] [Shodan] Searching for DNS resolvers...")
            for result in self.api.search_cursor(query):
                if len(results) >= limit:
                    break
                ip = result.get('ip_str', '')
                if ip:
                    results.append(ip)
                    print(f"[Info] [AI] [Shodan] Found DNS: {ip}")
        except Exception as e:
            print(f"[Error] [AI] [Shodan] Search failed: {e}")
        return results
    
    def search_snmp(self, limit=100):
        """Search for SNMP services"""
        if not self.api:
            return []
        results = []
        try:
            query = 'product:"SNMP" port:161'
            print(f"[Info] [AI] [Shodan] Searching for SNMP services...")
            for result in self.api.search_cursor(query):
                if len(results) >= limit:
                    break
                ip = result.get('ip_str', '')
                if ip:
                    results.append(ip)
                    print(f"[Info] [AI] [Shodan] Found SNMP: {ip}")
        except Exception as e:
            print(f"[Error] [AI] [Shodan] Search failed: {e}")
        return results
    
    def search_coap(self, limit=100):
        """Search for CoAP devices"""
        if not self.api:
            return []
        results = []
        try:
            query = 'port:5683 "CoAP"'
            print(f"[Info] [AI] [Shodan] Searching for CoAP devices...")
            for result in self.api.search_cursor(query):
                if len(results) >= limit:
                    break
                ip = result.get('ip_str', '')
                if ip:
                    results.append(ip)
                    print(f"[Info] [AI] [Shodan] Found CoAP: {ip}")
        except Exception as e:
            print(f"[Error] [AI] [Shodan] Search failed: {e}")
        return results
    
    def save_results(self, results, filename):
        """Save results to botnet file"""
        if not results:
            return
        with open(filename, 'a') as f:
            for ip in results:
                f.write(f"{ip}\n")
        print(f"[Info] [AI] [Shodan] Saved {len(results)} results to {filename}")

class CensysScanner(object):
    """Censys API integration for finding vulnerable servers"""
    
    def __init__(self, api_id=None, api_secret=None):
        self.api_id = api_id or os.getenv('CENSYS_API_ID')
        self.api_secret = api_secret or os.getenv('CENSYS_API_SECRET')
        self.api = None
        if CENSYS_AVAILABLE and self.api_id and self.api_secret:
            try:
                self.api = CensysHosts(api_id=self.api_id, api_secret=self.api_secret)
            except:
                pass
    
    def search_memcached(self, limit=100):
        """Search for exposed Memcached servers"""
        if not self.api:
            return []
        results = []
        try:
            query = 'services.service_name: MEMCACHED AND services.port: 11211'
            print(f"[Info] [AI] [Censys] Searching for Memcached servers...")
            for page in self.api.search(query, per_page=100, pages=limit//100 + 1):
                for result in page:
                    if len(results) >= limit:
                        break
                    ip = result.get('ip', '')
                    if ip:
                        results.append(ip)
                        print(f"[Info] [AI] [Censys] Found Memcached: {ip}")
        except Exception as e:
            print(f"[Error] [AI] [Censys] Search failed: {e}")
        return results
    
    def search_ssdp(self, limit=100):
        """Search for SSDP devices"""
        if not self.api:
            return []
        results = []
        try:
            query = 'services.port: 1900 AND services.service_name: SSDP'
            print(f"[Info] [AI] [Censys] Searching for SSDP devices...")
            for page in self.api.search(query, per_page=100, pages=limit//100 + 1):
                for result in page:
                    if len(results) >= limit:
                        break
                    ip = result.get('ip', '')
                    if ip:
                        results.append(ip)
                        print(f"[Info] [AI] [Censys] Found SSDP: {ip}")
        except Exception as e:
            print(f"[Error] [AI] [Censys] Search failed: {e}")
        return results
    
    def save_results(self, results, filename):
        """Save results to botnet file"""
        if not results:
            return
        with open(filename, 'a') as f:
            for ip in results:
                f.write(f"{ip}\n")
        print(f"[Info] [AI] [Censys] Saved {len(results)} results to {filename}")
