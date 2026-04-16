"""
Anthony Stone
CSC-463
Professor Wu

Completed protocol script.

- Defines headers.
- Defines encoding and decoding protocol.
- Defines the format to transfer file list.
- Defines packet size.
"""

# Defines the protocol header
HEAD_LIST='LST'
HEAD_REQUEST='REQ'
HEAD_DOWNLOAD='DLD'
HEAD_ERROR='ERR'
HEAD_READY='RDY'
HEAD_UPLOAD='ULD'

# Define packet size
PACKET_SIZE=1024

# we prepare the message that are sent between server and client as the header + content
def prepareMsg(header, msg):
    return (header+msg).encode()

def prepareFileList(header,fList):
    '''
    function to prepare file list to msg
    '''
    msg=header
    for i in range(len(fList)):
        if (i==len(fList)-1):
            msg+=fList[i]
        else:
            msg+=fList[i]+','
    return msg.encode()

# Decode the received message, the first three letters are used as protocol header
def decodeMsg(msg):
    if (len(msg)<=3):
        return HEAD_ERROR, 'EMPTY MESSAGE'
    else:
        return msg[0:3],msg[3:len(msg)]
