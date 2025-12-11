#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

Encrypted P2P Network
"""
import socket, threading, json, time, hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import base64

class P2PNode(object):
    """P2P network node with encryption"""
    
    def __init__(self, ufonet, port=7777):
        self.ufonet = ufonet
        self.port = port
        self.peers = {}
        self.encryption_keys = {}
        self.running = False
        self.message_queue = []
    
    def generate_key(self, peer_id):
        """Generate encryption key for peer"""
        if peer_id not in self.encryption_keys:
            self.encryption_keys[peer_id] = get_random_bytes(32)
        return self.encryption_keys[peer_id]
    
    def encrypt_message(self, message, peer_id):
        """Encrypt message for peer"""
        key = self.generate_key(peer_id)
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(json.dumps(message).encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()
    
    def decrypt_message(self, encrypted, peer_id):
        """Decrypt message from peer"""
        key = self.generate_key(peer_id)
        data = base64.b64decode(encrypted)
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        return json.loads(cipher.decrypt_and_verify(ciphertext, tag))
    
    def connect_peer(self, host, port):
        """Connect to peer"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            peer_id = f"{host}:{port}"
            self.peers[peer_id] = {
                'sock': sock,
                'host': host,
                'port': port,
                'connected': True
            }
            print(f"[Info] [AI] [P2P] Connected to peer {peer_id}")
            return True
        except Exception as e:
            print(f"[Error] [AI] [P2P] Connection failed: {e}")
            return False
    
    def broadcast_message(self, message_type, data):
        """Broadcast message to all peers"""
        message = {
            'type': message_type,
            'data': data,
            'timestamp': time.time(),
            'node_id': f"{socket.gethostname()}:{self.port}"
        }
        
        for peer_id, peer in self.peers.items():
            try:
                encrypted = self.encrypt_message(message, peer_id)
                peer['sock'].sendall(f"{len(encrypted):010d}{encrypted}".encode())
            except Exception as e:
                print(f"[Error] [AI] [P2P] Broadcast failed to {peer_id}: {e}")
    
    def share_botnet(self, botnet_type, entries):
        """Share botnet entries with peers"""
        self.broadcast_message('botnet_share', {
            'type': botnet_type,
            'entries': entries
        })
    
    def receive_botnet(self, message):
        """Receive botnet entries from peer"""
        botnet_type = message['data']['type']
        entries = message['data']['entries']
        
        filename = f"botnet/{botnet_type}.txt"
        with open(filename, 'a') as f:
            for entry in entries:
                f.write(f"{entry}\n")
        
        print(f"[Info] [AI] [P2P] Received {len(entries)} {botnet_type} entries")
