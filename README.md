<div align="center">
  <img src="./cbt.jpg" alt="CBT - Core Brim Tech" width="500">
  <h1>CBT - Core Brim Tech</h1>
  <p><strong>Denial of Service Toolkit | C&C/DarkNet</strong></p>
</div>

----------

 + Website:   https://www.corebrimtech.com

----------

#### Description:

  CBT (Core Brim Tech) - is a free software, P2P and cryptographic -disruptive toolkit- that allows to perform DoS and DDoS attacks; 
on the Layer 7 (APP/HTTP) through the exploitation of Open Redirect vectors on third-party websites to act as a botnet 
and on the Layer3 (Network) abusing the protocol.

  It also works as an encrypted DarkNET to publish and receive content by creating a global client/server network based 
on a direct-connect P2P architecture.

  See these links for more info:

   - FAQ:
     https://www.corebrimtech.com/FAQ.html

   - CWE-601:Open Redirect: 
     https://cwe.mitre.org/data/definitions/601.html

  ![CBT](https://www.corebrimtech.com/cbt/cbt-schema.png "CBT Schema")

   - LOIC: 
     https://en.wikipedia.org/wiki/Low_Orbit_Ion_Cannon

   - LORIS: 
     https://en.wikipedia.org/wiki/Slowloris_(software)

   - UFOSYN: 
     https://en.wikipedia.org/wiki/SYN_flood

   - FRAGGLE: 
     https://en.wikipedia.org/wiki/Fraggle_attack

   - UFORST: 
     https://ddos-guard.net/en/terminology/attack_type/rst-or-fin-flood

   - SPRAY: 
     https://en.wikipedia.org/wiki/DRDOS

   - SMURF: 
     https://en.wikipedia.org/wiki/Smurf_attack

   - XMAS: 
     https://en.wikipedia.org/wiki/Christmas_tree_packet

   - DROPER: 
     https://en.wikipedia.org/wiki/IP_fragmentation_attack

   - SNIPER: 
     https://www.imperva.com/learn/application-security/snmp-reflection/

   - TACHYON: 
     https://www.us-cert.gov/ncas/alerts/TA13-088A

   - PINGER: 
     https://www.cloudflare.com/learning/ddos/ping-icmp-flood-ddos-attack/

   - MONLIST: 
     https://www.us-cert.gov/ncas/alerts/TA14-013A

   - UFOACK: 
     https://www.f5.com/services/resources/glossary/push-and-ack-flood

   - OVERLAP: 
     https://cyberhoot.com/cybrary/fragment-overlap-attack/

   - UFOUDP: 
     https://en.wikipedia.org/wiki/UDP_flood_attack

   - NUKE: 
     https://dl.packetstormsecurity.net/papers/general/tcp-starvation.pdf

----------

#### Installing:

  CBT runs on many platforms:

  You can try to automatically get all required libraries using (as root):

       python3 setup.py

  For manual installation, run:

       sudo apt-get install -y --no-install-recommends libpython3.11-dev python3-pycurl python3-geoip python3-whois python3-cryptography python3-requests libgeoip1 libgeoip-dev
       python3 -m pip install --upgrade pip --no-warn-script-location --root-user-action=ignore
       python3 -m pip install pycurl --upgrade --root-user-action=ignore
       python3 -m pip install GeoIP python-geoip pygeoip requests whois scapy pycryptodomex duckduckgo-search --ignore-installed --root-user-action=ignore

----------

####  License:

  CBT (Core Brim Tech) is released under the GPLv3. You can find the full license text
in the [LICENSE](./docs/LICENSE) file.

----------

####  Screenshots (current version!):

  ![CBT](https://www.corebrimtech.com/cbt/cbt-shell-1.png "CBT Shell Version")

  ![CBT](https://www.corebrimtech.com/cbt/cbt-shell-2.png "CBT Shell Board")

  ![CBT](https://www.corebrimtech.com/cbt/cbt-shell-3.png "CBT GUI Shell")

  ![CBT](https://www.corebrimtech.com/cbt/cbt-main_small.png "CBT GUI Main Panel")

  ![CBT](https://www.corebrimtech.com/cbt/cbt-help_small.png "CBT GUI Help")

  ![CBT](https://www.corebrimtech.com/cbt/cbt-botnet.png "CBT GUI Botnet")

  ![CBT](https://www.corebrimtech.com/cbt/cbt-stats.png "CBT GUI General Stats")

  ![CBT](https://www.corebrimtech.com/cbt/cbt-ranking_small.png "CBT GUI Ranking")

  ![CBT](https://www.corebrimtech.com/cbt/cbt-attack.png "CBT GUI Attack")

  ![CBT](https://www.corebrimtech.com/cbt/cbt-board_small.png "CBT GUI Board")

  ![CBT](https://www.corebrimtech.com/cbt/cbt-wargames_small.png "CBT GUI Wargames")

  ![CBT](https://www.corebrimtech.com/cbt/cbt-gui3_small.png "CBT GeoMap /deploying/")

  ![CBT](https://www.corebrimtech.com/cbt/cbt-gui4_small.png "CBT GeoMap /attacking/")

