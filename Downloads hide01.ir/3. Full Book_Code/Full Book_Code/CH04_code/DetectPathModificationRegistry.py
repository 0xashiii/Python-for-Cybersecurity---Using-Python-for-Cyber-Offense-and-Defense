import filetime,winreg
from datetime import datetime,timedelta

delta = timedelta(weeks=2)
t = filetime.from_datetime(datetime.now()-delta)
def checkTimeDelta(time):
    if t<time:
        return True
    else:
        return False

def checkPath(hive,hivename,regpath):
    try:
        key = winreg.OpenKey(hive,regpath,access=winreg.KEY_READ)
        result = winreg.QueryInfoKey(key)
        if checkTimeDelta(result[2]):
            print("Path at %s\\%s has potentially been modified. Current Path:" % (hivename,regpath))
            val = winreg.QueryValueEx(key,"Path")[0]
            for v in val.split(";"):
                print("\t%s" % v)
    except Exception as e:
        return

def checkPaths():
    # Check SYSTEM Path
    checkPath(winreg.HKEY_LOCAL_MACHINE,"HKLM","SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
    
    # Check Current User Path
    checkPath(winreg.HKEY_CURRENT_USER,"HKCU","Environment")
    
    # Check User Paths
    try:
        numUsers = winreg.QueryInfoKey(winreg.HKEY_USERS)[0]
        for i in range(numUsers):
            userKey = winreg.EnumKey(winreg.HKEY_USERS,i)
            regPath = "%s\\%s" % (userKey,"Environment")
            checkPath(winreg.HKEY_USERS,"HKU",regPath)
    except Exception as e:
        return

checkPaths()