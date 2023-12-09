# Name: File Class
# Authors: Akhona, Sabiha and Oscar
# Date Modified: 24/09/22

'''
This is a file class that stores details about a file in a file manager system
'''

class File: 
    # Variables 
    name = ''
    type = ''
    
    # method on declaration setting the name and type of file  
    def __init__(self, name): 
        self.name = name   
        type = name.split(".")[1]      
    
    # Method to rename the file
    def rename(self, newName):
        self.name = newName
    
    # Method to return name of file         
    def getName(self):
      return self.name
      
    # Method to return type of file         
    def getName(self):
      return self.name           
