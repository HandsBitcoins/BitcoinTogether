import KorbitModule

class KorbitTraderCUI(object):
    def __init__(self):
        self.korbitAPI = KorbitModule.KorbitAPI()
        
    def connect(self):
        result = 1
        keyLock = self.getInput("Password is Needed. Please enter the password.")
        while result != 0:            
            result = self.korbitAPI.connect(keyLock)
            
            if result == KorbitModule.ERROR_KORBIT_API_NO_KEY_LOCK: #no keyLock
                keyLock = self.getInput("Password is Needed. Please enter the password.")
            elif result == KorbitModule.ERROR_KORBIT_API_NO_CONFIG_FILE: #no configFile
                self.genConfigFile()
            elif result == ERROR_KORBIT_API_WRONG_KEY_LOCK:
                keyLock = self.getInput("Password is Wrong. Please enter the RIGHT password.")                
                
    def getInput(self,msgToDisplay="Please enter anything. If you can see this message, please say fuck that lazy developers"):
        return input(msgToDisplay)
        
    def genConfigFile(self):
        pass
    