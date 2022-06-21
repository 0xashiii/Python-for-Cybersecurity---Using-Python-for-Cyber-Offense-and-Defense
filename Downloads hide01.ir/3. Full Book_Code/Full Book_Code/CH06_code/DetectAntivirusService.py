import winreg

av_list = ["MBAM"]
reghive = winreg.HKEY_LOCAL_MACHINE
regpath = "SYSTEM\CurrentControlSet\Services"
try: 
    key = winreg.OpenKey(reghive,regpath,0,access=winreg.KEY_READ)
    numKeys = winreg.QueryInfoKey(key)[0]
    for i in range(numKeys):
        subkey = winreg.EnumKey(key,i)
        for name in av_list:
            if name in subkey:
                subPath = "%s\\%s" % (regpath,subkey)
                k = winreg.OpenKey(reghive,subPath,0,winreg.KEY_READ)
                numVals = winreg.QueryInfoKey(k)[1]
                for j in range(numVals):
                    val = winreg.EnumValue(k,j)
                    if val[0] == "Start" and val[1] == 2:
                        print("Service %s set to run automatically" % subkey)
except Exception as e:
    print(e)