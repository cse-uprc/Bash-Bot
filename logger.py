import datetime


class Logger:
    def __init__(self,filePath="app.log"):
        """ Define the log filepath passed in the constructor. """
        
        self.filePath = filePath

    def log(self, msg):
        """ Log a message in the log file. """
        
        logMessage = "{0} - {1}".format(str(datetime.datetime.now()), msg)
        with open(self.filePath, "a+") as f:
            f.write(logMessage + "\n")
        print(logMessage)
