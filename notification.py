import telegram_send

def sendMessage(message):
    telegram_send.send(messages=[message])

if __name__ == "__main__":
    sendMessage("Hallo Welt!")