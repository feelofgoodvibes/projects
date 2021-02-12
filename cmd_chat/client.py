#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys
import os
from time import strftime
import subprocess

def send_message(text):
	try: sock.send(text.encode())
	except ConnectionResetError:
		print("Chat is shutted down\n\npress any key to close...")
		os.system("pause>nul")
		sys.exit()

# Open chat window
def showchat():
	os.system(f"start show_chat.py {IP} {PORT}")

os.system("CLS")
IP = input("IP: ")      # localhost
PORT = input("PORT: ")  # 9090
sock = socket.socket()
sock.connect((IP, int(PORT)))

nickname = None
while not nickname:
	nickname = input("Enter your nickname: ")
	if len(nickname) > 15:
		print("Too long! (Max. 15)")
		nickname = None

os.system("CLS")
print("===== Welcome to chat, {}! =====\n(to open chat window, type \"/showchat\" as message)\n".format(nickname))
send_message("/newuser {}".format(nickname))
showchat()

while True:
	msg = input("Enter message: ")
	msg = f"[{strftime('[%H:%M:%S]')}] {nickname}: {msg}"
	send_message(msg)

sock.close()