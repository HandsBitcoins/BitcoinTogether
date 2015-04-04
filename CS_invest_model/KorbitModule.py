class chiperSimple(object):
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
        
        return messageCiphered
        
    def decrypt(self,msg,keyLock):
        import hashlib
        
        from Crypto.Cipher import AES
    
        msgDecoded = msg
        
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

class korbitAPI(object):
    def __init__(self):
        pass
    
    def connect(self):
        if self.checkExistConfigFile():
            self.makeConfigFile()
        
    def checkExistConfigFile(self):
        return os.path.isfile("./korbitAPI.dat")
    
    def makeConfigFile(self,keyLock=-1,keyAPI=-1,keySecret=-1,strID=-1,strPassword=-1):
        if keyAPI < 0 or keySecret < 0 or strID < 0 or strPassword < 0 or keyLock < 0:
            return -1
            
        chiper = chiperSimple()
        
        hexToSave = chiper.encrypt(keyAPI, keyLock) + "|"
        hexToSave += chiper.encrypt(keySecret, keyLock) + "|"        
        hexToSave += chiper.encrypt(strID, keyLock) + "|"        
        hexToSave += chiper.encrypt(strPassword, keyLock)        
        
        streamFile = open("./korbitAPI.dat",'w')
        streamFile.write(hexToSave)
        streamFile.close()
        
        return 0
    
    def readConfigFile(self,keyLock=-1):
        streamFile = open("./korbitAPI.dat",'r')
        hexToDecrypt = streamFile.read()        
        streamFile.close()
        
        hexToDecrypt = hexToDecrypt.split('|')
        
        cipher = chiperSimple()
        dataToToken = []
        for i in range(4):
            print hexToDecrypt[i], len(hexToDecrypt[i])
            dataToToken.append(cipher.decrypt(hexToDecrypt[i], keyLock))
        
        return dataToToken
     
        