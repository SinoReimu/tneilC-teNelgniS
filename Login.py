#!/usr/bin/env python
# coding=utf-8

import sys
import ConfigParser
import platform
import utils

# copy from https://github.com/nowind/sx_pi/
# changed by Hakurei Sino


if __name__ == '__main__':
     print("using "+platform.system()+" mode!")
     
     if platform.system() == "Linux":
          import linuxTools as sEnv
     elif platform.system() == "Windows":
          import winTools as sEnv
     elif platform.system() == "Mac":
          import macTools as sEnv
     else:
          print("Unsupport os")
          
     if len(sys.argv) > 1:
          cf = ConfigParser.ConfigParser()
          cf.read("singleNet.conf")
          mUsername = cf.get("config", "username")
          mPassword = cf.get("config", "password")
          if sys.argv[1] == "1":
               mpin = utils.calc_pin(mUsername, mPassword)
               sEnv.connectWired(mUsername, mPassword, mpin)
          elif sys.argv[1] == "2":
	       wlanip = ""
               wlanip = sEnv.getIp()
	       if wlanip == "":
                    print("wlan device not found or error in found ip address")
	       else:
		    passRes = utils.execCmd("java EncryptPassword "+mPassword)
		    utils.connectWireless(mUsername, passRes, wlanip)
          else:
		print("Paramter error 1 for wired connect 2 for wireless connect")
     else:
          	print("Paramter error 1 for wired connect 2 for wireless connect")
