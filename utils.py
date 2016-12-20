#!/usr/bin/env python
# coding=utf-8

import struct
import os
import requests
import time
import hashlib

#Module : Common utils of connect singlenet

def execCmd(cmd):  
    r = os.popen(cmd)  
    text = r.read()  
    r.close()  
    return text

def connectWireless(username, password, ipAddress):
     headers = {'User-Agent': 'China Telecom Client'}
     payload = {'wlanuserip': ipAddress}
     url = 'http://115.239.134.163:8080/showlogin.do'
     r = requests.post(url, data=payload, headers=headers)
     if not r.status_code == 200:
	print("Connect with auth server failed")
	return
     uuidl = re.findall("<Uuid>(.*)</Uuid>", r.text)
     if len(uuidl) == 0:
	print("Get uuid error")
	return
     uuid = uuidl[0]
     loginURLl = re.findall("<LoginURL>(.*)</LoginURL>", r.text)
     if len(loginURLl) == 0:
	print("get loginURL error")
	return
     loginURL = loginURLl[0]
     payload2 = {
	'username': username,
	'password': password,
	'ratingtype': 1,
	'uuid': uuid
     }
     r = requests.post(loginURL, data=payload2, headers=headers)
     codel = re.findall("<ResponseCode>(.*)</ResponseCode>", r.text)
     if len(codel) == 0:
	print("get return code error")
	return
     coder = codel[0]
     print("return code = "+coder)

def calc_pin(username, password, share_key=None, timestamp=None, prefix='\x0D\x0A'):
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
    return pin
