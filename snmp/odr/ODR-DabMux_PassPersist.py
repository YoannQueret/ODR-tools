#!/usr/bin/python -u

# https://github.com/nagius/snmp_passpersist
# pip install snmp_passpersist

# add to snmpd.conf :
# pass_persist   .1.3.6.1.4.1.51436.1 /usr/bin/env python -u /usr/local/bin/ODR-DabMux_PassPersist.py

import sys
import json
import zmq
import os
import snmp_passpersist as snmp

ctx = zmq.Context()

def connect():
    """Create a connection to the dabmux stats server
    returns: the socket"""

    sock = zmq.Socket(ctx, zmq.REQ)
    sock.connect("tcp://localhost:12720")

    return sock


def update():
    sock = connect()

    # get version
    sock.send("info")
    info = json.loads(sock.recv())
    pp.add_str('1.0', info['version'])

    # get inputTable values
    sock.send("values")
    values = json.loads(sock.recv())

    idx=1
    for ident in values['values']:
        v = values['values'][ident]['inputstat']
        
        pp.add_int('10.1.1.'+str(idx), int(idx))
        pp.add_str('10.1.2.'+str(idx), str(ident))
        
        pp.add_int('10.1.3.'+str(idx), v['num_underruns'])
        pp.add_int('10.1.4.'+str(idx), v['num_overruns'])
        
        pp.add_int('10.1.5.'+str(idx), v['state'][v['state'].find("(")+1:v['state'].find(")")])
        
        pp.add_int('10.1.6.'+str(idx), v['peak_left'])
        pp.add_int('10.1.7.'+str(idx), v['peak_right'])
        
        #pp.add_int('10.1.8.'+str(idx), v['peak_left_long'])
        #pp.add_int('10.1.9.'+str(idx), v['peak_right_long'])
        
        idx=idx+1

pp = snmp.PassPersist('.1.3.6.1.4.1.51436.1')
pp.start(update, 30)