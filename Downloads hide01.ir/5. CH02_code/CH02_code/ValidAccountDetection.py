import win32evtlog

server = "localhost"
logtype = "Security"
flags = win32evtlog.EVENTLOG_FORWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ

def QueryEventLog(eventID):
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

def DetectBruteForce():
    failures = {}
    events = QueryEventLog(4625)
    for event in events:
        account = event.StringInserts[5]
        if account in failures:
            failures[account] += 1
        else:
            failures[account] = 1
    for account in failures:
        print("%s: %s failed logins" % (account,failures[account]))

def CheckDefaultAccounts():
    with open("defaults.txt","r") as f:
        defaults = [[x for x in line.split(' ')][0] for line in f]
    with open("allowlist.txt","r") as f:
        allowed = f.read().splitlines()

    events = QueryEventLog(4624)
    for event in events:
        if event.StringInserts[8] == ["10","3"]:
            if event.StringInserts[5] in defaults:
                if event.StringInserts[18] not in allowed:
                    print("Unauthorized login to %s from %s" % (event.StringInserts[5],event.StringInserts[18]))

DetectBruteForce()
CheckDefaultAccounts()

