from subprocess import check_output
import re

def checkLastLogin(user):
    res = check_output("net user "+user)
    logon = re.findall("Last logon\s*([^\r\n]+)",res.decode("utf-8"))[0]
    if logon != "Never":
        print("%s last logged in %s" % (user,logon))

decoyAccounts = ["tester","testuser"]
for user in decoyAccounts:
    checkLastLogin(user)