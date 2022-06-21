import os,sqlite3,time
from datetime import datetime,timedelta

user = "hepos"
profile = "jpb273b6.default-release"
firefoxPath = os.path.join( "C:\\Users",user,"AppData\\Roaming\\Mozilla\\Firefox\\Profiles",profile,"cookies.sqlite")

def createFakeCookie(name,value,host,path):
    exp = datetime.now()+timedelta(weeks=4)
    expiry = time.mktime(exp.timetuple())
    dt = datetime.now()
    lastAccessed = time.mktime(dt.timetuple())*1e6+dt.microsecond
    creationTime = time.mktime(dt.timetuple())*1e6+dt.microsecond
    query = "INSERT INTO moz_cookies ('name','value','host','path','expiry','lastAccessed','creationTime','isSecure','isHttpOnly','schemeMap') VALUES ('%s','%s','%s','%s','%d','%d','%d','%d','%d','%d');" % (name,value,host,path,expiry,lastAccessed,creationTime,0,0,2)
    
    conn = sqlite3.connect(firefoxPath)
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    c.close()
    return

createFakeCookie("name","ASDF",".fake.com","/")