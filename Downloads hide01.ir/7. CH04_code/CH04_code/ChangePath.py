import os, winreg

def readPathValue(reghive,regpath):
    key = winreg.OpenKey(reghive,regpath,access=winreg.KEY_READ)
    numValues = numValues = winreg.QueryInfoKey(key)[1]
    for i in range(numValues):
        val = winreg.EnumValue(key,i)
        if val[0] == "Path":
            return val[1]

def editPathValue(reghive,regpath,targetdir):
    path = readPathValue(reghive,regpath)
    if targetdir in path:
        return
    newpath = ";".join([targetdir, path])
    key = winreg.OpenKey(reghive,regpath,access=winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key,"Path",0,winreg.REG_EXPAND_SZ,newpath)
    
# Modify user path
reghive = winreg.HKEY_CURRENT_USER
regpath = "Environment"
targetdir = os.getcwd()
editPathValue(reghive,regpath,targetdir)

# Modify SYSTEM path
#reghive = winreg.HKEY_LOCAL_MACHINE
#regpath = "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
#editPathValue(reghive,regpath,targetdir)
