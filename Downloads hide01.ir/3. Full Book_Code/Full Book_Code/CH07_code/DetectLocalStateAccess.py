import win32evtlog

server = "localhost"
logtype = "Security"
flags = win32evtlog.EVENTLOG_FORWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ

def QueryEventLog(eventID, filename=None):
    logs = []
    if not filename:
        h = win32evtlog.OpenEventLog(server,logtype)
    else:
        h = win32evtlog.OpenBackupEventLog(server,filename)
    while True:
        events = win32evtlog.ReadEventLog(h,flags,0)
        if events:
            for event in events:
                if event.EventID == eventID:
                    logs.append(event)
        else:
            break
    return logs

def DetectLocalStateAccess():
    events = QueryEventLog(4663)
    for event in events:
        if event.StringInserts[6].endswith("Local State"):
            print("%s (PID %s) accessed Local State at %s" % (event.StringInserts[11],event.StringInserts[10],event.TimeGenerated))

DetectLocalStateAccess()