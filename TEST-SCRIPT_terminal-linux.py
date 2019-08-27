# This script tests the Terminal class on computers which are running
# a Linux operating system

from terminal import Terminal

testTerminal = Terminal("test-terminal", "/bin/bash")
terminalOutput = testTerminal.executeCommand("ls")
print(
    "The command '" + terminalOutput['executedCommand']
    + "' was executed in terminal '" + terminalOutput['terminalName']
    + "'.\n\n" + "The terminal returned the output:\n'"
    + terminalOutput['outputString'] + "'.\n\n"
    + "If there was an error message, it reads: '"
    + terminalOutput['errorString'] + "'.\n"
)