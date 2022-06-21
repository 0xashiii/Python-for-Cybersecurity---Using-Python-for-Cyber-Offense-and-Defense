from dnslib import *
from dnslib.server import DNSServer

host="localhost"
port = 8053

subdomains = {
    "www.": "10.0.0.1",
    "smtp.": "10.0.0.2"
}
domain = "example.com"
honeyip = "10.0.0.0"

blocked = {}

class HoneyResolver:
    def resolve(self,request,handler):
        subdomain = str(request.q.qname.stripSuffix(domain+"."))
        if subdomain in subdomains:
            reply = request.reply()
            ip = subdomains[subdomain]
            reply.add_answer(RR(
                rname=request.q.qname,
                rtype=QTYPE.A,
                rclass=1,
                ttl=300,
                rdata=A(ip)))
        else:
            reply = request.reply()
            reply.add_answer(RR(
                rname=request.q.qname,
                rtype=QTYPE.A,
                rclass=1,
                ttl=300,
                rdata=A(honeyip)))
        return reply

resolver = HoneyResolver()
server = DNSServer(resolver,port=port,address=host)
server.start_thread()
while True:
    time.sleep(5)
server.stop()