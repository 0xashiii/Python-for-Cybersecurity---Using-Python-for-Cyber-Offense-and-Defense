from scapy.all import *

ip = "192.168.1.209"
ports = [53,80]
honeys = [8080,8443]

blocked = []

def analyzePackets(p):
    global blocked
    if p.haslayer(IP):
        response = Ether(src=p[Ether].dst,dst=p[Ether].src)/\
            IP(src=p[IP].dst,dst=p[IP].src)/\
            TCP(sport=p[TCP].dport,dport=p[TCP].sport,ack=p[TCP].seq+1)
        source = p[IP].src
    else:
        response = Ether(src=p[Ether].dst,dst=p[Ether].src)/\
            IPv6(src=p[IPv6].dst,dst=p[IPv6].src)/\
            TCP(sport=p[TCP].dport,dport=p[TCP].sport,ack=p[TCP].seq+1)
        source = p[IPv6].src
        
    port = p[TCP].dport
    if port in honeys:
        p.show()
    if source in blocked:
        if port in ports:
            response[TCP].flags = "RA"
        elif port in honeys: 
            response[TCP].flags = "SA"
        sendp(response,verbose=False)
    else:
        if source not in ports:
            blocked += source
            if port in honeys:
                response[TCP].flags = "SA"
                sendp(response,verbose=False)

f = "dst host "+ip+" and tcp"
sniff(filter=f,prn=analyzePackets)
