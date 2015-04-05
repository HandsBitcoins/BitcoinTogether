import getpass

import KorbitModule

class KorbitTraderCUI(object):
    def __init__(self):
        self.korbitAPI = KorbitModule.KorbitAPI()
        
    def connect(self):
        notConnected = True
        keyLock = getpass.getpass("Please enter the program password: ")
        while notConnected:            
            result = self.korbitAPI.connect(keyLock)
            
            if result == KorbitModule.ERROR_KORBIT_API_NO_KEY_LOCK: #no keyLock
                keyLock = getpass.getpass("Password is Needed. Please enter the password: ")
            elif result == KorbitModule.ERROR_KORBIT_API_NO_CONFIG_FILE: #no configFile
                print "Can not find configuration file \"korbitAPI.dat\"."
                self.genConfigFile()
            elif result == KorbitModule.ERROR_KORBIT_API_WRONG_KEY_LOCK:
                keyLock = getpass.getpass("Password is Wrong. Please enter the RIGHT password: ")                
            else:
                print "Connection established."
                notConnected = False
                
        return result
                
    def getInput(self,msgToDisplay="Please enter anything. If you can see this message, please say 'Fuck' that lazy developers: "):
        valInput = raw_input(msgToDisplay)
        return valInput
        
    def genConfigFile(self):
        print "Making configuration file.\n"
        
        notMade = True
                
        print "The trading program saves your login informations to access Korbit repeatedly."
        print "For the secure of login information, you need to set a password."
        print "\tWARNING!!: Do not set your program password to same as Korbit password!!"        

        while notMade:
            keyLock = getpass.getpass("Please set your program password: ")
            print "Thanks! If you lost your password, please delete file named \"korbitAPI.dat\"."
            
            print "\nNext, the trading program needs login information"
            keyAPI = raw_input("Please enter API key: ")
            keySecret = raw_input("Please enter secret key: ")
            strID = raw_input("Please enter Korbit ID: ")        
            strPassword = getpass.getpass("Please enter Korbit Password: ")
            
            result = self.korbitAPI.makeConfigFile(keyLock,keyAPI,keySecret,strID,strPassword)
            
            if result == KorbitModule.ERROR_KORBIT_API_NOT_ENOUGH_PRAMS_TO_MAKE_CONFIG_FILE:
                print "Fail to make configuration file. Retry....\n"
            else:
                print "Making is succeed!!\n"
                notMade = False
                
        return True 

ui = KorbitTraderCUI()
api = KorbitModule.KorbitAPI()

print "Welcome to Korbit Trader!!\n"
if not api.checkExistConfigFile():
    ui.genConfigFile()
response = ui.connect()
print response
print api.getPrices()


     
        