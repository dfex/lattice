#!/usr/bin/python

## lattice - network topology in sql

import re, sys, getopt
import sqlite3
import junosconnect
from getpass import getpass
from pprint import pprint

def opendb():
	try:
		dbconnection = sqlite3.connect('lattice.sqlite')
		return dbconnection
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)	

def closeDB(dbconnection):
	dbconnection.close()

def reinitdb():
	confirmation = raw_input("Re-initialise lattice db - are you sure? (y/n)")
	if confirmation.upper == 'Y':
		dbconnection = opendb()
		cur = dbconnection.cursor()
		cur.execute("PRAGMA foreign_keys")
		cur.execute("DROP TABLE IF EXISTS CustomerTable;")
		cur.execute("DROP TABLE IF EXISTS UserTable;")
		cur.execute("DROP TABLE IF EXISTS LocationTable;")
		cur.execute("DROP TABLE IF EXISTS NodeTable;")
		cur.execute("DROP TABLE IF EXISTS PortTable;")
		cur.execute("DROP TABLE IF EXISTS ServiceTable;")
		cur.execute("DROP TABLE IF EXISTS SubInterfaceTable;")
		cur.execute("DROP TABLE IF EXISTS AuthorisationTable;")
		cur.execute("DROP TABLE IF EXISTS ServiceMappingTable;")
		cur.execute("DROP TABLE IF EXISTS TransactionLog;")
		# switch this across to a dict/array-based description of the db and load it in. 
		cur.execute("CREATE TABLE CustomerTable (CustomerID INTEGER PRIMARY KEY ASC, CustomerName TEXT, BillingEmailAddress TEXT, CustomerStatus TEXT);")
		cur.execute("CREATE TABLE UserTable (UserID INTEGER PRIMARY KEY ASC, UserName TEXT, UserPassword TEXT, UserStatus TEXT);")
		cur.execute("CREATE TABLE LocationTable (LocationID INTEGER PRIMARY KEY ASC, LocationName TEXT NOT NULL, RackID TEXT, RackUnit INTEGER, FacilityName TEXT NOT NULL, FacilityFloor TEXT, FacilityAddress TEXT NOT NULL, FacilityState TEXT NOT NULL, FacilityCountry TEXT NOT NULL, LocationStatus TEXT NOT NULL);")
		cur.execute("CREATE TABLE NodeTable (NodeID INTEGER PRIMARY KEY ASC, NodeName TEXT NOT NULL, NodeType TEXT NOT NULL, NodeIPAddress TEXT NOT NULL, LocationID INTEGER, NodeStatus TEXT, FOREIGN KEY(LocationID) REFERENCES LocationTable(LocationID));")
		cur.execute("CREATE TABLE PortTable (PortID INTEGER PRIMARY KEY ASC, PortName TEXT NOT NULL, PortStatus TEXT, PortSpeed INTEGER, CustomerID TEXT, NodeID INTEGER, FOREIGN KEY(NodeID) REFERENCES NodeTable(NodeID));")
		cur.execute("CREATE TABLE ServiceTable (ServiceID INTEGER PRIMARY KEY ASC, ServiceName TEXT NOT NULL, ServiceType TEXT NOT NULL, ServiceRouteTarget TEXT, ServiceRouteDistinguisher TEXT);")
		cur.execute("CREATE TABLE SubInterfaceTable (SubInterfaceID INTEGER PRIMARY KEY ASC, SubInterfaceUnit INTEGER, SubInterfaceVLANID INTEGER, ServiceID INTEGER, SubInterfaceStatus TEXT NOT NULL, PortID INTEGER, FOREIGN KEY(ServiceID) REFERENCES ServiceTable(ServiceID), FOREIGN KEY (PortID) REFERENCES PortTable(PortID));")
		cur.execute("CREATE TABLE AuthorisationTable (CustomerID INTEGER, UserName TEXT, AuthorisationRole TEXT, PortID INTEGER, SubInterfaceID INTEGER, FOREIGN KEY(CustomerID) REFERENCES CustomerTable(CustomerID), FOREIGN KEY(UserName) REFERENCES UserTable(UserName), FOREIGN KEY(PortID) REFERENCES PortTable(PortID), FOREIGN KEY(SubInterfaceID) REFERENCES SubInterfaceTable(SubInterfaceID));")
		cur.execute("CREATE TABLE ServiceMappingTable (ServiceID TEXT, SubInterfaceID TEXT, FOREIGN KEY(ServiceID) REFERENCES ServiceTable(ServiceID), FOREIGN KEY(SubInterfaceID) REFERENCES SubInterfaceTable(SubInterfaceID));")
		cur.execute("CREATE TABLE TransactionLog (TransactionID INTEGER PRIMARY KEY ASC, TransactionTimeStamp TEXT, UserID TEXT, IPAddress TEXT, EventType TEXT, PortID TEXT, SubInterfaceID TEXT, EventDescription TEXT);")
		closedb(dbconnection)
	else:
		return 0	

def usage():
    sys.stdout.write("Error: Missing parameter\n\n")
    sys.stdout.write("Usage: lattice reinit\n")
    sys.stdout.write("Usage: lattice node add <ip address>\n")
    sys.stdout.write("Usage: lattice node delete <ip address>\n")
    sys.stdout.write("Usage: lattice node list\n")
    sys.stdout.write("Usage: lattice service create <service-name> <service type>\n")
    sys.stdout.write("Usage: lattice service delete <id>\n")
    sys.stdout.write("Usage: lattice service attach <service-name> <port> <ID>\n")
    sys.stdout.write("Usage: lattice service detach <service-name> <port> <ID>\n")
    sys.stdout.write("Usage: lattice service list\n")
    sys.stdout.write("Usage: lattice subinterface create <node> <port> <ID>\n")
    sys.stdout.write("Usage: lattice subinterface delete <node> <port> <ID>\n")
    sys.stdout.write("Usage: lattice subinterface list\n")
    sys.stdout.write("\n")

def main(argv):
    sys.stdout.write("lattice\n\n")
    latticeFunction=''
    if len(sys.argv) <= 1:
        usage()
        exit(1)
    else:
        latticeFunction = sys.argv[1]
    if latticeFunction == 'reinit':
        reinitdb()
    else:
        usage()
    #case (sys.argv[1]):
    #	"reinit":
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
	# node list
	# - output list of nodes
	# - privileged exec only!
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