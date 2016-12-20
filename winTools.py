import os
import ConfigParser

def newRas():
     print("Build the Dial Now")
     os.system("staticTools\win\newDial.vbs")
     time.sleep(2)

def getIp():
     #Todo get wlan ip address in windows
     return ""

def connectWired(username, password, pin):
     cf = ConfigParser.ConfigParser()
     cf.read("singleNet.conf")
     if not cf.has_option("config", "built"):
          newRas()
          cf.set("config", "built", "1")
          f = open('singleNet.conf','w')
          cf.write(f)
     cmd = 'out\win\createADSL.exe "'+pin+'" "'+username+'" "'+password+'" "HSingleNet"'
     os.system(cmd)
     print("connect finished")
