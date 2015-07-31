#!/usr/bin/env python2
#

import sys
import json
import socket
import os

SOCK_RECV_SIZE = 10240

def connect():
	"""Create a connection to the dabmux stats server
	returns: the socket"""

	sock = socket.socket()
	sock.connect(("localhost", 12720))

	version = json.loads(sock.recv(SOCK_RECV_SIZE))

	if not version['service'].startswith("ODR-DabMux"):
		sys.stderr.write("Wrong version\n")
		sys.exit(1)

	return sock


class App:
	global config_template
	def __init__(self):
		self.sock = connect()

	def getValues(self):
		self.sock.send("values\n")
		values = json.loads(self.sock.recv(SOCK_RECV_SIZE))['values']

		value = ""
		for ident in values:
			v = values[ident]['inputstat']
			value += "{ident}\n".format(ident=ident)
			value += "left: {}\n".format(v['peak_left'])
			value += "right: {}\n".format(v['peak_right'])
		return value
    
if __name__ == "__main__":
	app = App()
	print app.getValues()
