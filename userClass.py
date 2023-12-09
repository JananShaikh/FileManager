# Name: User Class
# Authors: Akhona, Sabiha and Oscar
# Date Modified: 24/09/22

'''
This is a user class that stores details about a folder in a file manager system
'''

class User:  
    # variables
    id = 0
    name = ''
    password = ''
    
    # method on declaration setting the id of the user    
    def __init__(self, idNo): 
        self.id = idNo
    
    # method to set the name of the user
    def setName(self, newName):
        self.name = newName
    
    # method to set the password of the user    
    def setPwd(self, newPwd):
        self.password = newPwd    
    
    # method to return the name of the user         
    def getName(self):
      return self.name
    
    # method to return the password of the user
    def getPwd(self):
      return self.password  
    
    # method to return the id of the user
    def getID(self):
      return self.id  
