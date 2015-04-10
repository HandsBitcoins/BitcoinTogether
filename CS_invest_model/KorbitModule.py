ERROR_KORBIT_API_NO_KEY_LOCK = 65
ERROR_KORBIT_API_NO_CONFIG_FILE = 66
ERROR_KORBIT_API_WRONG_KEY_LOCK = 67
ERROR_KORBIT_API_NOT_ENOUGH_PRAMS_TO_MAKE_CONFIG_FILE = 68
ERROR_KORBIT_API_NOT_ENOUGH_DATA_TO_MAKE_PARAMS = 69

import json

import ChiperSimple

class KorbitAPI(object):
    def __init__(self):
        self.tokenAccess = {}
        
    def connect(self,keyLock=-1):
        import httplib        
        
        if keyLock < 0:
            return ERROR_KORBIT_API_NO_KEY_LOCK
        
        if not self.checkExistConfigFile():
            return ERROR_KORBIT_API_NO_CONFIG_FILE
                
        #dataToToken = [keyAPI, keySecret, strID, strPassword]
        dataToToken = self.readConfigFile(keyLock)        
        if len(dataToToken[0]) == 0:
            return ERROR_KORBIT_API_WRONG_KEY_LOCK
        
        connection = httplib.HTTPSConnection("api.korbit-test.com")
        parameter = self.getConnectionParameter(dataToToken)        
        header = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
        connection.request("POST", "/v1/oauth2/access_token", parameter, header)
        response = connection.getresponse()
        self.tokenAccess = response.read()
        self.tokenAccess = json.loads(self.tokenAccess)
        
        return self.tokenAccess
        
    def checkExistConfigFile(self):
        import os
        return os.path.isfile("./korbitAPI.dat")
    
    def makeConfigFile(self,keyLock=-1,keyAPI=-1,keySecret=-1,strID=-1,strPassword=-1):
        if keyAPI < 0 or keySecret < 0 or strID < 0 or strPassword < 0 or keyLock < 0:
            return ERROR_KORBIT_API_NOT_ENOUGH_PRAMS_TO_MAKE_CONFIG_FILE
            
        chiper = ChiperSimple()
        
        hexToSave = chiper.encrypt(keyAPI, keyLock) + "|"
        hexToSave += chiper.encrypt(keySecret, keyLock) + "|"        
        hexToSave += chiper.encrypt(strID, keyLock) + "|"        
        hexToSave += chiper.encrypt(strPassword, keyLock)        
        
        streamFile = open("./korbitAPI.dat",'w')
        streamFile.write(hexToSave)
        streamFile.close()
        
        return 0
    
    def readConfigFile(self,keyLock=-1):
        if keyLock < 0:
            return ERROR_KORBIT_API_NO_KEY_LOCK
        
        streamFile = open("./korbitAPI.dat",'r')
        hexToDecrypt = streamFile.read()        
        streamFile.close()
        
        hexToDecrypt = hexToDecrypt.split('|')
        
        cipher = ChiperSimple()
        dataToToken = []
        for i in range(4):            
            dataToToken.append(cipher.decrypt(hexToDecrypt[i], keyLock))
        
        return dataToToken
         
    def getConnectionParameter(self,dataToToken=-1):
        import urllib       
        
        if dataToToken < 0 or len(dataToToken) != 4:
            return ERROR_KORBIT_API_NOT_ENOUGH_DATA_TO_MAKE_PARAMS
        
        params = {'client_id': dataToToken[0],
                 'client_secret': dataToToken[1],
                 'username': dataToToken[2],
                 'password': dataToToken[3],
                 'grant_type': 'password'} 
        
        return urllib.urlencode(params)
    
    def getPrices(self):        
        import httplib
  
        #GET https://api.korbit.co.kr/v1/ticker/detailed                
        connection = httplib.HTTPSConnection("api.korbit-test.com")
        connection.request("GET","/v1/ticker/detailed")
        response = connection.getresponse()
        jsonResponse = response.read()
        infoPrices = json.loads(jsonResponse)
        
        return infoPrices
        
    def buy(self,amount,price):
        pass
    
    def sell(self,amount,price):
        pass
        
    def checkEnoughKRW(self,amount):
        pass
        
    def checkEnoughBTC(self,amount):
        pass
    
    def lookupOrders(self):
        pass
        
    def cancelOrder(self,id):
        pass
        

# kapi = KorbitAPI()
# kapi.makeConfigFile("A", "ASD", "keySecret", "strID", "strPassword")
# datas = kapi.readConfigFile("A")
# print "A", datas
# datas = kapi.readConfigFile("B")
# print "B", datas
# print len(datas[0])