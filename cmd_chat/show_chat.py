#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import os
from sys import argv

os.system("CLS")
IP, PORT = argv[1], argv[2]

sock = socket.socket()
sock.connect((IP, int(PORT)))
sock.setblocking(False)

os.system("CLS")
print("==== CHAT =====")

while True:
	try: data = sock.recv(1024)
	except BlockingIOError: continue
	data = data.decode()
	if data.startswith("/newuser"):
		print("            {} connected!".format(data.split(" ")[1]))
		continue
	print(data)

sock.close()