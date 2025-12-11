#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
This file is part of the CBT (Core Brim Tech) project, https://www.corebrimtech.com

Copyright (c) 2024 | MOMODU KAMARA-KOLLEH

You should have received a copy of the GNU General Public License along
with CBT; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import socket, threading, re, os, time, base64, traceback
import webbrowser, subprocess, json, sys, shlex
import urllib.request, urllib.error
from urllib.parse import urlparse as urlparse
from .main import UFONet
try:
    import pygeoip
except:
    print("\n[Error] [AI] Cannot import lib: pygeoip. \n\n To install it try:\n\n $ 'sudo apt-get install python3-geoip libgeoip-dev libgeoip1'\n")
    sys.exit(2)

class AjaxMap(object):
    def __init__(self):
        self.geo_db_mirror1 = 'https://turina.space/bordercheck/maps.tar.gz'  # Turina Server
        self._geoip=None
        self._geoasn=None
        self._geoipstatus='nomap'
        self._err=''
        ufonet = UFONet()
        ufonet.create_options()
        # Track botnet types by source
        self.botnet_types = {}  # Map botnet URL to type
        try:
            self.zombies = ufonet.extract_zombies() or []
            for z in self.zombies:
                self.botnet_types[z] = 'zombie'
            
            aliens_army = ufonet.extract_aliens() or []
            for a in aliens_army:
                self.botnet_types[a] = 'alien'
            
            droids_army = ufonet.extract_droids() or []
            for d in droids_army:
                self.botnet_types[d] = 'droid'
            
            ucavs_army = ufonet.extract_ucavs() or []
            for u in ucavs_army:
                self.botnet_types[u] = 'ucav'
            
            rpcs_army = ufonet.extract_rpcs() or []
            for r in rpcs_army:
                self.botnet_types[r] = 'rpc'
            
            ntps_army = ufonet.extract_ntps() or []
            for n in ntps_army:
                self.botnet_types[n] = 'ntp'
            
            dnss_army = ufonet.extract_dnss() or []
            for d in dnss_army:
                self.botnet_types[d] = 'dns'
            
            snmps_army = ufonet.extract_snmps() or []
            for s in snmps_army:
                self.botnet_types[s] = 'snmp'
            
            # New botnet types
            try:
                memcacheds_army = ufonet.extract_memcacheds() or []
                for m in memcacheds_army:
                    self.botnet_types[m] = 'memcached'
            except:
                memcacheds_army = []
            try:
                ssdps_army = ufonet.extract_ssdps() or []
                for s in ssdps_army:
                    self.botnet_types[s] = 'ssdp'
            except:
                ssdps_army = []
            try:
                chargens_army = ufonet.extract_chargens() or []
                for c in chargens_army:
                    self.botnet_types[c] = 'chargen'
            except:
                chargens_army = []
            try:
                http2s_army = ufonet.extract_http2s() or []
                for h in http2s_army:
                    self.botnet_types[h] = 'http2'
            except:
                http2s_army = []
            try:
                rudys_army = ufonet.extract_rudys() or []
                for r in rudys_army:
                    self.botnet_types[r] = 'rudy'
            except:
                rudys_army = []
            try:
                coaps_army = ufonet.extract_coaps() or []
                for c in coaps_army:
                    self.botnet_types[c] = 'coap'
            except:
                coaps_army = []
            
            self.zombies.extend(aliens_army)
            self.zombies.extend(droids_army)
            self.zombies.extend(ucavs_army)
            self.zombies.extend(rpcs_army)
            self.zombies.extend(ntps_army)
            self.zombies.extend(dnss_army)
            self.zombies.extend(snmps_army)
            self.zombies.extend(memcacheds_army)
            self.zombies.extend(ssdps_army)
            self.zombies.extend(chargens_army)
            self.zombies.extend(http2s_army)
            self.zombies.extend(rudys_army)
            self.zombies.extend(coaps_army)
        except Exception as e:
            print(f"[Error] [AI] Failed to extract botnets: {e}")
            import traceback
            traceback.print_exc()
            return

    def get_err(self):
        return self._err

    # check for geoip data status
    # basic lock file mechanism to avoid multiple downloads
    def get_status(self):
        if os.path.exists('maps.downloading'):
            if not os.path.exists('maps.downloadmsg'):
                f=open("maps.downloadmsg","wb")
                f.write("".encode('utf-8'))
                f.close()
                print("[Info] [AI] [Control] GeoIP data download started! -> [OK!]\n")
            self._geoipstatus='downloading'
        elif os.path.isdir('maps'):
            if self._geoip == None :
                self._geoip = pygeoip.GeoIP('maps/GeoLiteCity.dat')
            if self._geoasn == None :
                self._geoasn = pygeoip.GeoIP('maps/GeoIPASNum.dat')
            if os.path.exists("maps.downloadmsg") :
                os.remove("maps.downloadmsg")
            self._geoipstatus='ok'
        return self._geoipstatus

    def retrieve(self,url,name):
        try:
            handle = urllib.request.urlopen(url)
            CHUNK = 16384
            with open(name,'wb') as fp:
                while True:
                    chunk = handle.read(CHUNK)
                    if not chunk:
                        break
                    fp.write(chunk)
        except:
            traceback.print_exc()

    def download_maps(self):
        # generate geolocation values on a map
        if self.get_status() != 'nomap':
            return self._geoipstatus == 'ok'
        if os.path.exists("maps.downloadmsg"):
            os.remove("maps.downloadmsg")
        f=open("maps.downloading",'w')
        f.write("download started<script>$'('#ufomsg').load('/js/ajax.js?fetchmap=')")
        f.close()
        self._geoipstatus="downloading"
        try: # mirror 1
            print("\n[Info] [AI] Fetching maps from 'Turina Server':", self.geo_db_mirror1 + "\n")
            response = self.retrieve(self.geo_db_mirror1, 'maps.tar.gz')
        except:
            print(("[Error] [AI] Something wrong fetching maps from remote servers! -> [Aborting!]"), "\n")
            traceback.print_exc()
            return False #sys.exit(2)
        subprocess.call(shlex.split('tar zxfv maps.tar.gz'))
        print("\n[Info] [AI] [Control] GeoIP maps and databases -> [OK!]\n")
        # set pygeoip data sources
        self._geoip = pygeoip.GeoIP('maps/GeoLiteCity.dat')
        self._geoasn = pygeoip.GeoIP('maps/GeoIPASNum.dat')
        self._geoipstatus='ok'
        os.remove('maps.tar.gz')
        os.remove('maps.downloading')
        return True

    # fetches geoip data for specified zombie
    def geo_ip(self, zombie):
        # check for status, downloading is done by ajax() method
        if self.get_status() != 'ok':
            if self._geoipstatus =='downloading':
                print("\n[Info] [AI] [Control] GeoIP maps and databases -> [Downloading!]\n")
                self._err= "ufomsg('[Info] [AI] Downloading maps... -> [Waiting!]')"
            elif not os.path.exists('maps/GeoIPASNum.dat') or not os.path.exists('maps/GeoLiteCity.dat'):
                print("\n[Info] [AI] GeoIP maps and databases -> [Starting!]\n")
                self._err= "ufomsg('[Info] [AI] Map download starting')\n$('#ufomsg').load('/js/ajax.js?fetchgeoip=')"
            else:
                print("\n[Error] [AI] GeoIP maps and databases: FAILED! -> [Discarding!]\n")
                self._err= "ufomsg('<font color='red'>[Info] [AI]</font> Maps: unknown error -> [Discarding!]')"
            return None
        if re.match(r'^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$', zombie) or re.match(r'^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$', zombie) or re.match(r'^192.168\.\d{1,3}\.\d{1,3}$', zombie) or re.match(r'^172.(1[6-9]|2[0-9]|3[0-1]).[0-9]{1,3}.[0-9]{1,3}$', zombie) or re.match('localhost', zombie):
            self._err= "ufomsg('<font color='red'>[Info] [AI] [Control]</font> Maps: invalid ip data -> [Discarding!]')"
            return None
        # create geoip data skeleton
        geo_zombie={}
        geo_zombie['qq']=zombie
        url = urlparse(zombie)
        geo_zombie['city'] = '-'
        geo_zombie['country'] = '-'
        geo_zombie['country_code'] = '-'
        geo_zombie['longitude'] = '-'
        geo_zombie['latitude'] = '-'
        geo_zombie['ip'] = '-'
        geo_zombie['host_name'] = '-'
        geo_zombie['asn'] = '-'
        geo_zombie['latitude'] = '-'
        # retrieve and allocate geoip data
        try:
            ip = socket.gethostbyname(url.netloc)
        except:
            try:
                import dns.resolver
                r = dns.resolver.Resolver()
                r.nameservers = ['8.8.8.8', '8.8.4.4'] # google DNS resolvers
                a = r.query(url.netloc, "A") # A record
                for rd in a:
                    ip = str(rd)
            except:
                self._err= "ufomsg('<font color='yellow'>[Error] [AI]</font> GeoIP: hostbyname failed for "+str(url.netloc)+"...')"
                return None
        if ip:
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",ip):
                geo_zombie['ip'] = ip
                try:
                    record = self._geoip.record_by_addr(ip)
                except Exception as e:
                    # Better error handling - don't fail completely, use defaults
                    self._err= "ufomsg('<font color='yellow'>[Warning] [AI] </font> GeoIP: lookup failed for "+ip+", using defaults...')"
                    # Set default location (middle of ocean) instead of failing
                    geo_zombie['latitude'] = 0.0
                    geo_zombie['longitude'] = 0.0
                    geo_zombie['city'] = 'Unknown'
                    geo_zombie['country'] = 'Unknown'
                    geo_zombie['country_code'] = 'XX'
                    return geo_zombie  # Return with defaults instead of None
                try:
                    asn = self._geoasn.org_by_addr(ip)
                    if asn is not None:
                        geo_zombie['asn'] = asn
                    else:
                        geo_zombie['asn'] = 'No ASN provided'
                except Exception as e:
                    # Don't fail on ASN lookup errors
                    geo_zombie['asn'] = 'ASN lookup failed'
                try:
                    geo_zombie['host_name'] = socket.gethostbyaddr(ip)[0]
                except:
                    geo_zombie['host_name'] = 'No hostname'
                try:
                    longitude = str(float(record['longitude']))
                    geo_zombie['longitude'] = longitude
                    latitude = str(float(record['latitude']))
                    geo_zombie['latitude'] = latitude
                except:
                    pass
                try:
                    geo_zombie['country'] = record["country_name"]
                    geo_zombie['country_code'] = record["country_code"].lower()
                    if record['city'] is not None:
                        geo_zombie['city'] = record["city"]
                except:
                    pass
        else:
            geo_zombie = None
        return geo_zombie

    # generates javascript for adding a new zombie with geoip data
    def get_js(self,z):
        ret = ""
        try:
            gz = self.geo_ip(z)
            # Proper error handling - check if geoip returned valid data
            if gz is not None and gz.get('latitude') != '-' and gz.get('latitude') is not None:
                # Escape single quotes in strings to prevent JS errors
                city = str(gz.get('city', '-')).replace("'", "\\'")
                country = str(gz.get('country', '-')).replace("'", "\\'")
                country_code = str(gz.get('country_code', '-')).replace("'", "\\'")
                asn = str(gz.get('asn', '-')).replace("'", "\\'")
                ip = str(gz.get('ip', '-')).replace("'", "\\'")
                host_name = str(gz.get('host_name', '-')).replace("'", "\\'")
                
                # Determine botnet type for different marker colors
                botnet_type = self.determine_botnet_type(z)
                ret = "Zombies.add('"+str(z)+"',Array(new L.LatLng("+str(gz['latitude'])+","+str(gz['longitude'])+"),'"+city+"','"+country+"','"+country_code+"','"+asn+"','"+ip+"','"+host_name+"','"+botnet_type+"'))\n"
            else:
                # GeoIP failed but don't block - mark as dead
                ret += "dead_zombies.push('"+z+"')\n"
        except Exception as e:
            # Catch any errors and mark as dead instead of crashing
            ret += "dead_zombies.push('"+z+"')\n"
            print(f"[Warning] [AI] Failed to get GeoIP for {z}: {e}")
        ret += "last_zombie = '"+z+"'\n"
        return ret
    
    def determine_botnet_type(self, z):
        """Determine botnet type from tracked source"""
        # Use tracked type from source file
        return self.botnet_types.get(z, 'zombie')  # default to zombie if not found

    # fetches next zombie from list (using all types of zombies)
    def get_next_zombie(self,name):
        if name in self.zombies:
            for z in self.zombies:
                if name == None:
                    return z
                if z == name:
                    name = None
            return None
        else:
            return self.zombies[0]

    # ajax controller
    def ajax(self,pGet={}):
        if 'fetchgeoip' in list(pGet.keys()):
            if self.get_status() == "nomap":
                self.download_maps()
                return "[Info] [AI] [Control] Geoip data download! -> [OK!]<br/>"
        if 'stats' in list(pGet.keys()):
            stat='<script>$(".ufo_stat_div").show()</script>'
            if os.path.exists('/tmp/ufonet.html'):
                for x in open(r'/tmp/ufonet.html').readlines():
                    stat = stat + x
            else:
                stat="<i>[Info] [AI] [Control] Generating statistics... -> [Waiting!]</i>"
            return stat+"</div>"
        if self.get_status() != "ok":
            dljs=""
            if self.get_status() == "nomap":
                dljs+="$('#ufomsg').load('/js/ajax.js?fetchgeoip=')\n"
            if 'doll' in list(pGet.keys()):
                dljs+="$('#ufomsg').load('/js/ajax.js?fetchdoll="+pGet['doll']+"')\n"
                dljs+="doll=new Doll('"+pGet["doll"]+"')\n"
            return "[Info] [AI] GeoIP data download in progress...<br><i>See console for errors</i>+<script>"+dljs+"</script>"
        if 'zombie' in list(pGet.keys()):
            zn=base64.b64decode(pGet['zombie']).decode('utf-8')
            nzn=self.get_next_zombie(zn)
            if nzn is not None:
                try:
                    zombie=self.get_js(nzn)
                    if zombie:
                        return " <script>\n"+str(zombie)+"\nufomsg('[Info] [AI] [Control] Adding zombie: "+str(nzn)+"...')\n</script>"
                    else:
                        # GeoIP lookup failed, skip this zombie
                        return "<script>ufomsg('[Warning] [AI] [Control] Skipping zombie: "+str(nzn)+" (GeoIP failed)')</script>"
                except Exception as e:
                    # Proper error handling
                    error_msg = str(e).replace("'", "\\'")
                    return "<script>ufomsg('[Error] [AI] [Control] Failed to load zombie: "+str(nzn)+" - "+error_msg+"')</script>"
            else:
                return "<script>zdone=true\nufomsg('[Info] [AI] [Control] All zombies deployed! -> [OK!]')\n </script>\n"
        # Batch loading support
        if 'batch_zombies' in list(pGet.keys()):
            try:
                batch_data = json.loads(base64.b64decode(pGet['batch_zombies']).decode('utf-8'))
                results = []
                for zn in batch_data:
                    try:
                        zombie_js = self.get_js(zn)
                        if zombie_js:
                            results.append(zombie_js)
                    except:
                        continue
                if results:
                    return "<script>" + "\n".join(results) + "</script>"
                return "<script>ufomsg('[Info] [AI] [Control] Batch processed')</script>"
            except Exception as e:
                return "<script>ufomsg('[Error] [AI] [Control] Batch processing failed: " + str(e) + "')</script>"
        if 'fetchdoll' in list(pGet.keys()):
            tn=pGet['fetchdoll']
            target = self.geo_ip(tn)
            if target is None:
                return "doll waiting for geoip data !"
            return " doll up !<script>\ndoll.setData(Array(new L.LatLng("+str(target['latitude'])+","+str(target['longitude'])+"),'"+target['city']+"','"+target['country']+"','"+target['country_code']+"','"+target['asn']+"','"+target['ip']+"','"+target['host_name']+"'))\nufomsg('[Info] Adding target: "+tn+"...')\ndoll.show() </script>"
        if 'doll' in list(pGet.keys()):
            tn=pGet['doll']
            return "<script>\ndoll=new Doll('"+tn+"')\n</script>"
        return "\n"
