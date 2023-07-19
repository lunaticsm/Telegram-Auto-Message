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
client = TelegramClient(api_name, api_id, api_hash)

async def main():
    while True:
        try:
            with open("groups.json", 'r') as openfile:
                json_object = json.load(openfile)

            with open("message.json", "r") as m:
                msg = json.load(m)

            for data in json_object:
                random_index = randint(0, len(msg) - 1)
                message = msg[random_index]

                await client.forward_messages(data['id'], message['msg_id'], message['channel'])
                print(f"{data['name']} {data['id']} send successfully")

                time.sleep(10)

            os.system('cls' if os.name == 'nt' else 'clear')
            js = []

            print("-- UPDATE GRUP LIST --\n")
            async for dialog in client.iter_dialogs():
                if str(dialog.id).startswith("-100"):
                    dt = {"name": dialog.name, "id": dialog.id}
                    js.append(dt)
                    print(dialog.name, "has ID", dialog.id)

            with open("groups.json", "w") as outfile:
                json.dump(js, outfile)

            print("\nwaiting next loop 10 seconds")
            time.sleep(10)
            os.system('cls' if os.name == 'nt' else 'clear')

        except Exception as e:
            print("Error:", e)

with client:
    client.loop.run_until_complete(main())
