import psutil,os,signal

av_list = ["notepad"]

# Find and Kill Processes
for process in psutil.process_iter():
    for name in av_list:
        if name in process.name():
            os.kill(process.pid,signal.SIGTERM)
