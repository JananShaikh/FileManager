# Name: File Manager Application 
# Authors: Akhona, Sabiha and Oscar
# Date Modified: 24/09/22

'''
This is a lightweight file manager web application built using python flask and html.
Features included:
  1.Upload and download of files individually or in batch
  2.Directory create, rename and delete
  3.File move, rename and delete
  4.User authentication and permission
  5.Integrated viewer for HTML, images, audios and videos

'''
# Importing of libraries neccesery 
import subprocess
import shutil
import zipfile
import webbrowser
import os 
from io import BytesIO
from flask import Flask, render_template, request, redirect, flash, send_from_directory, send_file,session
from werkzeug.utils import secure_filename
from zipfile import ZipFile
from flask.views import View, MethodView
# Import classes
import fileClass
import folderClass
import userClass

# Set up flask app
app = Flask(__name__)
app.secret_key = "somesecretkey" 

# Lists to store files, folders and users
files = []
folders = []
users = []
idNo = 0 # id number of user

# Read a file indicating authorised users and entering them into the system
with open('access.txt') as f:
    while True:
        line = f.readline() # extract line from file ..
        if not line: # check if end-of-file
            break
        user = userClass.User(idNo) # Creating user object    
        user.setName(line.strip())  # Set name
        user.setPwd(f.readline().strip())  # Set Password
    
        users.append(user) # Add to user list
        idNo+=1

# FileManager class that contains features that manages files and directories
class FileManager(MethodView):
    
    # This function takes you to the login page
    @app.route('/', methods=['GET'])
    def index():
        return render_template("login.html")
    
    # This function takes you to the home page of the file manager
    @app.route('/home', methods=['GET'])
    def index2():
        return render_template('upload.html', current_working_directory=os.getcwd(), file_list=subprocess.check_output('ls', shell=True).decode('utf-8').split('\n'))
  

    @app.route('/form_logout',methods=['POST','GET'])
    def logout():
        return redirect("/")

    # This function authenticates users with permission or vice versa
    @app.route('/form_login',methods=['POST','GET'])
    def login():
        name=request.form['username']
        pwd=request.form['password']
        authorize = False
    
        for user in users:
            if user.getName() == name:
                authorize = True
                if user.getPwd() == pwd:
                    return redirect('/home')
                else:    
                    return render_template('login.html',info='Access Denied: Invalid Password')
             
        if not authorize :
            return render_template('login.html',info='Access Denied: Invalid User')
        # redirect to homepage
        return redirect('/home')      
              
    # This function is responsible for navigation of files between folders
    @app.route('/location')
    def location():
        # path retrieval
        os.chdir(request.args.get('path'))
      
        # redirect to homepage
        return redirect('/home')
      
    # This function lets users select files and folders  
    @app.route('/select', methods=['POST'])
    def select():
        if request.method == 'POST':
            # lists to store temporary selected files and/or folders
            global filelist 
            global folderlist
            
            # Retrieve the names of the files/folders
            filelist = request.form.getlist('filename')
            folderlist = request.form.getlist('foldername')
            
            # Inform users on what was selected
            flash("Selected files:")
            for file in filelist:
                flash(file) 
          
            flash("Selected folders:")
            for folder in folderlist:
                flash(folder)
            
            # redirect to homepage
            return redirect('/home')
      
    # This function uploads file(s)  
    @app.route('/upload', methods=['POST'])
    def uploadFiles():               
        if request.method == 'POST': 
            # retrieve file(s)
            path = os.getcwd()
            fileNames = request.files.getlist("file_list[]") # retrieve file list to upload
            #filenames = [] # List for batch download(if applicable)
      
            # upload file(s)
            for file in fileNames:
                filename = secure_filename(file.filename)
                file.save(path+"/"+filename)
                #filenames.append(filename)
                files.append( fileClass.File(filename))  # Create file object and add to list
            
            # redirect to homepage
            return redirect('/home')

    # This function downloads file(s)  
    @app.route('/download', methods=['GET'])
    def downloadFiles():
        if request.method == 'GET':
            global filelist
            path = os.getcwd() # Obtain path
            
            # If one file then single download..
            if len(filelist) == 1:
                for filename in filelist:
                    return send_file(path+"/"+filename, as_attachment=True) # Single Download
                    
            # ..else zip files then download zip
            elif len(filelist) > 1:  
                # Zipfile creation of selected files
                zipObj = ZipFile('download.zip', 'w')
          
                for filename in filelist:
                    zipObj.write(filename)
                zipObj.close()
          
                return send_file(path+"/"+'download.zip', mimetype = 'zip', as_attachment = True) # Batch download
        
        # redirect to homepage
        return redirect('/home')
    
    # This function creates a new directory  
    @app.route('/createDirectory')
    def createDirectory():
        # retrieve folder and delete
        os.mkdir(request.args.get('folder'))
      
        # create folder object and add to folder list
        folders.append( folderClass.Folder(request.args.get('folder')) ) 
      
        # redirect to homepage
        return redirect('/home')
    
    # This function moves a file to another folder
    @app.route('/move', methods=['POST'])        
    def move():
        # Get location and new name
        origin = os.getcwd()
        files = os.listdir(origin)
        text = request.form['text']
        target =os.getcwd()+"/"+text
        
        # Move to new location
        for file in filelist:
            shutil.move(origin + "/"+file, target)
            
        # redirect to homepage    
        return redirect('/home')
    
    # This function deletes file(s) and/or folder(s)      
    @app.route('/remove')  
    def remove():
        # Temporaryly selected file(s)/folder(s)
        global filelist
        global folderlist
      
        for filename in filelist:
          os.remove(filename) # delete file
          
          # Remove file object(s) from file list
          for file in files:
              if file.getName() == filename:
                  files.remove(file)
        
        for foldername in folderlist: 
          shutil.rmtree(os.getcwd() + '/' + foldername) # delete directory
          
          # Remove folder object(s) from list
          for folder in folders:
              if folder.getName() == foldername:
                  folders.remove(folder)
       
        # redirect to homepage
        return redirect('/home')          
    
    # This function renames file(s) and/or folder(s)
    @app.route('/rename', methods=['POST'])        
    def renameFile():
        # Obtain path and new name
        path = os.getcwd()
        text = request.form['text']
      
        for filename in filelist:
            ext = os.path.splitext(filename)[-1].lower() # Maintain extention of file
            os.rename(filename,text+ext) # rename file
            
            # Rename file object(s) from file list
            for file in files:
                if file.getName() == filename:
                    file.rename(text+ext)
        
        for foldername in folderlist:
            os.rename(foldername,text) # rename folder
            
            # Remove folder object(s) from list
            for folder in folders:
                if folder.getName() == foldername:
                    folder.rename(text)
            
        # redirect to homepage
        return redirect('/home')     

  
    # THis function allows viewing of text and python files
    @app.route('/view', methods = ['GET'] )
    def view():
        # get the file path
        filepath = os.getcwd()
        
        # Display 
        with open(request.args.get('file')) as f:
            return f.read().replace('\n', '<br>')
        
        # redirect to homepage
        return redirect('/home')    
  
    # This function allows integrated viewinf for HTML, images, audios and videos
    @app.route('/viewAdditional', methods = ['GET'])
    def viewAdditional():
        webbrowser.open(request.args.get('image'), new=2)
        
        # redirect to homepage
        return redirect('/home')
      
    '''
    For developers use only
    
    # print objects in lists:    
    @app.route('/display')
    def display():
        #print file, folder and user objects
        for f in files:
            print("file: "+f.getName())
      
        for f in folders:
            print("folder: "+f.getName())
            
        for u in users:
            print("user: "+u.getName())    
        
        return redirect('/home')      
        
    # Add to html file if wish to see:
    <form action="/display">
    <input type="submit" value="Display">
    </form>
    '''  
         
# Main 
if __name__ == '__main__':
    app.run()  # Run web application on local host
    
'''
References:
1.https://github.com/maksimKorzh/flask-tutorials/tree/master/simple-file-manager
2. https://github.com/nachi-hebbar/Login-Page-With-Flask-HTML
'''    
