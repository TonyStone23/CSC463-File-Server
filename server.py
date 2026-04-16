"""
Anthony Stone
CSC-463
Professor Wu

Completed server-side script.

- Sends error if it receives a message with a header not defined in protocol.
- Opens and closes connections with client.
- Transfers data out of a directory specified by administrator.
"""

import config
import protocol
import os
from socket import *
class server:

    # Constructor: load the server information from config file
    def __init__(self):
        self.port, self.path=config.config().readServerConfig()

    # Get the file names from shared directory
    def getFileList(self):
        return os.listdir(self.path)
    
    # Function to send file list to client       
    def listFile(self, serverSocket):
        serverSocket.send(protocol.prepareFileList(protocol.HEAD_LIST, self.getFileList()))

    # Function to send a file to client       
    def sendFile(self,serverSocket,fileName):

        print("sending " + fileName)

        f = open(fileName,'rb')
        l = f.read(protocol.PACKET_SIZE)
        while (l):
            serverSocket.send(l)
            l = f.read(protocol.PACKET_SIZE)
        
        print(fileName + " sent.")
    
    # Function for receiving file from client
    def receiveFile(self, serverSocket, fileName):
        fullPath = self.path + "/" + fileName

        with open(fullPath, 'wb') as f:
            print("Receiving file:", fileName)

            while True:
                data = serverSocket.recv(protocol.PACKET_SIZE)
                if not data:
                    break
                f.write(data)

        print(fileName + " uploaded successfully")

    # Main function of server, start the file sharing service
    def start(self):
        serverPort=self.port
        serverSocket=socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('',serverPort))
        serverSocket.listen(20)
        print('The server is ready to receive')
        while True:
            connectionSocket, addr = serverSocket.accept()
            print(connectionSocket)
            dataRec = connectionSocket.recv(protocol.PACKET_SIZE)
            header,msg=protocol.decodeMsg(dataRec.decode()) # Get client's info, parse it to header and content
            # Main logic of the program, send different content to client according to client's requests
            if(header==protocol.HEAD_REQUEST):
                self.listFile(connectionSocket)
            elif(header==protocol.HEAD_DOWNLOAD):
                self.sendFile(connectionSocket, self.path+"/"+msg)
            elif(header==protocol.HEAD_UPLOAD):
                connectionSocket.send(protocol.prepareMsg(protocol.HEAD_READY, " "))
                self.receiveFile(connectionSocket, msg)
            else:
                connectionSocket.send(protocol.prepareMsg(protocol.HEAD_ERROR, "Invalid Message"))
            connectionSocket.close()

def main():
    s=server()
    s.start()

if __name__ == "__main__":
    main()
