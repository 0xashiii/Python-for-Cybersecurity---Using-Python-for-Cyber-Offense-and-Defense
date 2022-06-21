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

def DetectAdministratorLogin():
    events = QueryEventLog(4672)
    for event in events:
        if event.StringInserts[0].startswith("S-1-5-21"):
            print("Login attempt by %s at %s" % (event.StringInserts[1],event.TimeGenerated))

DetectAdministratorLogin()