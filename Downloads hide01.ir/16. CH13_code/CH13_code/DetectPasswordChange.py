import datetime,platform, subprocess

def QueryEventLog(eventID):
    server = "localhost"
    logtype = "Security"
    flags = win32evtlog.EVENTLOG_FORWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    logs = []
    h = win32evtlog.OpenEventLog(server,logtype)
    while True:
        events = win32evtlog.ReadEventLog(h,flags,0)
        if events:
            for event in events:
                if event.EventID == eventID:
                    logs.append(event)
        else:
            break
    return logs

def checkWindowsPasswordChange():
    events = QueryEventLog(4724)
    for event in events:
        changed = event.StringInserts[0]
        changer = event.StringInserts[4]
        time = event.TimeGenerated
        print("Password of %s changed by %s at %s" % (changed,changer,time))

def compareDates(date1,date2):
    x = [int(x) for x in date1.split("/")]
    d1 = datetime.datetime(x[2],x[0],x[1])
    x = [int(x) for x in date2.split("/")]
    d2 = datetime.datetime(x[2],x[0],x[1])
    return d2 >= d1

threshold = "01/01/2021"
def checkLinuxPasswordChange():
    import pwd, grp
    for p in pwd.getpwall():
        user = p[0]
        results = subprocess.check_output(["passwd",user,"-S"]).decode("utf-8")
        date = results.split(" ")[2]
        if compareDates(threshold,date):
            print("Password of %s changed on %s"%(user,date))


if platform.system() == "Windows":
    import win32evtlog
    checkWindowsPasswordChange()
else:
    checkLinuxPasswordChange()
