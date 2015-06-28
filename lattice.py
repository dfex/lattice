#!/usr/bin/python

## node-load - import node interfaces into sqlite db

import re, sys, getopt
import sqlite3
import junosconnect
from getpass import getpass
from pprint import pprint

	
def main(argv):
	sys.stdout.write("node-load\n\n")
	
	# Handle parameter
	# reinit
	# - prompt (are you sure?)
	# - re-initialise the lattice database
	# - privileged exec only!
	# node add 192.168.100.100 
	# - prompt for user/pass and add node to db
	# - import ports and add to db (decide on delimeter for uplinks vs revenue ports.. pic 0 only?)
	# node delete 192.168.100.100
    # - check dependencies (attached sub-interfaces) - fail with list of attached sub-interfaces in hierarchical manner
    # - remove sub-interfaces from services (and delete services?) in db
    # - push config to the switch to do the same
    # - remote ports from node
	# - remove node from db
	# service create <vlan> <name> <ID>
	# service create <vxlan> <name> <ID>..
	# service create <l2vpn> <name> <ID>..
	# service create <vpls> <name> <ID>..
	# service create <evpn> <name> <ID>..
	# service <name> create <vlan> <ID> ??
	# - create reference to service in db (with parameters and owner)
	# service attach <node> <port> <ID>
	# - create service attachment reference in db
	# - push configuration to node and bind port to service
	# service detach <node> <port> <ID>
	# - remove configuration from node and unbind port from service
	# - remove service attachment reference in db
	# service list [<port> <ID>]
	# - no parameters: show all "owned services" - recurse through attached sub-interfaces
	# - port: show all services attached to port
	# - port, id: show service attached to port/ID combination
	# subinterface create <node> <port> <ID> 
	# - create sub-interface reference in db
	# - push config to node and build logical interface
    # subinterface delete <node> <port> <ID>
	# - check dependencies (attached services) - fail with list of attached services
    # - remove config from node for logical interface
    # - remove subinterface from db
    # subinterface list [<node> <port> <ID>]
    # - no parameters: show all "owned" sub-interfaces
    # - <node>: show all "owned" sub-interfaces attached to a node
    # - <node>, <port>: show all "owned" sub-interfaces attaches to <node>, <port>
    # - <node>, <port>, <ID>: show "owned" sub-interface at <node>, <port>, <id>
	
	
if __name__ == "__main__":
   main(sys.argv[1:])