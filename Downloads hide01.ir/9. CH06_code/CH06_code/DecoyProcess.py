import signal,sys
from setproctitle import setproctitle
from time import sleep

def terminated(signum,frame):
    pass

decoy_name = "notepad"
setproctitle(decoy_name)
signal.signal(signal.SIGTERM,terminated)
signal.signal(signal.SIGINT,terminated)
siginfo = signal.sigwaitinfo({signal.SIGINT,signal.SIGTERM})
with open("terminated.txt","w+") as f:
    f.write("Process terminated by %d\n" % siginfo.si_pid)
sys.exit(0)
