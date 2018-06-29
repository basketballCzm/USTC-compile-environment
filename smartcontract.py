# -*- coding: utf-8 -*-
import socket
import os
from multiprocessing import Process
import signal
#import threading
import random
import commands

def tcpcharlink(sock, addr):
	print ("Accept new connection from %s:%s..." % addr)
	count = random.randint(1, 10000)*10000
	while True:
		try:
			# close client connection
			print ('begin recv .....')
			data = sock.recv(10240)
		except:
			break
		filename = 'contract'+str(count)+'.cpp'
		fobject = open(filename, 'w+')
		fobject.write(data)
		fobject.close()
		count = count + 1
		responseData = commands.getstatusoutput(('eosiocpp -o {0}.wast {1}').format(filename,filename))
		#eosiocpp 0 -- Yes   256 --  No 
		if 0 != responseData[0]:
			print ("compile error!")
			sock.send(str(responseData[-1]))
			continue
		responseData = commands.getstatusoutput('/root/my-llvm/llvm-compiler/llvm/build/bin/clang-tidy -checks=-*,-clang-analyzer-*,cppcoreguidelines-pro-bounds-pointer-arithmetic %s'%filename)
		sock.send(str(responseData[-1]))
	sock.close()
	print ("Connection from %s:%s closed." % addr)

def tcpfilelink(sock, addr):
	print ("Accept new file connection from %s:%s..." % addr)
	count = random.randint(1, 10000)*10000
	while True:
		try:
			# close client connection
			print ('begin recv .....')
			data = sock.recv(10240)
		except:
			break
		filename = 'contractpackage'+str(count)+'.zip'
		unfilename = 'contractpackage'+str(count)
		fobject = open(filename, 'w+')
		fobject.write(data)
		fobject.close()
		count = count + 1

		responseData = commands.getstatusoutput(('unzip {0} -d {1}').format(filename,unfilename))
		#unzip 0 -- No   256 --  Yes 
		if 256 != responseData[0]:
			print ("unzip error!")
			sock.send(str(responseData[-1]))
			continue

		filepath = commands.getstatusoutput('pwd')
		userdirname = commands.getstatusoutput('cd {0} && ls'.format(unfilename))
		emptydir = commands.getstatusoutput('cd {0} && cd {1} && ls'.format(unfilename,userdirname[-1]))
		if '' == emptydir[-1]:
			sock.send(str('*.zip file is empty'))
			continue

		responseData = commands.getstatusoutput(('eosiocpp -o {0}/{1}/{2}/{1}.wast {0}/{1}/{2}/*.cpp').format(filepath[-1], unfilename, userdirname[-1]))
		if 0 != responseData[0]:
			print ("compile error!")
			sock.send(str(responseData[-1]))
			continue

		responseData = commands.getstatusoutput('/root/my-llvm/llvm-compiler/llvm/build/bin/clang-tidy -checks=-*,-clang-analyzer-*,cppcoreguidelines-pro-bounds-pointer-arithmetic {0}/{1}/{2}/*.cpp'.format(filepath[-1],unfilename,userdirname[-1]))
		sock.send(str(responseData[-1]))
	sock.close()
	print ("file Connection from %s:%s closed." % addr)

def pfilelink(line, sfile):
	while True:
		sock, addr = sfile.accept();
		p = Process(target=tcpfilelink, args=(sock, addr))
		p.daemon = True
		p.start()

# multiprocessing will automatically handle the zombie process
def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sfile = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#resolve the port be occuped for four minutes
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sfile.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("192.168.118.128",19000))
	sfile.bind(("192.168.118.128",19001))
	s.listen(100)
	sfile.listen(100)
	print ("Waiting for connection...")

	line =1 
	p = Process(target=pfilelink, args=(line ,sfile))
	p.start()

	while True:
		sock, addr = s.accept();
		#t = threading.Thread(target=tcplink, args=(sock, addr));
		p = Process(target=tcpcharlink, args=(sock, addr));
		# 主进程结束完 子进程必须结束
		p.daemon = True
		p.start()

main()