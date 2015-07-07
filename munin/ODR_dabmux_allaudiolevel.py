#!/usr/bin/env python2
#
# present statistics from dabmux Stats Server
# to munin

import sys
import json
import socket
import os

SOCK_RECV_SIZE = 10240

config_template = """
multigraph audio_levels_{ident}
graph_title Contribution {ident} audio level (peak)
graph_order left right
graph_args --base 1000
graph_vlabel peak audio level during last ${{graph_period}}
graph_category encoders
graph_info This graph shows the audio level of both channels of the {ident} ZMQ input

left.info Left channel audio level
left.label Left channel audio level
left.min -90
left.max 0
left.warning -40:0
left.critical -80:0
right.info Right channel audio level
right.label Right channel audio level
right.min -90
right.max 0
right.warning -40:0
right.critical -80:0
"""

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

	def getConfig(self):
		self.sock.send("config\n")
		config = json.loads(self.sock.recv(SOCK_RECV_SIZE))
		
		munin_config = ""
		for conf in config['config']:
			munin_config += config_template.format(ident=conf)
		return munin_config
		
	def getValues(self):
		self.sock.send("values\n")
		values = json.loads(self.sock.recv(SOCK_RECV_SIZE))['values']

		munin_values = ""
		for ident in values:
			v = values[ident]['inputstat']
			#munin_values += "multigraph buffers_{ident}\n".format(ident=ident)
			#munin_values += "high.value {}\n".format(v['max_fill'])
			#munin_values += "low.value {}\n".format(v['min_fill'])
			#munin_values += "multigraph over_underruns_{ident}\n".format(ident=ident)
			#munin_values += "underruns.value {}\n".format(v['num_underruns'])
			#munin_values += "overruns.value {}\n".format(v['num_overruns'])
			munin_values += "multigraph audio_levels_{ident}\n".format(ident=ident)
			munin_values += "left.value {}\n".format(v['peak_left'])
			munin_values += "right.value {}\n".format(v['peak_right'])
		return munin_values
    
if __name__ == "__main__":
	app = App()
	
	if len(sys.argv) == 2 and sys.argv[1] == "autoconf":
			print "yes"
	elif len(sys.argv) == 2 and sys.argv[1] == "config":
			print app.getConfig()
	else:
			print app.getValues()



