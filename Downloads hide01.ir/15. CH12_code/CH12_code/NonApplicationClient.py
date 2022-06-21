from scapy.all import *

def transmit(message, host):
    for m in message:
        packet = IP(dst=host)/ICMP(code = ord(m))
        send(packet)

host = "3.220.15.183"
message = "Hello"
transmit(message,host)