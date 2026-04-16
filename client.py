"""
Anthony Stone
CSC-463
Professor Wu

Completed client-side script.

- Seeks connections and sends requests to the server.
- Downloads server files to a directory specified by the user.
- Uploads files to the server from a directory specified by the user.
"""
import protocol
import config
from socket import *
import os

class client:
    
    fileList=[] # list to store the file information

    #Constructor: load client configuration from config file
    def __init__(self):
        self.serverName, self.serverPort, self.clientPort, self.downloadPath, self.uploadPath = config.config().readClientConfig()

    # Function to produce user menu 
    def printMenu(self):
        print("\nWelcome to simple file sharing system!")
        print("Please select operations from menu")
        print("--------------------------------------")
        print("1. Review the List of Available Files")
        print("2. Download File")
        print("3. Upload File")
        print("4. Quit\n")

    # Function to get user selection from the menu
    def getUserSelection(self):       
        ans=0

        while ans>4 or ans<1:
            self.printMenu()
            try:
                ans=int(input())
            except:
                ans=0

            if (ans<=4) and (ans>=1):
                return ans
            
            print("Invalid Option")

    # Build connection to server
    def connect(self):
        serverName = self.serverName
        serverPort = self.serverPort
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName,serverPort))
        return clientSocket

    # Get file list from server by sending the request
    def getFileList(self):
        mySocket=self.connect()
        mySocket.send(protocol.prepareMsg(protocol.HEAD_REQUEST," "))
        header, msg=protocol.decodeMsg(mySocket.recv(protocol.PACKET_SIZE).decode())
        mySocket.close()

        if(header==protocol.HEAD_LIST): 
            files=msg.split(",")
            self.fileList=[]

            for f in files:
                self.fileList.append(f)

        else:
            print ("Error: cannnot get file list!")

    # function to print files in the list with the file number
    def printFileList(self):
        count=0

        for f in self.fileList:
            count+=1
            print('{:<3d}{}'.format(count,f))

    # Function to select the file from file list by file number
    def selectDownloadFile(self):

        if(len(self.fileList)==0):
            self.getFileList()
        ans=-1

        while ans<0 or ans>len(self.fileList)+1:
            self.printFileList()
            print("Please select the file you want to download from the list (enter the number of files):")
            try:
                ans=int(input())
            except:
                ans=-1

            if (ans>0) and (ans<len(self.fileList)+1):
                return self.fileList[ans-1]
            
            print("Invalid number")

    # Function to send download request to server and wait for file data
    def downloadFile(self,fileName):
        mySocket=self.connect()
        mySocket.send(protocol.prepareMsg(protocol.HEAD_DOWNLOAD, fileName))

        with open(self.downloadPath+"/"+fileName, 'wb') as f:
            print ("Downloading " + fileName)

            while True:
                data = mySocket.recv(protocol.PACKET_SIZE)
                if not data:
                    break
            
                f.write(data) # write data to a file

        print(fileName+" downloaded successfully")
        mySocket.close()

    # Function to select a file to upload to the server by file number
    def selectUploadFile(self):
        files = os.listdir(self.uploadPath)

        i = 1
        for f in files:
            print(f"{i}. {f}")
            i += 1

        ans = -1
        while ans < 1 or ans > len(files):
            try:
                ans = int(input("Select file to upload: "))
            except:
                ans = -1

        return files[ans - 1]

    # Function to send file data to the server
    def uploadFile(self, fileName):
        mySocket = self.connect()

        mySocket.send(protocol.prepareMsg(protocol.HEAD_UPLOAD, fileName))

        dataRec = mySocket.recv(protocol.PACKET_SIZE)
        header,msg=protocol.decodeMsg(dataRec.decode())
        if header != protocol.HEAD_READY:
            print(header, protocol.HEAD_READY)
            print("Server not ready")
            return

        fullPath = os.path.join(self.uploadPath, fileName)

        with open(fullPath, 'rb') as f:
            print("Uploading:", fileName)

            while True:
                data = f.read(protocol.PACKET_SIZE)
                if not data:
                    break
                mySocket.send(data)

        mySocket.close()
        print("Upload complete")

    # Main logic of the client, start the client application
    def start(self):
        opt=0
        while opt!=4:
            opt=self.getUserSelection()
            if opt==1:
                if(len(self.fileList)==0):
                    self.getFileList()
                self.printFileList()                  
            elif opt==2:
                self.downloadFile(self.selectDownloadFile())
            #**************************
            # You need another option for uploading files
            elif opt==3:
                self.uploadFile(self.selectUploadFile())
                
def main():
    c=client()
    c.start()
main()
