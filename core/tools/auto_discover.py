#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

Auto-Discovery Tool - Finds vulnerable servers using multiple methods
"""
import socket, random, time, threading
from .scanner import AutoScanner
from .shodan_scanner import ShodanScanner, CensysScanner

class AutoDiscover(object):
    """Automated discovery of vulnerable servers using multiple sources"""
    
    def __init__(self, ufonet):
        self.ufonet = ufonet
        self.scanner = AutoScanner(ufonet)
        self.shodan = None
        self.censys = None
        
    def setup_shodan(self, api_key):
        """Setup Shodan scanner"""
        self.shodan = ShodanScanner(api_key)
    
    def setup_censys(self, api_id, api_secret):
        """Setup Censys scanner"""
        self.censys = CensysScanner(api_id, api_secret)
    
    def discover_memcached(self, methods=['shodan', 'censys', 'scan'], limit=100):
        """Discover Memcached servers using multiple methods"""
        results = []
        
        if 'shodan' in methods and self.shodan:
            print("[Info] [AI] [AutoDiscover] Using Shodan...")
            shodan_results = self.shodan.search_memcached(limit)
            results.extend(shodan_results)
            self.shodan.save_results(shodan_results, 'botnet/memcacheds.txt')
        
        if 'censys' in methods and self.censys:
            print("[Info] [AI] [AutoDiscover] Using Censys...")
            censys_results = self.censys.search_memcached(limit)
            results.extend(censys_results)
            self.censys.save_results(censys_results, 'botnet/memcacheds.txt')
        
        if 'scan' in methods:
            print("[Info] [AI] [AutoDiscover] Scanning common IP ranges...")
            # Scan common cloud provider ranges (for authorized testing)
            common_ranges = [
                ('1.1.1.0', '1.1.1.255'),  # Example range
            ]
            for start, end in common_ranges:
                scan_results = self.scanner.scan_ip_range(start, end, 'memcached')
                results.extend(scan_results.get('memcacheds', []))
        
        return list(set(results))  # Remove duplicates
    
    def discover_ssdp(self, methods=['shodan', 'censys', 'scan'], limit=100):
        """Discover SSDP devices using multiple methods"""
        results = []
        
        if 'shodan' in methods and self.shodan:
            shodan_results = self.shodan.search_ssdp(limit)
            results.extend(shodan_results)
            self.shodan.save_results(shodan_results, 'botnet/ssdps.txt')
        
        if 'censys' in methods and self.censys:
            censys_results = self.censys.search_ssdp(limit)
            results.extend(censys_results)
            self.censys.save_results(censys_results, 'botnet/ssdps.txt')
        
        return list(set(results))
    
    def discover_all(self, methods=['shodan', 'censys'], limit=100):
        """Discover all types of vulnerable servers"""
        print("[Info] [AI] [AutoDiscover] Starting comprehensive discovery...")
        
        all_results = {
            'memcacheds': self.discover_memcached(methods, limit),
            'ssdps': self.discover_ssdp(methods, limit),
        }
        
        if 'shodan' in methods and self.shodan:
            all_results['ntps'] = self.shodan.search_ntp(limit)
            self.shodan.save_results(all_results['ntps'], 'botnet/ntp.txt')
            
            all_results['dnss'] = self.shodan.search_dns(limit)
            self.shodan.save_results(all_results['dnss'], 'botnet/dns.txt')
            
            all_results['snmps'] = self.shodan.search_snmp(limit)
            self.shodan.save_results(all_results['snmps'], 'botnet/snmp.txt')
            
            all_results['coaps'] = self.shodan.search_coap(limit)
            self.shodan.save_results(all_results['coaps'], 'botnet/coaps.txt')
        
        print(f"[Info] [AI] [AutoDiscover] Discovery complete!")
        print(f"[Info] [AI] [AutoDiscover] Found: {sum(len(v) for v in all_results.values())} total servers")
        
        return all_results
