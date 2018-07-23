import http.client, urllib

def readApplicationData():
	f = open("app.token", "r")
	app = f.read()
	f.close()
	
	f = open("user.token", "r")
	user = f.read()
	f.close()
	return (app, user)
app = readApplicationData()

def sendMessage(message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": app[0],
        "user": app[1],
        "message": message,
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()