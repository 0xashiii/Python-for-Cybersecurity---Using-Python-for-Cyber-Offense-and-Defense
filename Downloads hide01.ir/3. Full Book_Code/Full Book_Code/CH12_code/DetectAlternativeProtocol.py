from scapy.all import *
from base64 import b64decode

from pandas import Series
from scipy.stats import entropy

def calcEntropy(data):
    s = Series(data)
    counts = s.value_counts()
    return entropy(counts)

threshold = 100
def testData(d):
    if calcEntropy(d) > threshold:
        return "encrypted"
    try:
        decoded = b64decode(d)
        return decoded
    except:
        return False

def processPacket(p):
    if p.haslayer(IP):
        src = p[IP].src
        dst = p[IP].dst
    else:
        return
    
    if p.haslayer(DNS):
        hostname = p[DNS].qd.qname.decode("utf-8")
        d = hostname.split(".")
        for v in d:
            res = testData(v)
            if res == "encrypted":
                print("Potential encrypted data in DNS packet %s->%s" % (src,dst))
            elif res:
                print("Extracted data %s from DNS packet %s->%s" %(res,src,dst))

sniff(prn=processPacket)