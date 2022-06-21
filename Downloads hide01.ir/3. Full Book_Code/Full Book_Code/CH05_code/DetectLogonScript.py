import winreg

def checkValues(key,keyword):
    numValues = winreg.QueryInfoKey(key)[1]
    for i in range(numValues):
        try:
            values = winreg.EnumValue(key,i)
            if values[0] == keyword:
                return values[1]
        except Exception as e:
            continue
    return None
    
def checkLogonScripts():
    try:
        numUsers = winreg.QueryInfoKey(winreg.HKEY_USERS)[0]
    except Exception as e:
        print(e)
        return
    for i in range(numUsers):
        try:
            userKey = winreg.EnumKey(winreg.HKEY_USERS,i)
            regPath = "%s\\%s" % (userKey,"Environment")
            key = winreg.OpenKey(winreg.HKEY_USERS,regPath)
            script = checkValues(key,"UserInitMprLogonScript")
            if script:
                print("Logon script detected at HKU\\%s\\Environment:\n\t%s" % (userKey,script))
        except:
            continue
checkLogonScripts()