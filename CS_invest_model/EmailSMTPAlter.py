import smtplib

def testEmail():    
    import email
    
    msg = email.mime.Text.MIMEText("This is test message")

    addrEmail = "rectifying@gmail.com"

    msg['Subject'] = "Bitcoin alter message test"
    msg['From'] = addrEmail
    msg['To'] = addrEmail
    
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.login("rectifying@gmail.com", "")
    s.sendmail(addrEmail, [addrEmail], msg.as_string())
    s.close()

class SMTPEmailAlter(object):
    def __init__(self):
        pass
    
    def initEmail(self):                
        self.fileName = "./SMTPEmail.dat"
        self.fileNameReciver = "./Maillist.txt"         
        
        self.sender = "rectifying@gmail.com"
        self.password = self.getKeyLock()
                
    def sendEmail(self,subject,content):
        import email
        
        receiver = self.getReceiver()
        
        msg = email.mime.Text.MIMEText(content)        
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ", ".join(receiver)
        
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(self.sender, self.password)
        server.sendmail(self.sender, receiver, msg.as_string())
        server.close()
    
    def getReceiver(self):
        streamFile = open(self.fileNameReciver,'r')
        streamReciver = streamFile.read()        
        streamFile.close()
         
        listReciver = streamReciver.split(',')
                 
        return listReciver

    def isExistConfigFile(self):
        import os
        return os.path.isfile(self.nameFile)
    
    def getKeyLock(self):
        import getpass
        return getpass.getpass("Please enter the email password: ")
    
    def createConfigFile(self):
        pass
#         chiper = ChiperSimple.ChiperSimple()
#         
#         hexToSave = chiper.encrypt(keyAPI, keyLock) + "|"
#         hexToSave += chiper.encrypt(keySecret, keyLock) + "|"        
#         hexToSave += chiper.encrypt(strID, keyLock) + "|"        
#         hexToSave += chiper.encrypt(strPassword, keyLock)        
#         
#         streamFile = open(self.nameFile,'w')
#         streamFile.write(hexToSave)
#         streamFile.close()
        
    def readConfigFile(self):
        pass
#         streamFile = open(self.nameFile,'r')
#         hexToDecrypt = streamFile.read()        
#         streamFile.close()
#         
#         hexToDecrypt = hexToDecrypt.split('|')
#         
#         cipher = ChiperSimple()
#         dataToToken = []
#         for i in range(4):            
#             dataToToken.append(cipher.decrypt(hexToDecrypt[i], keyLock))
#         
#         return dataToToken