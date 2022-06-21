import winreg

def checkRegAutorun(hive,path):
    autoruns = []
    try:
        key = winreg.OpenKey(hive,path)
        numValues = winreg.QueryInfoKey(key)[1]
    except:
        return []
    for i in range(numValues):
        try:
            [name,data,_] = winreg.EnumValue(key,i)
        except:
            continue
        if len(name) > 0:
            autoruns.append([name,data])
    return autoruns

def printResults(hive,path,autoruns):
    print("Autoruns detected in %s\\%s" % (hive,path))
    for autorun in autoruns:
        print("\t%s: %s" % (autorun[0],autorun[1]))
    print()

hives = {
    "HKCU": winreg.HKEY_CURRENT_USER,
    "HKLM": winreg.HKEY_LOCAL_MACHINE}
paths = ["SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"]
def checkAutoruns():
    for hive in hives:
        for path in paths:
            autoruns = checkRegAutorun(hives[hive],path)
            if autoruns:
                printResults(hive,path,autoruns)
    
    # Check HKU hive
    numKeys = winreg.QueryInfoKey(winreg.HKEY_USERS)[0]
    for i in range(numKeys):
        subKey = winreg.EnumKey(winreg.HKEY_USERS,i)
        for path in paths:
            subpath = "%s\\%s" % (subKey,path)
            autoruns = checkRegAutorun(winreg.HKEY_USERS,subpath)
            if autoruns:
                printResults("HKU",subpath,autoruns)

checkAutoruns()