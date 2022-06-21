import os,re,subprocess

def findADS(d):
    for dirpath,dirnames,filenames in os.walk(d):
        for file in filenames:
            filename = os.path.join(dirpath,file)
            cmd = "Get-Item -path "+ filename + " -stream * "
            cmd += "| Format-Table -Property \"Stream\" -HideTableHeaders"
            results = subprocess.run(["powershell", "-Command", cmd],capture_output=True)
            streams = results.stdout.decode("utf-8").split("\r\n")
            streams = [s.strip() for s in streams]
            streams = [s for s in streams if len(s) > 1]
            if len(streams)> 1:
                print("ADS detected for %s" % filename)
                for s in streams[1:]:
                    print("\t%s" % s)

findADS(".")