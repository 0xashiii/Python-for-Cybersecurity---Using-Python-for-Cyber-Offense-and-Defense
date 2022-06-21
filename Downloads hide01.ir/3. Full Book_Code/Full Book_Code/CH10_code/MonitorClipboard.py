import win32gui, win32api, ctypes
from win32clipboard import GetClipboardOwner
from win32process import GetWindowThreadProcessId
from psutil import Process

allowlist = []
def processEvent(hwnd,msg,wparam,lparam):
    if msg == 0x031D:
        try:
            win = GetClipboardOwner()
            pid = GetWindowThreadProcessId(win)[1]
            p = Process(pid)
            name = p.name()
            if name not in allowlist:
                print("Clipboard modified by %s" % name)
        except:
            print("Clipboard modified by unknown process")

def createWindow():
    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = processEvent
    wc.lpszClassName = 'clipboardListener'
    wc.hInstance = win32api.GetModuleHandle(None)
    class_atom = win32gui.RegisterClass(wc)
    return win32gui.CreateWindow(class_atom, 'clipboardListener', 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)

def setupListener():
    hwnd = createWindow()
    ctypes.windll.user32.AddClipboardFormatListener(hwnd)
    win32gui.PumpMessages()

setupListener()