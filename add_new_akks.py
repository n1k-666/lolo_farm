import asyncio
import json
import time

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
import openpyxl
from ASF import IPC

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

bot = Bot(token= config["tg_token_add"])
dp = Dispatcher()


@dp.message()
async def alo(message: Message):

    if "обавить" in message.text:
        await add_akks(message.text)
        await create_json(message.text)
        await message.answer("готово")
    elif "ерекличка" in message.text:
        time.sleep(2)
        await message.answer("я не сплю")
    elif "грать" in message.text:
        async with IPC(ipc='http://127.0.0.1:1242', password='YOUR IPC PASSWORD') as asf:
            cmd = "play ASF 730, 570"
            await command(asf, cmd)
        await message.answer("аккаунты играют в 730, 570")
    elif "кастом" in message.text:
        async with IPC(ipc='http://127.0.0.1:1242', password='YOUR IPC PASSWORD') as asf:
            cmd = "play ASF 730, 570"
            await command(asf, cmd)
        await message.answer("настроено аккаунтов: ")



async def command(asf, cmd):
    return await asf.Api.Command.post(body={
        'Command': cmd
    })


async def main():
    await dp.start_polling(bot)
    print(1)


async def add_akks(messege):
    login = 0
    kol_igr = 1
    parol = 2
    pochta = 3
    parol_pochta = 4

    lines = messege.split("\n")
    lines.pop(0)
    for nomer_stroki in range(len(lines)):
        lines[nomer_stroki] = lines[nomer_stroki].split(":")
    print(lines)
    book = openpyxl.load_workbook("done.xlsx")
    sheet = book.active
    proverka_na_pustotu = 0
    for nomer_akka in range(len(lines)):
        nomer_stroki = nomer_akka + proverka_na_pustotu
        while sheet[nomer_stroki + 1][login].value != None:
            proverka_na_pustotu += 1
            nomer_stroki = nomer_akka + proverka_na_pustotu
        sheet[nomer_stroki + 1][login].value = lines[nomer_akka][0]
        sheet[nomer_stroki + 1][kol_igr].value = 0
        sheet[nomer_stroki + 1][parol].value = lines[nomer_akka][1]
        sheet[nomer_stroki + 1][pochta].value = lines[nomer_akka][2]
        sheet[nomer_stroki + 1][parol_pochta].value = lines[nomer_akka][3]
    book.save("done.xlsx")
    book.close()


async def create_json(messege):
    print(1)
    login = 0
    parol = 1
    lines = messege.split("\n")
    lines.pop(0)
    shab = """{
      "AcceptGifts": true,
      "Enabled": true,
      "SteamLogin": "112233",
      "SteamPassword": "sssdeded"
    }"""
    print(2)
    for nomer_stroki in range(len(lines)):
        lines[nomer_stroki] = lines[nomer_stroki].split(":")
    print(lines)
    for nomer_akka in range(len(lines)):
        done = shab.replace("112233", lines[nomer_akka][login])
        done = done.replace("sssdeded", lines[nomer_akka][parol])
        data = json.loads(done)
        with open(f'asf/config/{lines[nomer_akka][login]}.json', "w") as file:
            json.dump(data, file, indent=2)


asyncio.run(main())
