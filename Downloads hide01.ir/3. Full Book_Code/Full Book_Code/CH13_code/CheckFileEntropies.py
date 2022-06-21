from pandas import Series
from scipy.stats import entropy
from pathlib import Path

def calcEntropy(data):
    s = Series(data)
    counts = s.value_counts()
    return entropy(counts)

def calcFileEntropy(filename):
    with open(filename,"rb") as f:
        b = list(f.read())
    fileLen = len(b)
    e = calcEntropy(b)
    return e

def getFiles(directory,ext):
    paths = list(Path(directory).rglob("*"+ext+"*"))
    return paths

threshold = 0
def checkFiles(directory,ext):
    files = getFiles(directory,ext)
    for f in files:
        entropy = calcFileEntropy(f)
        if entropy > threshold:
            print("%s is potentially encrypted (entropy %f)" % (f,entropy))

directory = "Documents"
ext = ".docx"
checkFiles(directory,ext)