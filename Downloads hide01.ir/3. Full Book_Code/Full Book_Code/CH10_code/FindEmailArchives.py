import glob, os
import glob, os
import glob, os
from zipfile import ZipFile
from sys import platform

def findFiles(extensions):
    files = []
    for ext in extensions:
        if platform == "win32":
            pattern = r"~\**\*."+ext
        else:
            pattern = r"~/**/*."+ext
        pattern = os.path.expanduser(pattern)
        f = glob.glob(pattern,recursive=True)
        if ext in archiveFiles:
            for a in f:
                if searchArchiveFile(a):
                    files.append(a)
        else:
            files += f
    return files

archiveFiles = ["zip"]
def searchArchiveFile(filename):
    try:
        for file in ZipFile(filename,"r").namelist():
            email = True in [file.endswith(ext) for ext in emailFiles]
            if email:
                return True
    except:
        return False
    return False

emailFiles = ["pst","ost"]
extensions = emailFiles+archiveFiles
print("Email archives:")
for f in findFiles(extensions):
    print("\t%s" % f)