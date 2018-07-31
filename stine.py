import os
import urllib.request
import time
import notification as notify
from urllib.request import url2pathname
import mechanicalsoup
from bs4 import BeautifulSoup

def readAccountData():
	f = open("name.stine", "r")
	name = f.read()
	f.close()
	
	f = open("passwort.stine", "r")
	passwort = f.read()
	f.close()
	return (name, passwort)

def deuglyfy(string):
	index = string.find("<br")
	string = string[:index]
	modulname = string.strip().replace("&nbsp;", "").replace("\t", "")
	modulname = modulname.replace("\n", "").replace("  ","")
	return modulname

def handleChange(entry):
	modulname = deuglyfy(entry)
	message = modulname +" ist jetzt online!"
	notify.sendMessage(message)

def getEntries(browser):
	soup = browser.get_current_page()
	trs = soup.find_all("tr", class_ = "tbdata")
	# remove <tr> by searching for td and "<td>\n" by slicing
	return [str(x.find("td"))[5:] for x in trs]

entrynumber = -1
account = readAccountData()

browser = mechanicalsoup.StatefulBrowser()
browser.open("https://www.stine.uni-hamburg.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=EXTERNALPAGES&ARGUMENTS=-N000000000000001,-N000265,-Astartseite")

form = browser.select_form("#cn_loginForm")
form["usrname"] = account[0]
form["pass"] = account[1]
r = browser.submit_selected()
print(r.text)
browser.launch_browser()

browser.follow_link(browser.find_link(link_text="Studium"))
browser.follow_link(browser.find_link(link_text="Prüfungsergebnisse"))

entries = getEntries(browser)
entrynumber = len(entries)

while True:
	
	browser.refresh()
	entries = getEntries(browser)

	if entrynumber < len(entries):
		handleChange(entries[entrynumber])
	entrynumber = len(entries)
	time.sleep(300)
		
