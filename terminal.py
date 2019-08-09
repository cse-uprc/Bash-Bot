import subprocess

# Class to represent an instance of a terminal which is initiated
# by a discord user via the discord bot
class Terminal:

    # Object constructor
    def __init__(self, name, terminalPath):
        # The name of the terminal instance (supplied by the user)
        self.name = name

        # The path of the actual terminal program to be run via discord bot
        self.terminalPath = terminalPath
        
        # The actual terminal instance on the computer 
        self.terminalInstance = subprocess.Popen(
            args = self.terminalPath,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True, 
       )
    
    # Execute a bash terminal command (passed as an argument to the function) on the
    # machine running the bot. Returns a string message which can be displayed for the user.
    def executeCommand(self, command):
        # Execute a shell-terminal command and store the "stdout" and "stderr" output in the
        # variables "outputString" and "errorString", respectively
        outputString, errorString = self.terminalInstance.communicate(command.encode('utf-8'))

        # Object containing data returned by the terminal after the command was executed
        return ({
            'terminalName': self.name,
            'executedCommand': command,
            'outputString': outputString.decode('utf-8'),
            'errorString': errorString.decode('utf-8')
        })

# ~~~~~~~~~~~~~~~~ TEST CODE (for windows) ~~~~~~~~~~~~~~~~

# testTerminal = Terminal("test-terminal", "cmd.exe")
# terminalOutput = testTerminal.executeCommand("dir")
# print("The command '" + terminalOutput['executedCommand'] + "' was executed in terminal '"
#      + terminalOutput['terminalName'] + "'.\n\n" + "The terminal returned the output:\n'"
#      + terminalOutput['outputString'] + "'.\n\n" + "If there was an error message, it reads: '"
#      + terminalOutput['errorString'] + "'.\n")

# ~~~~~~~~~~~~~~~~ TEST CODE (for linux) ~~~~~~~~~~~~~~~~~~

# testTerminal = Terminal("test-terminal", "/bin/bash")
# terminalOutput = testTerminal.executeCommand("ls")
# print("The command '" + terminalOutput['executedCommand'] + "' was executed in terminal '"
#     + terminalOutput['terminalName'] + "'.\n\n" + "The terminal returned the output:\n'"
#     + terminalOutput['outputString'] + "'.\n\n" + "If there was an error message, it reads: '"
#     + terminalOutput['errorString'] + "'.\n")

