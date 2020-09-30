import requests
import time
import notification
import modulparser

def read_file(addr):
    with open(addr) as f:
        return f.read()

name = read_file("name.stine").replace("\n", "")
passwort = read_file("passwort.stine").replace("\n", "")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
"Cache-Control": "max-age=0",
"Connection": "keep-alive",
"Content-Length": "220",
"Content-Type": "application/x-www-form-urlencoded",
"Cookie": "cnsc=0;",
"Host": "www.stine.uni-hamburg.de",
"Origin": "https://www.stine.uni-hamburg.de",
"Referer": "https://www.stine.uni-hamburg.de/",
"Upgrade-Insecure-Requests": "1"
}

payload = {'usrname': name,
'pass':passwort,
"APPNAME": "CampusNet",
"PRGNAME": "LOGINCHECK",
"ARGUMENTS": "clino,usrname,pass,menuno,menu_type,browser,platform",
"clino": "000000000000001",
"menuno": "000265",
"menu_type": "classic",
"browser":"",
"platform":""
}


url = "https://www.stine.uni-hamburg.de/scripts/mgrqispi.dll"

SEND_GRADES = False
SEND_BESTANDEN = False

# Hab vergessen, was/wie das tut
# Es tauscht das letzte Komma gegen ein und aus
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def parse_session_arguments(refval):
    split = refval.split("-N")
    return (split[1][:-1], split[2][:-1])

def bestandenstring(grade):
    return "durchgefallen" if grade=="5,0" else "bestanden"

def handleChange(old, new, gradedict):
    difference_set = set(new) - set(old)
    verb = "ist"
    message = ""

    for x in difference_set:
        gradestring = f" ({gradedict[x]})" if SEND_GRADES else ""
        gradestring = f" ({bestandenstring(gradedict[x])})" if not SEND_GRADES and SEND_BESTANDEN else gradestring
        message += f"{x}{gradestring}, "
    message = message[:-2]

    if len(difference_set) > 1:
        verb = "sind"
        message = rreplace(message, ", ", " und ", 1)

    message += f" {verb} jetzt online!"
    notification.sendMessage(message)

def main():
    with requests.Session() as s:
        s = requests.Session()
        r = s.post(url, headers=headers, data=payload)

        a,b = parse_session_arguments(r.headers["REFRESH"])

        newurl = f"{url}?APPNAME=CampusNet&PRGNAME=EXAMRESULTS&ARGUMENTS=-N{a},-N{b}"
        r = s.get(newurl)

        r.encoding = "utf-8"
        courses = modulparser.parse_courses(r.text)
        while True:
            # timenow = time.strftime("%H:%M:%S", time.localtime())
            try:
                r = s.get(newurl, timeout = 60)
            except:
                # notification.sendMessage("STiNE timed out :(")
                pass
            # print("reloaded at "+ timenow)
            # print(f"this took {r.elapsed.total_seconds()} seconds")
            r.encoding = "UTF-8"
            new_courses = modulparser.parse_courses(r.text)
            if len(new_courses) != 0 and new_courses != courses:
                handleChange(courses, new_courses, modulparser.parse_all(r.text))
                courses = new_courses
            time.sleep(180)

if __name__ == "__main__":
    main()
    # handleChange(["a","b"],
    # ["a", "b","Bierdonnerstag", "Pizzafreitag", "Saftsamstag"],
    # {"Bierdonnerstag": "2,0", "Pizzafreitag":"1,0", "Saftsamstag":"5,0"})
