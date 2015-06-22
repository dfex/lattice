#!/usr/bin/python

## node-load - import node interfaces into sqlite db

import re, sys, getopt
import sqlite3
from jnpr.junos import Device
from jnpr.junos.op.ethport import EthPortTable
from getpass import getpass
from pprint import pprint


def initialiseDB(dbconnection):
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
	cur.execute("CREATE TABLE CustomerTable (CustomerID INTEGER PRIMARY KEY ASC, CustomerName TEXT, BillingEmailAddress TEXT, CustomerStatus TEXT);")
	cur.execute("CREATE TABLE UserTable (UserID INTEGER PRIMARY KEY ASC, UserName TEXT, UserPassword TEXT, UserStatus TEXT);")
	cur.execute("CREATE TABLE LocationTable (LocationID INTEGER PRIMARY KEY ASC, LocationName TEXT NOT NULL, RackID TEXT, RackUnit INTEGER, FacilityName TEXT NOT NULL, FacilityFloor TEXT, FacilityAddress TEXT NOT NULL, FacilityState TEXT NOT NULL, FacilityCountry TEXT NOT NULL, LocationStatus TEXT NOT NULL);")
	cur.execute("CREATE TABLE NodeTable (NodeID INTEGER PRIMARY KEY ASC, NodeName TEXT NOT NULL, NodeType TEXT NOT NULL, NodeIPAddress TEXT NOT NULL, LocationID INTEGER NOT NULL, NodeStatus TEXT NOT NULL, FOREIGN KEY(LocationID) REFERENCES LocationTable(LocationID));")
	cur.execute("CREATE TABLE PortTable (PortID INTEGER PRIMARY KEY ASC, PortName TEXT NOT NULL, PortStatus TEXT, PortSpeed INTEGER, CustomerID TEXT, NodeID INTEGER, FOREIGN KEY(NodeID) REFERENCES NodeTable(NodeID));")
	cur.execute("CREATE TABLE ServiceTable (ServiceID INTEGER PRIMARY KEY ASC, ServiceName TEXT NOT NULL, ServiceType TEXT NOT NULL, ServiceRouteTarget TEXT, ServiceRouteDistinguisher TEXT);")
	cur.execute("CREATE TABLE SubInterfaceTable (SubInterfaceID INTEGER PRIMARY KEY ASC, SubInterfaceUnit INTEGER, SubInterfaceVLANID INTEGER, ServiceID INTEGER, SubInterfaceStatus TEXT NOT NULL, PortID INTEGER, FOREIGN KEY(ServiceID) REFERENCES ServiceTable(ServiceID), FOREIGN KEY (PortID) REFERENCES PortTable(PortID));")
	cur.execute("CREATE TABLE AuthorisationTable (CustomerID INTEGER, UserName TEXT, AuthorisationRole TEXT, PortID INTEGER, SubInterfaceID INTEGER, FOREIGN KEY(CustomerID) REFERENCES CustomerTable(CustomerID), FOREIGN KEY(UserName) REFERENCES UserTable(UserName), FOREIGN KEY(PortID) REFERENCES PortTable(PortID), FOREIGN KEY(SubInterfaceID) REFERENCES SubInterfaceTable(SubInterfaceID));")
	cur.execute("CREATE TABLE ServiceMappingTable (ServiceID TEXT, SubInterfaceID TEXT, FOREIGN KEY(ServiceID) REFERENCES ServiceTable(ServiceID), FOREIGN KEY(SubInterfaceID) REFERENCES SubInterfaceTable(SubInterfaceID));")
	cur.execute("CREATE TABLE TransactionLog (TransactionID INTEGER PRIMARY KEY ASC, TransactionTimeStamp TEXT, UserID TEXT, IPAddress TEXT, EventType TEXT, PortID TEXT, SubInterfaceID TEXT, EventDescription TEXT);")
	return cur

def getNodeInventory(node):
	# Need to fix this so that it aligns with nodeTable better
	nodeInventory = []
	nodeInventory.append({"Serial Number":node.facts['serialnumber'],"Model":node.facts['model']})
	return nodeInventory

def getPortInventory(node):
	portInventory = EthPortTable(node)
	portInventory.get()
	return portInventory
	
def openDB():
	try:
		dbconnection = sqlite3.connect('lattice.db')
		return dbconnection
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)	

def closeDB(dbconnection):
	dbconnection.close()

def openNode(hostAddress, username, password):
	if password != '':
		node = Device(host=hostAddress.rstrip('\n'),user=username,passwd=password)
	else:
		node = Device(host=hostAddress.rstrip('\n'),user=username)
	node.open()
	return node
	
def closeNode(node):
	node.close()
	
def main(argv):
	sys.stdout.write("node-load\n\n")
	
	# Handle parameter
	inetRegex = re.compile("^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-1][0-9]|22[0-3])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$") 
	if len(sys.argv) != 2:
		sys.stdout.write("Error: Missing parameter\n")
		sys.stdout.write("Usage: node-load <node IP address>\n")
		sys.exit()
	elif not(inetRegex.match(sys.argv[1])):
		sys.stdout.write("Error: Invalid IP Address\n")
		sys.stdout.write("Usage: node-load <node IP address>\n")
		sys.exit()
				
	# Open connection to db		    
	dbcon = openDB()
	cur = initialiseDB(dbcon)
		
	username = raw_input('Username: ')
	password = getpass('Password (leave blank to use SSH Key): ')

	# Open device, retrieve Serial Number and Model
	node = openNode(sys.argv[1], username, password)
	nodeInventory = getNodeInventory(node)
		
	# storeDeviceInventory - write to node table
		
	print "Serial Number ", nodeInventory[0]['Serial Number']
	print "Model         ", nodeInventory[0]['Model']
	
	cur.execute("INSERT INTO NodeTable(NodeName, NodeType, NodeIPAddress) VALUES(?, ?, ?)",(node.hostname, nodeInventory[0]['Model'], sys.argv[1]))
	
	#storePortInventory - retrieve port information and write to port table
	
	portInventory = getPortInventory(node)
		
	print "Interfaces:"
	for port in portInventory:
		print port.name
		cur.execute("INSERT INTO PortTable(PortName) VALUES(?)",(port.name,))
	dbcon.commit()

	closeNode(node)
	closeDB(dbcon)

if __name__ == "__main__":
   main(sys.argv[1:])