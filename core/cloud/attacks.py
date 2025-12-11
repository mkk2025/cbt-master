#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

Cloud Infrastructure Targeting
"""
import socket, ssl, json, time, random
import urllib.request, urllib.error, urllib.parse

class CloudAttacker(object):
    """Cloud-specific attack vectors"""
    
    def __init__(self, ufonet):
        self.ufonet = ufonet
    
    def detect_cloud_provider(self, target):
        """Detect cloud provider"""
        try:
            if not target.startswith('http'):
                target = f'http://{target}'
            
            req = urllib.request.Request(target)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                headers = dict(response.headers)
                
                # AWS detection
                if 'x-amz' in str(headers).lower() or 'x-amzn' in str(headers).lower():
                    return 'aws'
                
                # Azure detection
                if 'x-azure' in str(headers).lower() or 'server' in headers and 'azure' in headers['Server'].lower():
                    return 'azure'
                
                # GCP detection
                if 'x-google' in str(headers).lower() or 'server' in headers and 'gfe' in headers['Server'].lower():
                    return 'gcp'
                
                # Cloudflare (CDN)
                if 'cf-ray' in headers:
                    return 'cloudflare'
        except:
            pass
        
        return 'unknown'
    
    def aws_amplification(self, target):
        """AWS-specific amplification attacks"""
        # S3 bucket enumeration
        # CloudFront cache poisoning
        # Lambda function abuse
        
        attacks = []
        
        # Try S3 bucket access
        parsed = urllib.parse.urlparse(target if '://' in target else f'http://{target}')
        domain = parsed.netloc or parsed.path.split('/')[0]
        
        # Common S3 bucket patterns
        bucket_patterns = [
            f"{domain}.s3.amazonaws.com",
            f"s3-{domain}.amazonaws.com",
            f"{domain}-assets.s3.amazonaws.com"
        ]
        
        for bucket_url in bucket_patterns:
            try:
                req = urllib.request.Request(f"http://{bucket_url}")
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status == 200:
                        attacks.append({
                            'type': 's3_bucket_access',
                            'target': bucket_url,
                            'status': 'vulnerable'
                        })
            except:
                pass
        
        return attacks
    
    def azure_attacks(self, target):
        """Azure-specific attacks"""
        # Blob storage enumeration
        # Function App abuse
        # App Service targeting
        
        attacks = []
        
        # Try Azure Blob Storage
        blob_patterns = [
            f"{target}.blob.core.windows.net",
            f"{target}-storage.blob.core.windows.net"
        ]
        
        for blob_url in blob_patterns:
            try:
                req = urllib.request.Request(f"https://{blob_url}")
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status in [200, 403]:  # 403 means exists but protected
                        attacks.append({
                            'type': 'azure_blob',
                            'target': blob_url,
                            'status': 'found'
                        })
            except:
                pass
        
        return attacks
    
    def gcp_attacks(self, target):
        """GCP-specific attacks"""
        # Cloud Storage bucket enumeration
        # Cloud Functions abuse
        # App Engine targeting
        
        attacks = []
        
        # Try GCP Cloud Storage
        storage_patterns = [
            f"{target}.storage.googleapis.com",
            f"storage.googleapis.com/{target}"
        ]
        
        for storage_url in storage_patterns:
            try:
                req = urllib.request.Request(f"https://{storage_url}")
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status in [200, 403]:
                        attacks.append({
                            'type': 'gcp_storage',
                            'target': storage_url,
                            'status': 'found'
                        })
            except:
                pass
        
        return attacks
    
    def cloudflare_bypass(self, target):
        """Cloudflare-specific bypass techniques"""
        # Use Cloudflare Workers
        # Cache poisoning
        # Edge server targeting
        
        techniques = [
            'cache_poisoning',
            'worker_bypass',
            'edge_targeting'
        ]
        
        return random.choice(techniques)
    
    def container_escape(self, target):
        """Container escape techniques"""
        # Docker API abuse
        # Kubernetes API targeting
        # Container registry attacks
        
        attacks = []
        
        # Try Docker API
        docker_endpoints = [
            f"{target}:2375",  # Unencrypted Docker
            f"{target}:2376",  # Encrypted Docker
        ]
        
        for endpoint in docker_endpoints:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((endpoint.split(':')[0], int(endpoint.split(':')[1])))
                if result == 0:
                    attacks.append({
                        'type': 'docker_api',
                        'target': endpoint,
                        'status': 'open'
                    })
                sock.close()
            except:
                pass
        
        return attacks
    
    def serverless_abuse(self, target, provider):
        """Serverless function abuse"""
        # Lambda/Function cold start attacks
        # Function enumeration
        # Event trigger abuse
        
        if provider == 'aws':
            # AWS Lambda
            lambda_patterns = [
                f"lambda.{target}",
                f"functions.{target}",
                f"{target}.lambda-url.region.on.aws"
            ]
        elif provider == 'azure':
            # Azure Functions
            lambda_patterns = [
                f"{target}.azurewebsites.net/api",
                f"{target}.azurefunctions.net"
            ]
        elif provider == 'gcp':
            # GCP Cloud Functions
            lambda_patterns = [
                f"{target}.cloudfunctions.net",
                f"{target}-functions.cloudfunctions.net"
            ]
        else:
            return []
        
        attacks = []
        for pattern in lambda_patterns:
            attacks.append({
                'type': 'serverless_enumeration',
                'target': pattern,
                'method': 'GET'
            })
        
        return attacks
