# Work with Python 3.6
import discord
import json
import io
from discord import File

with open('keys.json') as json_file:  
    data = json.load(json_file)
    TOKEN = data['discordKey']

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        # we do not want the bot to reply to itself
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    elif message.content.startswith('!download'):
        attachment = message.attachments[0]
        buffer = io.BytesIO()
        await attachment.save(buffer)
        f = open(attachment.filename,'wb')
        f.close()
        msg = 'Attachment Downloaded'
        await message.channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
