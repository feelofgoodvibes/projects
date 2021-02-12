#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket
import threading

os.system("cls")

users = []			# List of active users

# Check for new connections
def conn_check():
	while True:
		try:
			conn, addr = sock.accept()
			print('New connection: ', addr)
			users.append(conn)
		except BlockingIOError: pass

# Waiting for new messages
def sock_read():
	while True:
		data = []
		for u in users:
			try:
				user_data = u.recv(1024)
			except BlockingIOError: continue
			except (ConnectionAbortedError, ConnectionResetError):
				print('someone exited :(')
				users.remove(u)
				for x in users: x.send("someone exited".encode())

			if user_data: data.append(user_data)

		for x in data:
			print("Got", x)
			print(len(users))
		for u in users:
			for x in data: u.send(x)

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 31789))
sock.listen(6)
sock.setblocking(False)

print("Server ip:", socket.gethostbyname(socket.gethostname()))
print("Server port: 31789")

connection_check_thread = threading.Thread(target = conn_check)		# Connection-waiting thread
socket_read_thread = threading.Thread(target = sock_read)			# Messages-waiting thread

connection_check_thread.start()
socket_read_thread.start()