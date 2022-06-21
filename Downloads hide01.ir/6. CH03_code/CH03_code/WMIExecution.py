import subprocess,wmi

def WMIProcessCreation(name):
    c = wmi.WMI()
    processID,returnValue = c.Win32_Process.Create(CommandLine=name)
    print("Process %s created with PID %d" %(name,processID))

def PSProcessCreation(name):
    command = ["powershell","& { invoke-wmimethod win32_process -name create -argumentlist notepad.exe | select ProcessId | % { $_.ProcessId } | Write-Host }"]
    p = subprocess.run(command,shell=True,capture_output=True)
    if p.returncode == 0:
        print("Process %s created with PowerShell, PID %s" % (name, p.stdout.decode("utf-8")))

command = "notepad.exe"
WMIProcessCreation(command)
PSProcessCreation(command)