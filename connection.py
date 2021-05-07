import os

import discord
import requests as requests
#import dotenv

import os

import discord

def OtworzPlik (nazwa):
    try:
        zawartosc = []
        for line in open(nazwa, 'r'):
            zawartosc.append(line)
        assert zawartosc != [], 'puste odczyt z pliku'
        return zawartosc
    except IOError:
        print('\n \n Błąd otwarcia pliku \n \n')



TOKEN = OtworzPlik("Token.env")
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$dzialaj'):
        await message.channel.send('Kurwa dzialam')
    if message.content.startswith('$postac'):
        try:
            if str(message.attachments) == "[]":  # Checks if there is an attachment on the message
                return
            else:  # If there is it gets the filename from message.attachments
                split_v1 = str(message.attachments).split("filename='")[1]
                filename = str(split_v1).split("' ")[0]
                if filename.endswith(".ods"):  # Checks if it is a .csv file
                    await message.attachments[0].save(fp="postacie/{}".format(filename))
            await message.channel.send('ładuje')
        except Exception:
            await message.channel.send('cos nie pykło')
    if message.content.startswith('$oddawaj'):
        try:
            with open('./postacie/Karta-do-TG-v18.ods', 'rb') as fp:
                await message.channel.send(file=discord.File(fp, 'Karta-do-TG-v18.ods'))
        except Exception:
            await message.channel.send('coś nie pykło')

client.run(TOKEN[0])