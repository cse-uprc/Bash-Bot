# Work with Python 3.6

####################
# Imports
####################

import json
import io
import os
import sys

import discord
from discord.ext import commands
from discord import File

import terminal
import logger


#####################
# Global
#####################

with open("keys.json") as json_file:  
    data = json.load(json_file)
    TOKEN = data["discordKey"]

logger = logger.Logger("app.log")
client = commands.Bot(command_prefix = "!")

# CREATE testTerminal for the bash and cwd commands
testTerminal = terminal.Terminal("test1", "/bin/bash")


####################
# Helper methods
####################

def remove_command_prefix(operand: str):
    """ Removes however many characters are necessary to remove the
    command prefix from operand.
    """
    
    newOperand = operand[len(client.command_prefix):len(operand)]
    return newOperand


def parse_command(messageContent: str):
    """ Takes messageContent and splits it into two items.
      0: the command (prefixless) - str
      1: the operands (or an empty string if none are present) - list
    These items are then joined into a list and returned to the
    caller.
    """
    
    splitMessage = messageContent.split(" ")
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
    """ Displays to the console that the client has successfully logged
    in.
    """
    
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")


@client.event
async def on_command(ctx):
    """ Whenever a command is called, we want to log:
      WHO called it
      WHAT they called (which command)
      HOW they called it (what operands)
    IF AND ONLY IF there are operands,
      we want to send to the console and logger said operands.
    """

    splitMessage = parse_command(ctx.message.content)
    command = splitMessage[0]
    operands = splitMessage[1]

    userAction = "{0.author} calls {1}".format(ctx, command)
    if len(operands) > 0:
        userAction = '{0}\n\t\t"{1}"'.format(userAction, " ".join(operands))

    logger.log(userAction)

    
#####################
# Commands
#####################

@client.command(name = "download")
async def download(ctx, *args:str):
    """ Download to the host machine the first attachment provided by
    the user. Said file should be given a destination path, but will
    default if the name is not provided. If the destination is valid,
    then it should start reading the destination into the file 16kb
    at a time, at which point if an exception is not thrown it should
    tell the user and the logger that the attachment has been
    downloaded.
    """
    
    attachment = ctx.message.attachments[0]
    buffer = io.BytesIO()
    await attachment.save(buffer)
    try:
        if len(args)>0:
            filePath = args[0]
        else:
            filePath = attachment.filename
            logger.log("Filepath defined: {0}".format(filePath))

        with open(filePath, "wb") as f:
            bufferSize=16384
            while True:
                buf = buffer.read(bufferSize)
                if not buf:
                    break
                f.write(buf)
        logger.log("File Downloaded: {0}".format(filePath))
        msg = "Attachment Downloaded"
    
    except Exception as e:
        errorMessage = str(e)
        logger.log("Download Failed - {}".format(errorMessage))
        msg = "Download Fail"
     
    await ctx.send(msg)


@client.command(name = "upload")
async def upload(ctx, *args:str):
    """ Upload from the host machine a file at the path specified by
    the user through args. If successful, the machine should be able to
    upload the file and log that it was successful. If there are
    exceptions thrown, clarify to the user that the upload failed and
    give the exception to the host machine in detail.
    """
    
    try:
        filePath = args[0]
        logger.log("Filepath defined: {0}".format(filePath))
        with open(filePath, "rb") as f:
            await ctx.send(file=File(f, filePath))
        logger.log("Upload successful: {0}".format(filePath))
    except Exception as e:
        errorMessage = str(e)
        await ctx.send("Upload Fail")
        logger.log("Upload Fail {0}".format(errorMessage))


@client.command(name = "bash")
async def upload(ctx, *args:str):
    """ Receive a bash command from the discord chat and run in on the
    appropriate bot instance.
    """
    
    try:
        # Turn the tuple of args into a single string
        argsString = " ".join(args)
        
        # Ensure nothing extremely dangerous was attempted
        if "sudo" in argsString:
            raise Exception("CANNOT EXECUTE SUPER USER COMMANDS")

        # Run and Log the command
        output = testTerminal.executeCommand(argsString)
        logger.log("Command executed {0}".format(argsString))
        
        # Check for empty output string
        outStr = ("```{0}```".format(output["outputString"]) if
            len(output["outputString"])>0 else "")
        
        errStr = ("```{0}```".format(output["errorString"]) if
            len(output["errorString"])>0 else "")
 
        # Build message
        msg = (
            "Terminal: {0} \n".format(output["terminalName"])
            + "Current Dir: {0} \n".format(output["currentDirectory"])
            + "Output:{0}\n".format(outStr)
            + "Error:{0}\n".format(errStr)
        )
        
        logger.log(msg)
        await ctx.send(msg)

    except Exception as e:
        # If an exception occured it should be logged and posted to
        # discord
        errorMessage = str(e)    
        msg = "Command Failed {0}".format(errorMessage)
        logger.log(msg)
        await ctx.send(msg)


@client.command(name = "cwd")
async def changeWorkingDirectory(ctx, *args:str):
    """ Change the working directory of the terminal. """
    
    try:
        # The file path should be the first and only argument
        filePath = args[0]
        logger.log("Directory specified {0}".format(filePath))
        # Set the currentDirectory of the terminal instance
        testTerminal.currentDirectory = filePath
        msg = "Terminal Directory set!"
        logger.log(msg)
        await ctx.send(msg)
        
    except Exception as e:
        errorMessage = str(e)
        msg = "Changing Directory Failed {0}".format(errorMessage)
        logger.log(msg)
        await ctx.send(msg)


@client.command(name = "hello")
async def hello(ctx):
    """ Clarifies that the command system is successfully implemented
    and mentions the user while saying hello.
    """
    
    msg = "Hello {0.author.mention}".format(ctx)
    await ctx.send(msg)
    

@client.command(name = "shutdown")
async def shutdown(ctx):
    """ Clarifies to the user that the bot is shutting down. Logs out.
    Tells the host machine that the bot has logged out.
    """
    
    await ctx.send("Shutting down...")
    logger.log("{0.user.name} has logged out.".format(client))
    await client.logout()

    
#####################
# Start the bot
#####################
client.run(TOKEN)
