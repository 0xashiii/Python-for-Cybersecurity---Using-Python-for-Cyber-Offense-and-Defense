from scapy.all import *
from scapy.layers.http import *

decoy_domains = [".fake.com"]

def processHTTP(p):
    if p.haslayer(HTTPRequest):
        if p[HTTPRequest].Cookie:
            host = p[HTTPRequest].Host.decode()
            decoy = [host.endswith(d) for d in decoy_domains]
            if True in decoy:
                print("Request to decoy domain %s from %s" % (host,p[IP].src))

sniff(offline="decoyCookie.pcap",prn=processHTTP)