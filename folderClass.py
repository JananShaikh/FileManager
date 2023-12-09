# Name: Folder Class
# Authors: Akhona, Sabiha and Oscar
# Date Modified: 24/09/22

'''
This is a folder class that stores details about a folder in a file manager system
'''

class Folder:  
    # variables
    name = ''
    
    # method on declaration setting the name of the folder  
    def __init__(self, name): 
        self.name = name         
    
    # Method to rename the folder
    def rename(self, newName):
        self.name = newName
    
    # Method to return name of folder         
    def getName(self):
      return self.name 
