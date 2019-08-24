# This script tests the Terminal class on computers which are running
# a Windows operating system

from terminal import Terminal

testTerminal = Terminal("test-terminal", "cmd.exe")
print("The current directory is " + testTerminal.currentDirectory)
terminalOutput = testTerminal.executeCommand("dir")
print(
    "The command '" + terminalOutput['executedCommand'] 
    + "' was executed in terminal '" + terminalOutput['terminalName']
    + "'.\n\n" + "The terminal returned the output:\n'"
    + terminalOutput['outputString'] + "'.\n\n"
    + "If there was an error message, it reads: '"
    + terminalOutput['errorString'] + "'.\n"
)
