from scapy.all import *
from pandas import Series
from scipy.stats import entropy

def calcEntropy(data):
    b = bytearray(data)
    s = Series(b)
    counts = s.value_counts()
    return entropy(counts)

entropyThreshold = 2.5
def processPayloads(p):
    if not p.haslayer(Raw):
        return
    load = p[Raw].load
    e = calcEntropy(load)
    if e >= entropyThreshold and len(load) % 16 == 0:
        print("Potentially encrypted data detected with entropy %f" % e)
        print("\t%s" % load.hex())
    return

sniff(offline="EncryptedChannel.pcapng",prn=processPayloads)