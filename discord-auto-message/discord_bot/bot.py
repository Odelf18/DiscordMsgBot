from http.client import HTTPSConnection
import sys
from json import dumps
from time import sleep
from random import random

file = open("info.txt")
text = file.read().splitlines()

if len(sys.argv) > 1 and sys.argv[1] == "--setall" and input("Configure bot? (y/n)") == "y":
    file.close()
    file = open("info.txt", "w")
    text = []
    text.append(input("User agent: "))
    text.append(input("Discord token: "))
    text.append(input("Discord channel URL: "))
    text.append(input("Discord channel ID: "))

    for parameter in text:
        file.write(parameter + "\n")

    file.close()
    exit()
elif len(sys.argv) > 1 and sys.argv[1] == "--setchannel" and input("Set channel? (y/n)") == "y":
    user_agent = text[0]
    token = text[1]
    text = text[0:2]
    file.close()
    file = open("info.txt", "w")
    text.append(input("Discord channel URL: "))
    text.append(input("Discord channel ID: "))
    for parameter in text:
        file.write(parameter + "\n")

    file.close()
    exit()
elif len(sys.argv) > 1 and sys.argv[1] == "--setauth" and input("Set authentication? (y/n)") == "y":
    channelurl = text[2]
    channelid = text[3]
    text = text[2:4]
    file.close()
    file = open("info.txt", "w")
    text.insert(0, input("Discord token: "))
    text.insert(0, input("User agent: "))
    for parameter in text:
        file.write(parameter + "\n")

    file.close()
    exit()
elif len(sys.argv) > 1 and sys.argv[1] == "--help":
    print("Showing help for discord-auto-message")
    print("Usage:")
    print("  'python3 bot.py'               :  Runs the autotyper. Fill in the messages and wait times.")
    print("  'python3 bot.py --setall'      :  Configure all settings.")
    print("  'python3 bot.py --setchannel'  :  Set channel to send message to. Includes Channel ID and Channel URL")
    print("  'python3 bot.py --setauth'     :  Set authentication. Includes User Token and User Agent")
    print("  'python3 bot.py --help'        :  Show help")
    exit()

if len(text) != 4:
    print("An error was found inside the user information file. Run the script with the 'Set All' flag ('python3 bot.py --setall') to reconfigure.")
    exit()
    
if len(sys.argv) > 1:
    exit()
    
header_data = {
    "content-type": "application/json",
    "user-agent": text[0],
    "authorization": text[1],
    "host": "discordapp.com",
    "referrer": text[2]
}

print("Messages will be sent to " + header_data["referrer"] + ".")

def get_connection():
    return HTTPSConnection("discordapp.com", 443)


def send_message(conn, channel_id, message_data):
    try:
        conn.request("POST", f"/api/v6/channels/{channel_id}/messages", message_data, header_data)
        resp = conn.getresponse()

        if 199 < resp.status < 300:
            print("Message sent!")
            pass

        else:
            sys.stderr.write(f"Received HTTP {resp.status}: {resp.reason}\n")
            pass

    except:
        sys.stderr.write("Failed to send_message\n")
        for key in header_data:
            print(key + ": " + header_data[key])


def main(msg):
    message_data = {
        "content": msg,
        "tts": "false",
    }

    send_message(get_connection(), text[3], dumps(message_data))


my_list = [line.split(',') for line in open("SomeFile.txt")]
flat_list = [item for sublist in my_list for item in sublist]

j=0
if __name__ == '__main__':
    #message = input("Message to send: Just type somtething we dont care of it")
    messages = int(input("Amount of messages: "))
    main_wait = int(input("Seconds between messages: "))
    human_margin = int(input("Human error margin in seconds: "))
    loop = input("Infinity loop? (y/n)")
    print()
    
    
    if loop == 'y':
        messages =  100000

    for i in range(0,messages):
        main(flat_list[j])
        print("Estimated time to complete: " + str((messages-i) * (human_margin // 2 + main_wait) // 60) + " minutes.")
        print("Iteration " + str(i) + " complete.\n")
        sleep(main_wait)
        sleep(random()*human_margin)
        if j == len(flat_list)-1:
            j=0
        else:
            j+=1
    

    print("Session complete! " + str(messages) + " messages sent.")
