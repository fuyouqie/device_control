#!/usr/bin/env python

import telnetlib
from multiprocessing import Pool

class UserCreds:
	dev_1 = {'host':'10.0.20.1','username':'admin', 'password':'ShiYue753951'}
	dev_2 = {'host':'127.0.0.1','username':'admin', 'password':'cisco'}
	dev_3 = {'host':'127.0.0.1','username':'admin', 'password':'cisco'}
	dev_4 = {'host':'127.0.0.1','username':'admin', 'password':'cisco'}
	dev_5 = {'host':'127.0.0.1','username':'admin', 'password':'cisco'}
	dev_6 = {'host':'127.0.0.1','username':'admin', 'password':'cisco'}
	dev_7 = {'host':'127.0.0.1','username':'admin', 'password':'cisco'}
	dev_8 = {'host':'127.0.0.1','username':'admin', 'password':'cisco'}
	dev_9 = {'host':'127.0.0.1','username':'admin', 'password':'cisco'}
	dev_10 = {'host':'127.0.0.1','username':'admin', 'password':'cisco'}

commands=['config wlan disable 2','save config']

def telnet_nego(session, negotiation):
    sock = session.get_socket()
    if sock is not None:
        sock.send(negotiation)

def do_telnet(host, username, password, commands):
	tn=telnetlib.Telnet(host.encode('utf-8'),timeout=10)
	telnet_nego(tn, telnetlib.IAC + telnetlib.WILL + telnetlib.SGA)
	tn.read_until(b'User: ', timeout=5)
	#y=tn.read_until(b'User:', timeout=5)
	#print(y.decode())
	tn.write((username + '\n').encode('utf-8'))
	#tn.write(('\n').encode('utf-8'))
	tn.read_until(b'Password:', timeout=5)
	#x=tn.read_until(b'Password:', timeout=5)
	#print(x.decode())
	tn.write((password + '\n').encode('utf-8'))
	for command in commands:
		tn.read_until(b'>', timeout=5)
		tn.write((command + '\n').encode('utf-8'))
	#tn.read_until(b'>',timeout=5)
	tn.read_until(b') ', timeout=5)
	tn.write(('y').encode('utf-8'))
	tn.close()

proc_pool = Pool(10)

for i in range(1,11):
	exec('dev=UserCreds.dev_{}'.format(i))
	host=dev['host']
	username=dev['username']
	password=dev['password']
	proc_pool.apply_async(func=do_telnet, args=(host, username, password, commands))

proc_pool.close()
proc_pool.join()
