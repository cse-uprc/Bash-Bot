# Work with Python 3.6
import discord
import json
import io
import os
import logger
from discord.ext import commands
from discord import File

with open('keys.json') as json_file:  
    data = json.load(json_file)
    TOKEN = data['discordKey']

logger = logger.Logger('app.log')

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


#####################
# Commands
#####################

@client.command(name='download')
async def download(ctx, *args:str):
    logger.log('called download')
    attachment = ctx.message.attachments[0]
    buffer = io.BytesIO()
    await attachment.save(buffer)
    try:
        if len(args)>0:
            filePath = args[0]
        else:
            filePath = attachment.filename
        logger.log('Filepath defined: {0}'.format(filePath))

        with open(filePath, 'wb') as f:
            bufferSize=16384
            while True:
                buf = buffer.read(bufferSize)
                if not buf:
                    break
                f.write(buf)
        logger.log('File Downloaded: {0}'.format(filePath))
        msg = 'Attachment Downloaded'
    
    except Exception as e:
        logger.log('Download Failed - {}'.format(str(e)))
        msg = 'Download Fail'
     
    await ctx.send(msg)

@client.command(name='upload')
async def upload(ctx, *args:str):
    logger.log('called upload')
    try:
        filePath = args[0]
        logger.log('Filepath defined: {0}'.format(filePath))
        with open(filePath,'rb') as f:
            await ctx.send(file=File(f,filePath))
        logger.log("Upload successful: {0}".format(filePath))
    except Exception as e:
        await ctx.send('Upload Fail')
        logger.log("Upload Fail {0}".format(str(e)))
    
@client.command(name='hello')
async def hello(ctx):
    logger.log('called hello')
    msg = 'Hello {0.author.mention}'.format(ctx)
    await ctx.send(msg)
    
#####################
# Global
#####################

client.run(TOKEN)
