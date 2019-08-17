import subprocess
import os
from pathlib import Path

# Class to represent an instance of a terminal which is initiated
# by a discord user via the discord bot
class Terminal:

    # Object constructor
    def __init__(self, name, terminalPath):
        # The name of the terminal instance (supplied by the user)
        self.name = name

        # The path of the actual terminal program to be run via discord bot
        self.terminalPath = terminalPath
        
        # The current working directory that the user is in (starts in the home directory)
        self.currentDirectory = str(Path.home())
    
    # Execute a bash terminal command (passed as an argument to the function) on the
    # machine running the bot. Returns a string message which can be displayed for the user.
    def executeCommand(self, command):
        
        # Use the correct path-separator for the operating system
        directorySeparator = os.sep

        # Execute a shell-terminal command and store the "stdout" and "stderr" output in the
        # variables "outputString" and "errorString", respectively
        commandReturnObject = subprocess.run(
            self.currentDirectory + directorySeparator + command,
            shell = True,
            capture_output = True
        )

        # Object containing data returned by the terminal after the command was executed
        return ({
            'terminalName': self.name,
            'executedCommand': command,
            'outputString': commandReturnObject.stdout.decode('utf-8'),
            'errorString': commandReturnObject.stderr.decode('utf-8')
        })

# ~~~~~~~~~~~~~~~~ TEST CODE (for windows) ~~~~~~~~~~~~~~~~

# testTerminal = Terminal("test-terminal", "cmd.exe")
# print("The current directory is " + testTerminal.currentDirectory)
# terminalOutput = testTerminal.executeCommand("dir")
# print("The command '" + terminalOutput['executedCommand'] + "' was executed in terminal '"
#     + terminalOutput['terminalName'] + "'.\n\n" + "The terminal returned the output:\n'"
#     + terminalOutput['outputString'] + "'.\n\n" + "If there was an error message, it reads: '"
#     + terminalOutput['errorString'] + "'.\n")

# ~~~~~~~~~~~~~~~~ TEST CODE (for linux) ~~~~~~~~~~~~~~~~~~

# testTerminal = Terminal("test-terminal", "/bin/bash")
# terminalOutput = testTerminal.executeCommand("ls")
# print("The command '" + terminalOutput['executedCommand'] + "' was executed in terminal '"
#     + terminalOutput['terminalName'] + "'.\n\n" + "The terminal returned the output:\n'"
#     + terminalOutput['outputString'] + "'.\n\n" + "If there was an error message, it reads: '"
#     + terminalOutput['errorString'] + "'.\n")

