import re
import utils

def getIp():
     ipRe = re.compile(r"(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)")
     wlanList = ['wlp2s0', 'wlan0']
     wlanip = ""
     for wlan in wlanList:
          ip = utils.execCmd("ifconfig "+wlan)
	  ipList = ipRe.findall(ip)
	  if len(ipList) != 0:
	       wlanip = ipList[0]
	       break
     return wlanip
    
def connectWired(username, password, pin):
    pass
