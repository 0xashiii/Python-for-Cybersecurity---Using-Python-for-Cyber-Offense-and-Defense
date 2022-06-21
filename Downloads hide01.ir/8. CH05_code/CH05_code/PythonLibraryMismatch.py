import sys,os

def getImports():
    before = list(sys.modules.keys())
    import test
    after = list(sys.modules.keys())
    new = [m for m in after if not m in before]
    modules = set([n.split(".")[0] for n in new])
    return modules

def findModules(imports):
    mods = {}
    path = sys.path
    path[0] = os.getcwd()
    for p in path:
        for r,d,f in os.walk(p):
            for i in imports:
                files = [file for file in f if file.startswith(i+".py")]
                for file in files:
                    filepath = os.path.join(r,file)
                    if i in mods:
                        mods[i].append(filepath)
                    else:
                        mods[i] = [filepath]
                if i in d and os.path.isfile("\\".join([r,i,"__init__.py"])):
                    filepath = os.path.join(r,i)
                    if i in mods:
                        mods[i].append(filepath)
                    else:
                        mods[i] = [filepath]
    return mods

imports = getImports()
modules = findModules(imports)
for m in modules:
    if len(modules[m]) > 1:
        print("Duplicate versions of %s found:"%m)
        for x in set(modules[m]):
            print("\t%s" %x)