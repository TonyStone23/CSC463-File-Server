"""
Anthony Stone
CSC-463
Professor Wu

Completed configuration script.

- Parse .config files for port numbers and Download/Upload/Share Folder paths.
"""

import os
class config:
    import os

    base_dir = os.path.dirname(os.path.abspath(__file__))
    #define header
    server_port='SERVER_PORT'
    path="PATH"
    server="SERVER"
    client_port="CLIENT_PORT"
    download="DOWNLOAD"
    upload="UPLOAD"
    clientConfig = os.path.join(base_dir, "client.config")
    serverConfig = os.path.join(base_dir, "server.config")
    
    def __init__(self):
        pass
    
    def readServerConfig(self):
        try:
            with open(self.serverConfig,'r') as f:
                serPort=0
                sharePath=""
                for l in f:
                    sub=l.strip().split("=")
                    if(sub[0]==self.server_port):
                        serPort=int(sub[1])
                    elif(sub[0]==self.path):
                        sharePath=sub[1]
                    else:
                        pass
                return serPort, sharePath
        except Exception as e:
            print(str(e))
     
          
    def readClientConfig(self):
        '''
        This function read client configuration file, return four values
        @return: serverName
        @return: serverPort
        @return: clientPort
        @return: downloadPath
        '''
        try:
            with open(self.clientConfig,'r') as f:
                serPort=0
                serName=""
                clientPort=0
                downPath=""
                upPath=""
                for l in f:
                    sub=l.strip().split("=")
                    if(sub[0]==self.server_port):
                        serPort=int(sub[1])
                    elif(sub[0]==self.server):
                        serName=sub[1]
                    elif(sub[0]==self.client_port):
                        clientPort=sub[1]   
                    elif(sub[0]==self.download):
                        downPath=sub[1]     
                    elif(sub[0]==self.upload):
                        upPath=sub[1] 
                    else:
                        pass  
                return serName, serPort, clientPort, downPath, upPath 
        except Exception as e:
            print(str(e))