
class korbitAPI(object):
    def __init__(self):
        pass
    
    def connect(self):
        if self.checkExistConfigFile():
            self.makeConfigFile()
        
    def checkExistConfigFile(self):
        return False
    
    def makeConfigFile(self,keyAPI=-1,keySecret=-1,):
        return 0
    
    def 