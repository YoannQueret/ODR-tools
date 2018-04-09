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

muxs=[ { 'name': 'MUX 1', 'port': '12720' } ]

def connect(port):
    """Create a connection to the dabmux stats server
    returns: the socket"""

    sock = zmq.Socket(ctx, zmq.REQ)
    sock.connect("tcp://localhost:%s" % (port))

    return sock


def update():
    
    # - time : 1.0
    pp.add_str('1.0', 'datetime')
    
    # - muxtable : 10.
    muxIDX=1
    for mux in muxs:
        pp.add_int('10.1.1.'+str(muxIDX), int(muxIDX))
        pp.add_str('10.1.2.'+str(muxIDX), str(mux['name']))
        pp.add_int('10.1.3.'+str(muxIDX), mux['port'])
        
        # Connect to mux statsPort
        sock = connect(mux['port'])
        
        ## get version
        sock.send("info")
        infoValues = json.loads(sock.recv())
        pp.add_str('10.1.4.'+str(muxIDX), infoValues['version'])
        
        # get inputTable values
        sock.send("values")
        inputValues = json.loads(sock.recv())
        
        inputState = []
        inputIDX=1
        for ident in inputValues['values']:
            v = inputValues['values'][ident]['inputstat']
            
            inputState.append( v['state'][v['state'].find("(")+1:v['state'].find(")")] )
            
            pp.add_int('10.1.20.'+str(muxIDX)+'.1.'+str(inputIDX), int(inputIDX))
            pp.add_str('10.1.20.'+str(muxIDX)+'.2.'+str(inputIDX), str(ident))
            
            pp.add_int('10.1.20.'+str(muxIDX)+'.3.'+str(inputIDX), v['num_underruns'])
            pp.add_int('10.1.20.'+str(muxIDX)+'.4.'+str(inputIDX), v['num_overruns'])
            
            pp.add_int('10.1.20.'+str(muxIDX)+'.5.'+str(inputIDX), v['state'][v['state'].find("(")+1:v['state'].find(")")])
            
            pp.add_int('10.1.20.'+str(muxIDX)+'.6.'+str(inputIDX), v['peak_left'])
            pp.add_int('10.1.20.'+str(muxIDX)+'.7.'+str(inputIDX), v['peak_right'])
            
            pp.add_int('10.1.20.'+str(muxIDX)+'.8.'+str(inputIDX), v['peak_left_slow'])
            pp.add_int('10.1.20.'+str(muxIDX)+'.9.'+str(inputIDX), v['peak_right_slow'])
            
            inputIDX=inputIDX+1
        
        pp.add_int('10.1.5.'+str(muxIDX), min(inputState))
        
        muxIDX=muxIDX+1

pp = snmp.PassPersist('.1.3.6.1.4.1.51436.1')
pp.start(update, 30)