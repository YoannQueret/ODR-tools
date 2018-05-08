#!/usr/bin/python -u

# https://github.com/nagius/snmp_passpersist
# pip install snmp_passpersist

# add to snmpd.conf :
# pass_persist   .1.3.6.1.4.1.51436.1 /usr/bin/env python -u /usr/local/bin/ODR-DabMux_PassPersist.py

import sys
import json
import zmq
import os
import argparse
import snmp_passpersist as snmp

import syslog, sys, time, errno

ctx = zmq.Context()

def connect(port):
    """Create a connection to the dabmux stats server
    returns: the socket"""

    sock = zmq.Socket(ctx, zmq.REQ)
    sock.connect("tcp://localhost:%s" % (port))

    return sock


def update_data():
    sock = connect(cli_args.port)

    # get version
    sock.send("info")
    info = json.loads(sock.recv())
    pp.add_int('1.0', cli_args.port)
    pp.add_str('2.0', info['version'])
    
    # get inputTable values
    sock.send("values")
    values = json.loads(sock.recv())

    inputState = []
    for ident in values['values']:
        v = values['values'][ident]['inputstat']
        inputState.append( v['state'][v['state'].find("(")+1:v['state'].find(")")] )
    pp.add_int('3.0', min(inputState))


    idx=1
    for ident in values['values']:
        v = values['values'][ident]['inputstat']
        syslog.syslog(syslog.LOG_INFO,"pp.add %s" % (int(idx)))
        
        pp.add_int('10.1.1.'+str(idx), int(idx))
        pp.add_str('10.1.2.'+str(idx), str(ident))

        pp.add_int('10.1.3.'+str(idx), v['num_underruns'])
        pp.add_int('10.1.4.'+str(idx), v['num_overruns'])

        pp.add_int('10.1.5.'+str(idx), v['state'][v['state'].find("(")+1:v['state'].find(")")])

        pp.add_int('10.1.6.'+str(idx), v['peak_left'])
        pp.add_int('10.1.7.'+str(idx), v['peak_right'])

        pp.add_int('10.1.8.'+str(idx), v['peak_left_slow'])
        pp.add_int('10.1.9.'+str(idx), v['peak_right_slow'])
            
        idx=idx+1
        
    

if __name__ == "__main__":
    # Get configuration file in argument
    parser = argparse.ArgumentParser(description='ODR-DabMux PassPersit')
    parser.add_argument('-o','--oid', help='start oid (example: .1.3.6.1.4.1.51436.1.1)',required=True)
    parser.add_argument('-p','--port', help='state port (example: 12720)',required=True)
    cli_args = parser.parse_args()
    
    syslog.openlog(sys.argv[0],syslog.LOG_PID)
    
    try:
        syslog.syslog(syslog.LOG_INFO,"Starting ODR-DabMux monitoring...")
        pp = snmp.PassPersist(cli_args.oid)
        pp.start(update_data, 30)
    except KeyboardInterrupt:
        print "Exiting on user request."
        sys.exit(0)
    except IOError, e:
        if e.errno == errno.EPIPE:
            syslog.syslog(syslog.LOG_INFO,"Snmpd had close the pipe, exiting...")
            sys.exit(0)
        else:
            syslog.syslog(syslog.LOG_WARNING,"Updater thread as died: IOError: %s" % (e))
    except Exception, e:
        syslog.syslog(syslog.LOG_WARNING,"Main thread as died: %s: %s" % (e.__class__.__name__, e))
    else:
        syslog.syslog(syslog.LOG_WARNING,"Updater thread as died: %s" % (pp.error))
        
    