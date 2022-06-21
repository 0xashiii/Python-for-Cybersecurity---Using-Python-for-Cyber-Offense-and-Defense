from scapy.all import *
import re,struct

def processPacket(p):
    if not p.haslayer(SMB2_Header):
        return
    cmd = p[SMB2_Header].Command
    if cmd in [1280]:
        d = p[Raw].load.decode("utf-16")
        matches = re.findall("[ -~]*[.][ -~]*",d)
        if matches:
            print("File operation detected: %s" % matches)
    elif cmd == 256:
        load = p[Raw].load
        try:
            ind = load.index(bytes("NTLMSSP","utf-8"))
        except:
            return
        if ind > -1 and load[ind+8] == 3:
            nameLen = struct.unpack("<h",load[ind+36:ind+38])[0]
            userOffset = ind+struct.unpack("<hh",load[ind+40:ind+44])[0]
            username = load[userOffset:userOffset+nameLen].decode("utf-16")
            print("Account access attempt: %s" % username)

sniff(offline="SMB.pcapng",prn=processPacket)