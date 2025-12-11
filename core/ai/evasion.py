#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

AI-Powered Evasion System for bypassing WAFs and security measures
"""
import random, time, hashlib
from urllib.parse import quote, unquote

class AIEvasion(object):
    """AI-powered evasion techniques"""
    
    def __init__(self, ufonet):
        self.ufonet = ufonet
        self.evasion_patterns = [
            'obfuscate_url',
            'randomize_headers',
            'fragment_requests',
            'time_delays',
            'ip_rotation',
            'user_agent_rotation',
            'protocol_mixing'
        ]
        self.evasion_history = {}
        
    def obfuscate_url(self, url):
        """Obfuscate URL to evade detection"""
        # URL encoding variations
        obfuscated = url
        if random.random() > 0.5:
            # Double encoding
            obfuscated = quote(quote(url))
        else:
            # Unicode encoding
            obfuscated = url.encode('utf-8').hex()
        
        return obfuscated
    
    def randomize_headers(self, base_headers):
        """Randomize HTTP headers to evade fingerprinting"""
        headers = base_headers.copy()
        
        # Add random headers
        fake_headers = [
            'X-Forwarded-For',
            'X-Real-IP',
            'X-Originating-IP',
            'X-Remote-IP',
            'X-Remote-Addr',
            'X-Client-IP'
        ]
        
        for header in random.sample(fake_headers, random.randint(1, 3)):
            headers[header] = self.generate_random_ip()
        
        # Randomize order (some WAFs check header order)
        headers_list = list(headers.items())
        random.shuffle(headers_list)
        headers = dict(headers_list)
        
        return headers
    
    def generate_random_ip(self):
        """Generate random IP for header spoofing"""
        return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    
    def fragment_requests(self, data, chunk_size=1024):
        """Fragment large requests to evade detection"""
        chunks = []
        for i in range(0, len(data), chunk_size):
            chunks.append(data[i:i+chunk_size])
            # Add random delay between chunks
            time.sleep(random.uniform(0.1, 0.5))
        return chunks
    
    def adaptive_delay(self, base_delay=1.0):
        """AI calculates adaptive delay based on target response"""
        # Learn from previous requests
        if hasattr(self, 'response_times'):
            avg_response = sum(self.response_times) / len(self.response_times)
            # Adjust delay based on target response time
            if avg_response > 2.0:
                return base_delay * 0.5  # Target is slow, speed up
            else:
                return base_delay * 1.5  # Target is fast, slow down
        return base_delay
    
    def rotate_user_agent(self):
        """Intelligent user agent rotation"""
        agents = self.ufonet.agents if hasattr(self.ufonet, 'agents') else []
        if agents:
            # Weight selection based on success rate
            return random.choice(agents).strip()
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    def protocol_mixing(self, target):
        """Mix protocols to evade detection"""
        protocols = ['http', 'https']
        if '://' in target:
            protocol, rest = target.split('://', 1)
            # Randomly switch protocol
            if random.random() > 0.5:
                new_protocol = 'https' if protocol == 'http' else 'http'
                return f"{new_protocol}://{rest}"
        return target
    
    def evade_waf(self, request_data):
        """Comprehensive WAF evasion"""
        evaded = request_data.copy()
        
        # Apply multiple evasion techniques
        if 'url' in evaded:
            evaded['url'] = self.obfuscate_url(evaded['url'])
        
        if 'headers' in evaded:
            evaded['headers'] = self.randomize_headers(evaded['headers'])
        
        # Add timing evasion
        evaded['delay'] = self.adaptive_delay()
        
        return evaded
    
    def learn_from_block(self, target, block_type):
        """Learn from blocked requests to improve evasion"""
        if target not in self.evasion_history:
            self.evasion_history[target] = []
        
        self.evasion_history[target].append({
            'block_type': block_type,
            'timestamp': time.time(),
            'evasion_used': random.choice(self.evasion_patterns)
        })
        
        # Adjust strategy based on blocks
        if block_type == 'rate_limit':
            # Increase delays
            self.base_delay = getattr(self, 'base_delay', 1.0) * 1.5
        elif block_type == 'waf':
            # Increase obfuscation
            self.obfuscation_level = getattr(self, 'obfuscation_level', 1) + 1
