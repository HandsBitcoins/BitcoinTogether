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
    
    def initEmail(self):
        self.server = smtplib.SMTP('smtp.gmail.com:587')
                    
    def isExistConfigFile(self):
        import os
        return os.path.isfile("./SMTPEmail.dat")
    
    def createConfigFile(self):
        pass
        
    def readConfigFile(self):
        pass