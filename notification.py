import subprocess

def sendMessage(message):
    subprocess.call(["telegram-send", message])

if __name__ == "__main__":
    sendMessage("Hallo Welt!")