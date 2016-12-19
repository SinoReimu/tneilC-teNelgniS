#!/usr/bin/env python
# coding=utf-8
import re
import time
import struct
import hashlib
import sys
import os
import time
import ConfigParser
import socket
import requests

# copy from https://github.com/nowind/sx_pi/
# changed by Hakurei Sino
def connectWireless(ipAddress):
     headers = {'User-Agent': 'China Telecom Client'}
     payload = {'wlanuserip': ipAddress}
     url = 'http://115.239.134.163:8080/showlogin.do'
     r = requests.post(url, data=payload, headers=headers)
     print(r)
     
def execCmd(cmd):  
    r = os.popen(cmd)  
    text = r.read()  
    r.close()  
    return text

def newRas():
     print("Build the Dial Now")
     os.system("newDial.vbs")
     time.sleep(2)
     
def cur_file_dir():
     path = sys.path[0]
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

def calc_pin(username, password, dname, share_key=None, timestamp=None, prefix='\x0D\x0A'):
    share_key = 'singlenet01'
    username = username.upper()

    timestamp = int(timestamp or time.time())
    time_div_by_five = timestamp / 5

    time_hash = [0] * 4
    for i in xrange(4):
        for j in xrange(8):
            time_hash[i] = time_hash[i] + (((time_div_by_five >> (i + 4 * j)) & 1) << (7 - j))

    pin27_byte = [0] * 8
    pin27_byte[0] = ((time_hash[0] >> 2) & 0x3F)
    pin27_byte[1] = ((time_hash[0] & 0x03) << 4 & 0xff) | ((time_hash[1] >> 4) & 0x0F)
    pin27_byte[2] = ((time_hash[1] & 0x0F) << 2 & 0xff) | ((time_hash[2] >> 6) & 0x03)
    pin27_byte[3] = time_hash[2] & 0x3F
    pin27_byte[4] = ((time_hash[3] >> 2) & 0x3F)
    pin27_byte[5] = ((time_hash[3] & 0x03) << 4 & 0xff)
    for i in xrange(6):
        pin27_byte[i] = {True: (pin27_byte[i] + 0x20) & 0xff,
                         False: (pin27_byte[i] + 0x21) & 0xff}[((pin27_byte[i] + 0x20) & 0xff) < 0x40]

    pin27_str = ''
    for i in xrange(6):
        pin27_str = pin27_str + chr(pin27_byte[i])

    before_md5 = struct.pack('>I', time_div_by_five) + username.split('@')[0] + share_key
    pin89_str = hashlib.md5(before_md5).hexdigest()[0:2]
    pin = pin27_str + pin89_str
    cmd = cur_file_dir()+'\\createADSL.exe "'+pin+'" "'+username+'" "'+password+'" "'+dname+'"'
    #cmd = 'C:\Users\Administrator\Desktop\createADSL.exe "'+pin+'" "'+username+'" "'+password+'"'
    #print(cmd)
    os.system(cmd)
    print("Finish wired connect.")

if __name__ == '__main__':
     if len(sys.argv) > 1:
          cf = ConfigParser.ConfigParser()
          cf.read("singleNet.conf")
          mUsername = cf.get("config", "username")
          mPassword = cf.get("config", "password")
          if sys.argv[1] == "1":
               if not cf.has_option("config", "built"):
                    newRas()
                    cf.set("config", "built", "1")
                    f = open('singleNet.conf','w')
                    cf.write(f)
               print("will do login for account:" + mUsername)
               calc_pin(mUsername, mPassword, "HSingleNet")
          elif sys.argv[1] == "2":
               print(socket.gethostbyname(socket.gethostname()))
               result = execCmd("java EncryptPassword 123123")
               print(result)
               pass
          else:
               print("Paramter error 1 for wired connect 2 for wireless connect")
     else:
          print("Paramter error 1 for wired connect 2 for wireless connect")
     pass
