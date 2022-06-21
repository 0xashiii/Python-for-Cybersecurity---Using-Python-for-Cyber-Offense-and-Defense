import win32evtlog
import xml.etree.ElementTree as ET

server = "localhost"
logtype = "Microsoft-Windows-WMI-Activity/Trace"
flags = win32evtlog.EvtQueryForwardDirection
query = "*[System[EventID=23]]"

def GetEventLogs():
    q = win32evtlog.EvtQuery(logtype,flags,query)
    events = ()
    while True:
        e = win32evtlog.EvtNext(q,100,-1,0)
        if e:
            events = events + e
        else:
            break
    return events

def ParseEvents(events):
    for event in events:
        xml = win32evtlog.EvtRender(event,1)
        root = ET.fromstring(xml)
        path = './{*}UserData/{*}ProcessCreate/{*}'
        name = root.findall(path+'Commandline')[0].text
        pid = root.findall(path+'CreatedProcessId')[0].text
        print("Process %s launched with PID %s" % (name,pid))

events = GetEventLogs()
ParseEvents(events)