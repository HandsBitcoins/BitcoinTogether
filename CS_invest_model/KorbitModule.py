class ChiperSimple(object):
    def __init__(self):
        self.LEN_SALT = 32
        self.NUM_ROUND = 1337
        self.SIZE_BLOCK = 16
        self.SIZE_KEY = 32
    
    def encrypt(self,message,keyLock):
        import hashlib
        import os
        
        from Crypto.Cipher import AES
                
        salt = os.urandom(self.LEN_SALT)
        iv = os.urandom(self.SIZE_BLOCK)
        
        lenPadding = 16 - (len(message)%16)
        messagePadded = message + chr(lenPadding)*lenPadding
        
        keyDerived = keyLock
        for i in range(0,self.NUM_ROUND):
            keyDerived = hashlib.sha256(keyDerived+salt).digest()
        keyDerived = keyDerived[:self.SIZE_KEY]
        
        cipher = AES.new(keyDerived, AES.MODE_CBC, iv)
        messageCiphered = cipher.encrypt(messagePadded)
        messageCiphered = messageCiphered + iv + salt
        
        return messageCiphered.encode("hex")
        
    def decrypt(self,msg,keyLock):
        import hashlib
        
        from Crypto.Cipher import AES
    
        msgDecoded = msg.decode("hex")
        
        posIv = len(msgDecoded)-self.SIZE_BLOCK-self.LEN_SALT
        posSalt = len(msgDecoded)-self.LEN_SALT
        
        data = msgDecoded[:posIv]
        iv = msgDecoded[posIv:posSalt]
        salt = msgDecoded[posSalt:]
                
        keyDerive = keyLock
        for i in range(0,self.NUM_ROUND):
            keyDerive = hashlib.sha256(keyDerive+salt).digest()
        keyDerive = keyDerive[:self.SIZE_KEY]
        
        cipher = AES.new(keyDerive, AES.MODE_CBC, iv)
        msgPadded = cipher.decrypt(data)
        lenPadding = ord(msgPadded[-1])
        msgDecrypted = msgPadded[:-lenPadding]
        
        return msgDecrypted

ERROR_KORBIT_API_NO_KEY_LOCK = 65
ERROR_KORBIT_API_NO_CONFIG_FILE = 66
ERROR_KORBIT_API_WRONG_KEY_LOCK = 67
ERROR_KORBIT_API_NOT_ENOUGH_PRAMS_TO_MAKE_CONFIG_FILE = 68
ERROR_KORBIT_API_NOT_ENOUGH_DATA_TO_MAKE_PARAMS = 69

class KorbitAPI(object):
    def __init__(self):
        pass
        
    def connect(self,keyLock=-1):
        import httplib
        
        if keyLock < 0:
            return ERROR_KORBIT_API_NO_KEY_LOCK
        
        if self.checkExistConfigFile():
            return ERROR_KORBIT_API_NO_CONFIG_FILE
                
        #dataToToken = [keyAPI, keySecret, strID, strPassword]
        dataToToken = self.readConfigFile(keyLock)
        
        if len(dataToToken[0]) == 0:
            return ERROR_KORBIT_API_WRONG_KEY_LOCK
        
        connection = httplib.HTTPSConnection("https://api.korbit.co.kr/v1/oauth2/access_token")
        parameter = getParameter(dataToToken)
        header = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
        connection.request("POST", "/v1/oauth2/access_token", parameter, header)
        response = connection.getresponse()
        
        return response
                
    def checkExistConfigFile(self):
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
     
    def getParameter(self,dataToToken=-1):
        if dataToToken < 0 or len(dataToToken) != 4:
            return ERROR_KORBIT_API_NOT_ENOUGH_DATA_TO_MAKE_PARAMS
        
        param = []        
        param.append("client_id="      + dataToToken[0])
        param.append("&client_secret=" + dataToToken[1])
        param.append("&username="      + dataToToken[2])        
        param.append("&password="      + dataToToken[3])
        param.append("&grant_type=password")

        paramPost = ""
        for eachParam in param:
            paramPost += eachParam
            
        return paramPost

kapi = KorbitAPI()
kapi.makeConfigFile("A", "ASD", "keySecret", "strID", "strPassword")
datas = kapi.readConfigFile("A")
print "A", datas
datas = kapi.readConfigFile("B")
print "B", datas
print len(datas[0])