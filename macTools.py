import netifaces

def getIp():
    return netifaces.ifaddresses('en0')[2][0]['addr']

def connectWired(username, password, pin):
    pass
