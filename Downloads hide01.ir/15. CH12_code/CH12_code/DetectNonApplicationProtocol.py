from scapy.all import *

# Based on https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml
typecode = {
    0: [0],
    3: [x for x in range(16)],
    5: [x for x in range(4)],
    8: [0],
    9: [0,16],
    10: [0],
    11: [0,1],
    12: [0,1,2],
    13: [0],
    14: [0],
    40: [x for x in range(6)],
    41: [],
    42: [0],
    43: [x for x in range(5)],
    253: [],
    254: []
}
def testICMP(p):
    t = p[ICMP].type
    c = p[ICMP].code
    if t in typecode:
        if not c in typecode[t]:
            print("Anomalous code detected %x/%s" % (c,chr(c)))
    else:
        print("Anomalous type detected %x/%s" % (t,chr(t)))

def processPacket(p):
    if p.haslayer(ICMP):
        testICMP(p)

sniff(prn=processPacket)