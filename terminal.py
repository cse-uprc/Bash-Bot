import subprocess
import os
from pathlib import Path


class Terminal:
    # Class to represent an instance of a terminal which is initiated
    # by a discord user via the discord bot

    def __init__(self, name, terminalPath, directoryPath=str(Path.home())):
        # Object constructor

        # The name of the terminal instance (supplied by the user)
        self.name = name

        # The path of the actual terminal program to be run via
        # discord bot
        self.terminalPath = terminalPath
        
        # The current working directory that the user is in (starts
        # in the home directory)
        self.currentDirectory = directoryPath
    
    def executeCommand(self, command):
        # Execute a bash terminal command (passed as an argument to
        # the function) on the machine running the bot. Returns a
        # string message which can be displayed for the user.

        # Create a Popen object which will take in the command and
        # the working directory and run the command when communicate
        # is called
        self.terminalInstance = subprocess.Popen(
            [command],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True,
            cwd = self.currentDirectory)
        
        # Use communicate to run the command and get the bytes-like
		# objects as output/error
        stdout, stderr = self.terminalInstance.communicate()
        
        # Object containing data returned by the terminal after the
		# command was executed
        return ({
            "terminalName": self.name,
            "currentDirectory": self.currentDirectory,
            "executedCommand": command,
            "outputString": stdout.decode("utf-8"),
            "errorString": stderr.decode("utf-8")
        })
