import os

import discord
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
print(TOKEN[0])
client.run(TOKEN[0])