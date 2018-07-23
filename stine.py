from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import urllib.request
import time

def readAccountData():
	f = open("name.stine", "r")
	name = f.read()
	f.close()
	
	f = open("passwort.stine", "r")
	passwort = f.read()
	f.close()
	return (name, passwort)

account = readAccountData()
options = Options()
#options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://www.stine.uni-hamburg.de/")

driver.find_element_by_name("usrname").send_keys(account[0])
driver.find_element_by_name("pass").send_keys(account[1])
driver.find_element_by_id("logIn_btn").click()
driver.find_element_by_partial_link_text("Studium").click()
driver.find_element_by_partial_link_text("Prüfungsergebnisse").click()


while True:
	driver.refresh()
	entries = driver.find_element_by_class_name("tbdata")
	time.sleep(300)


		
