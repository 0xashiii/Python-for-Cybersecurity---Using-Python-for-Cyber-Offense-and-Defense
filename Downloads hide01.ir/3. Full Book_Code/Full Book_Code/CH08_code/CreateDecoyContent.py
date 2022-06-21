import pathlib

def getTimestamps(filename):
    fname = pathlib.Path(filename)
    stats = fname.stat()
    if not fname.exists(): # File deleted
        return []
    return(stats.st_ctime,stats.st_mtime,stats.st_atime)

def createDecoyFiles(filenames):
    with open("decoys.txt","w") as f:
        for file in filenames:
            (ctime, mtime, atime) = getTimestamps(file)
            f.write("%s,%s,%s,%s\n" % (file,ctime,mtime,atime))

decoys = [r"Documents\clients.csv",r"Documents\Resume.docx"]
createDecoyFiles(decoys)
