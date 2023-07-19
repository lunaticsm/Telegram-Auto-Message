from telethon import TelegramClient, errors
from dotenv import load_dotenv
import time
import os
import json
from random import randint

# API details
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
api_name = os.getenv("API_NAME")
# Account connection
api_id = 0
api_hash = 'API_HASH'
api_name = 'API_NAME'
client = TelegramClient(api_name, api_id, api_hash)


async def main():
    me = await client.get_me()
    # Read message from file and send to a list of scraped groups

    while True:

        with open("groups.json", 'r') as openfile:
            json_object = json.load(openfile)

        for data in json_object:

            with open("message.json", "r") as m:
                msg = json.load(m)
                random_index = randint(0, len(msg) - 1)
                message = msg[random_index]

            try:
                # Get the original message entity to be forwarded
                original_msg = await client.get_messages(message['channel'], ids=message['msg_id'])

                # Copy the original message to the target group
                await client.send_message(data['id'], original_msg)

                print(data['name'] + " " + str(data['id']) + " message copied successfully")
            except Exception as e:
                print(data['name'] + " " + str(data['id']) + " failed to copy message. Reason: " + str(e))

            time.sleep(10)

        os.system('cls' if os.name == 'nt' else 'clear')
        js = []

        print("-- UPDATE GROUP LIST --\n")
        async for dialog in client.iter_dialogs():
            if str(dialog.id).startswith("-100"):
                dt = {"name": dialog.name, "id": dialog.id}
                js.append(dt)
                print(dialog.name, "has ID", dialog.id)

        with open("groups.json", "w") as outfile:
            json.dump(js, outfile)

        print("\nWaiting for the next loop in 10 seconds")
        time.sleep(10)
        os.system('cls' if os.name == 'nt' else 'clear')


with client:
    client.loop.run_until_complete(main())
