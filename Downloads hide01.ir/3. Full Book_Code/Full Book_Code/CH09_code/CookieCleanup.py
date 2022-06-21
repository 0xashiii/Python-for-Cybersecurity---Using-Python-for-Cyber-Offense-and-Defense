import os,sqlite3,time
from datetime import datetime,timedelta

user = "hepos"
profile = "jpb273b6.default-release"
firefoxPath = os.path.join( "C:\\Users",user,"AppData\\Roaming\\Mozilla\\Firefox\\Profiles",profile,"cookies.sqlite")

query = "DELETE FROM moz_cookies WHERE host='.fake.com';"

conn = sqlite3.connect(firefoxPath)
c = conn.cursor()
c.execute(query)
conn.commit()
c.close()