# Work with Python 3.6
import discord
import json
import io
from discord import File

with open('keys.json') as json_file:  
    data = json.load(json_file)
    TOKEN = data['discordKey']

client = commands.Bot(command_prefix = '!')

#####################
# Events
#####################

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        # we do not want the bot to reply to itself
        return
    # Make it clear that we can add things later, but do not wish to currently.
    pass

#####################
# Commands
#####################
        
@client.command()
    async def download(message):
        attachment = message.attachments[0]
        buffer = io.BytesIO()
        await attachment.save(buffer)
        f = open(attachment.filename,'wb')
        f.close()
        msg = 'Attachment Downloaded'
        await message.channel.send(msg)
        
@client.command()
    async def hello(message):
        msg = 'Hello {0.author.mention}'.format(ctx.message)
        await message.channel.send(msg)
        
#####################
# Global
#####################

client.run(TOKEN)
