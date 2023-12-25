from telethon import TelegramClient, events, errors
from dotenv import load_dotenv
import time
import os
import json
from random import randint

load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
api_name = os.getenv("API_NAME")

api_id = 
api_hash = ''
api_name = ''
client = TelegramClient(api_name, api_id, api_hash)

js = []
berhasil_dikirim = []
gagal_dikirim = []

admin_list = [, ] 

ignore_grup = [-100, -100]

log_grup_id = -100  

async def main():
    global berhasil_dikirim, gagal_dikirim 
    me = await client.get_me()
    
    try:
        await client.send_message(log_grup_id, "Bot sudah menyala")
    except Exception as e:
        print("Gagal mengirim pesan log ke grup. Alasan: ", str(e))

    while True:
        with open("groups.json", 'r') as openfile:
            json_object = json.load(openfile)

        for data in json_object:
            if data['id'] in ignore_grup:
                continue

            with open("message.json", "r") as m:
                msg = json.load(m)
                random_index = randint(0, len(msg) - 1)
                message = msg[random_index]

            try:

                original_msg = await client.get_messages(message['channel'], ids=message['msg_id'])

                await client.send_message(data['id'], original_msg)
                berhasil_dikirim.append({"name": data['name'], "id": data['id']})
                print(data['name'] + " " + str(data['id']) + " pesan berhasil dikirim")
            except Exception as e:
                gagal_dikirim.append({"name": data['name'], "id": data['id']})
                print(data['name'] + " " + str(data['id']) + " gagal mengirim pesan. Alasan: " + str(e))

            time.sleep(3)

        with open("groups.json", "w") as outfile:
            json.dump(js, outfile)

        berhasil_dikirim = []
        gagal_dikirim = []

        print("-- MEMPERBARUI DAFTAR GRUP --\n")
        async for dialog in client.iter_dialogs():
            if str(dialog.id).startswith("-100"):
                dt = {"name": dialog.name, "id": dialog.id}
                js.append(dt)
                print(dialog.name, "memiliki ID", dialog.id)

        print("\nMenunggu loop berikutnya dalam 1 detik")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')

@client.on(events.NewMessage(pattern='/check_berhasil'))
async def check_berhasil(event):
    if event.sender_id in admin_list:
        response = "Daftar grup yang berhasil dikirim:\n\n"
        for grup in berhasil_dikirim:
            line = f"» {grup['name']} ({grup['id']})\n------------------------\n"
            if len(response + line) <= 4096:
                response += line
            else:
                await event.respond(response)
                response = line

        if response:
            await event.respond(response)
    else:
        await event.respond("Anda tidak memiliki izin untuk menggunakan perintah ini.")

@client.on(events.NewMessage(pattern='/check_gagal'))
async def check_gagal(event):
    if event.sender_id in admin_list:
        response = "Daftar grup yang gagal dikirim:\n\n"
        for grup in gagal_dikirim:
            line = f"» {grup['name']} ({grup['id']})\n------------------------\n"
            if len(response + line) <= 4096:
                response += line
            else:
                await event.respond(response)
                response = line

        if response:
            await event.respond(response)
    else:
        await event.respond("Anda tidak memiliki izin untuk menggunakan perintah ini.")

@client.on(events.NewMessage(pattern='/admins'))
async def show_admins(event):
    if event.sender_id in admin_list:
        response = "List admins:\n\n"
        for admin_id in admin_list:
            admin = await client.get_entity(admin_id)
            line = f"» {admin.username} [{admin_id}]\n------------------\n"
            if len(response + line) <= 4096:
                response += line
            else:
                await event.respond(response)
                response = line

        if response:
            await event.respond(response)
    else:
        await event.respond("Anda tidak memiliki izin untuk menggunakan perintah ini.")

@client.on(events.NewMessage(pattern='/help'))
async def show_help(event):
    response = (
        "Hallo, ini adalah userbot auto share pesan ke grup,\n\n"
        "Gunakan /check_berhasil untuk melihat grup mana saja yang berhasil di kirim.\n"
        "Gunakan /check_gagal untuk melihat grup mana saja yang gagal di kirim.\n"
        "Gunakan /admins untuk melihat list admin\n\n"
        "Bot di buat oleh @hentaiiboys."
    )
    await event.respond(response)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    response = "Bot sudah aktif. Gunakan /help untuk melihat panduan penggunaan."
    await event.respond(response)

with client:
    client.loop.run_until_complete(main())
