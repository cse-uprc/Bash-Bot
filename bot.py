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

####################
# Helper methods
####################

def remove_command_prefix(operand: str):
    newOperand = operand[len(client.command_prefix):len(operand)]
    return newOperand

def parse_command(messageContent: str):
    splitMessage = messageContent.split(' ')
    command = remove_command_prefix(splitMessage[0])
    operands = ""
    if len(splitMessage) > 1:
        operands = splitMessage[1:len(splitMessage)]
    return [command, operands]

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
async def on_command(ctx):
    splitMessage = parse_command(ctx.message.content)
    command = splitMessage[0]
    operands = splitMessage[1]

    userAction = "{0.author} calls {1}".format(ctx, command)
    if len(operands) > 0:
        userAction = '{0}\n\t\t"{1}"'.format(userAction, ' '.join(operands))

    logger.log(userAction)

#####################
# Commands
#####################

@client.command(name='download')
async def download(ctx, *args:str):
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
    try:
        filePath = args[0]
        logger.log('Filepath defined: {0}'.format(filePath))
        with open(filePath,'rb') as f:
            await ctx.send(file=File(f,filePath))
        logger.log("Upload successful: {0}".format(filePath))
    except Exception as e:
        errorMessage = str(e)
        await ctx.send('Upload Fail')
        logger.log("Upload Fail {0}".format(errorMessage))
    
@client.command(name='hello')
async def hello(ctx):
    msg = 'Hello {0.author.mention}'.format(ctx)
    await ctx.send(msg)
    
@client.command(name='ping')
async def ping(ctx):
    await ctx.send("Pong!")

@client.command(name='shutdown')
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    await client.logout() 

#####################
# Global
#####################

client.run(TOKEN)
