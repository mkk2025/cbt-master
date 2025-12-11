#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

Steganography & Covert Channels
"""
import base64, hashlib, random, time
from urllib.parse import quote, unquote

class Steganography(object):
    """Steganography and covert channel techniques"""
    
    def __init__(self, ufonet):
        self.ufonet = ufonet
    
    def dns_tunnel(self, data, domain):
        """DNS tunneling for covert communication"""
        # Encode data in DNS queries
        encoded = base64.b32encode(data.encode()).decode().lower()
        chunks = [encoded[i:i+63] for i in range(0, len(encoded), 63)]  # DNS label limit
        
        queries = []
        for chunk in chunks:
            query = f"{chunk}.{domain}"
            queries.append(query)
        
        return queries
    
    def header_steganography(self, payload, headers):
        """Hide payload in HTTP headers"""
        # Encode payload in header values
        encoded = base64.b64encode(payload.encode()).decode()
        
        # Split into header-sized chunks
        header_names = ['X-Request-ID', 'X-Correlation-ID', 'X-Trace-ID', 'X-Session-ID']
        stego_headers = {}
        
        chunk_size = 20  # Reasonable header value length
        for i, chunk in enumerate([encoded[j:j+chunk_size] for j in range(0, len(encoded), chunk_size)]):
            if i < len(header_names):
                stego_headers[header_names[i]] = chunk
        
        # Merge with existing headers
        headers.update(stego_headers)
        return headers
    
    def image_steganography(self, payload, image_path):
        """Hide payload in image (LSB steganography)"""
        try:
            from PIL import Image
            import numpy as np
            
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Convert payload to binary
            payload_bin = ''.join(format(ord(c), '08b') for c in payload)
            payload_bin += '1111111111111110'  # End marker
            
            # Embed in LSB of pixels
            flat = img_array.flatten()
            for i, bit in enumerate(payload_bin):
                if i < len(flat):
                    flat[i] = (flat[i] & 0xFE) | int(bit)
            
            # Reshape and save
            stego_array = flat.reshape(img_array.shape)
            stego_img = Image.fromarray(stego_array.astype(np.uint8))
            stego_img.save(image_path.replace('.', '_stego.'))
            
            return True
        except Exception as e:
            print(f"[Error] [AI] [Stego] Image steganography failed: {e}")
            return False
    
    def timing_channel(self, data, base_delay=1.0):
        """Timing-based covert channel"""
        # Encode data in timing delays
        delays = []
        for byte in data.encode():
            # Each byte encoded as delay multiplier (0-255 -> 0.1-2.5 seconds)
            delay = base_delay * (0.1 + (byte / 255.0) * 2.4)
            delays.append(delay)
        
        return delays
    
    def http_body_steganography(self, payload, legitimate_content):
        """Hide payload in HTTP body"""
        # Use whitespace steganography
        # Encode payload in whitespace patterns
        encoded = ''.join(format(ord(c), '08b') for c in payload)
        
        stego_content = legitimate_content
        for i, bit in enumerate(encoded):
            if i < len(stego_content):
                # Use space vs tab to encode bits
                if bit == '1':
                    stego_content = stego_content[:i] + '\t' + stego_content[i+1:]
        
        return stego_content
    
    def extract_from_headers(self, headers):
        """Extract hidden payload from headers"""
        stego_headers = ['X-Request-ID', 'X-Correlation-ID', 'X-Trace-ID', 'X-Session-ID']
        encoded = ''
        
        for header in stego_headers:
            if header in headers:
                encoded += headers[header]
        
        try:
            payload = base64.b64decode(encoded).decode()
            return payload
        except:
            return None
