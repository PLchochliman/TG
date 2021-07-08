import os

import discord
import requests as requests
#import dotenv

import os

import discord
import FilesMenagment as FilesMenagment



TOKEN = FilesMenagment.OtworzPlik("Token.env")
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if "/" or "\\" or "DROP" in message.content:
        await message.channel.send('hakerze won')
    if message.content.startswith('$dzialaj'):
        await message.channel.send('dzialam')
    if message.content.startswith('$postac'):
        try:
            if str(message.attachments) == "[]":  # Checks if there is an attachment on the message
                await message.channel.send('nie mam pliku(załącz go, a w treści wiadomości napisz $postać)')
                return
            else:  # If there is it gets the filename from message.attachments
                split_v1 = str(message.attachments).split("filename='")[1]
                filename = str(split_v1).split("' ")[0]
                if filename.endswith(".ods"):  # Checks if it is a .csv file
                    await message.attachments[0].save(fp="postacie/{}".format(filename))
            await message.channel.send('ładuje')
        except Exception:
            await message.channel.send('cos pykło')
    if message.content.startswith('$zwroc'):
        try:
            name_of_file = message.content.split()
            name_of_file = name_of_file[1]
            with open('./postacie/'+ name_of_file, 'rb') as fp:
                await message.channel.send(file=discord.File(fp, name_of_file))
        except IOError:
            await message.channel.send('Nie mam takiego pliku')
        except Exception:
            await message.channel.send('coś nie pykło')

client.run(TOKEN[0])