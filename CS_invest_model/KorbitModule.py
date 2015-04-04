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

class korbitAPI(object):
    def __init__(self):
        pass
    
    def connect(self):
        if self.checkExistConfigFile():
            self.makeConfigFile()
        
    def checkExistConfigFile(self):
        return False
    
    def makeConfigFile(self,keyAPI=-1,keySecret=-1,strID=-1,strPassword=-1):
        
        return 0
        
        
    
        