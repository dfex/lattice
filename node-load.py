#!/usr/bin/python

## node-load - import device interfaces into sqlite db

import re, sys, getopt
import sqlite3
from jnpr.junos import Device
from jnpr.junos.op.ethport import EthPortTable
from getpass import getpass
from pprint import pprint


def populateDB(dbconnection):
	cur = dbconnection.cursor()    

	cur.execute('DROP TABLE IF EXISTS PortTable')
	cur.execute('CREATE TABLE CustomerTable (CustomerID INTEGER PRIMARY KEY ASC, CustomerName TEXT, BillingEmailAddress TEXT, CustomerStatus TEXT)')
	cur.execute('CREATE TABLE UserTable (UserID INTEGER PRIMARY KEY ASC, UserName TEXT, UserPassword TEXT, UserStatus TEXT)')
	cur.execute('CREATE TABLE LocationTable (LocationID INTEGER PRIMARY KEY ASC, LocationName TEXT NOT NULL, RackID TEXT, RackUnit INTEGER, FacilityName TEXT NOT NULL, FacilityFloor TEXT, FacilityAddress TEXT NOT NULL, FacilityState TEXT NOT NULL, Facility Country TEXT NOT NULL, LocationStatus TEXT NOT NULL)')
    cur.execute('CREATE TABLE NodeTable (NodeID INTEGER PRIMARY KEY ASC, NodeName TEXT NOT NULL, NodeType TEXT NOT NULL, NodeIPAddress TEXT NOT NULL, FOREIGN KEY(LocationID) REFERENCES LocationTable(LocationID), NodeStatus TEXT NOT NULL)')
	cur.execute('CREATE TABLE PortTable (PortID INTEGER PRIMARY KEY ASC, PortName TEXT NOT NULL, PortStatus TEXT, PortSpeed INTEGER, FOREIGN KEY(CustomerID REFERENCES CustomerTable(CustomerID), FOREIGN KEY(NodeID) REFERENCES NodeTable(NodeID))')
    cur.execute('CREATE TABLE ServicesTable (ServiceID INTEGER PRIMARY KEY ASC, ServiceName TEXT NOT NULL, ServiceType TEXT NOT NULL, ServiceRouteTarget TEXT, ServiceRouteDistinguisher TEXT)')
    cur.execute('CREATE TABLE SubInterfaceTable (SubInterfaceID INTEGER PRIMARY KEY ASC, SubInterfaceUnit INTEGER, SubInterfaceVLANID INTEGER, FOREIGN KEY(ServiceID) REFERENCES ServiceTable(ServiceID), SubInterfaceStatus TEXT NOT NULL, FOREIGN KEY(PortID) REFERENCES ServiceTable(PortID)')
    cur.execute('CREATE TABLE AuthorisationTable (FOREIGN KEY(CustomerID) REFERENCES CustomerTable(CustomerID), FOREIGN KEY(UserID TEXT) REFERENCES UserTable(Username), AuthorisationRole TEXT, FOREIGN KEY(PortID) REFERENCES PortTable(PortID), FOREIGN KEY(SubInterfaceID) REFERENCES SubInterfaceTable(SubInterfaceID)')
	cur.execute('CREATE TABLE ServiceMappingTable (FOREIGN KEY(ServiceID) REFERENCES ServiceTable(ServiceID), FOREIGN KEY(SubInterfaceID) REFERENCES SubInterfaceTable(SubInterfaceID))')
	cur.execute('CREATE TABLE TransactionLog (TransactionID INTEGER PRIMARY KEY ASC, TransactionTimeStamp TEXT, FOREIGN KEY(UserID) REFERENCES UserTable(UserID), IPAddress TEXT, EventType TEXT, FOREIGN KEY(PortID) REFERENCES PortTable(PortID), FOREIGN KEY(SubInterfaceID) REFERENCES SubInterfaceTable(SubInterfaceID), EventDescription TEXT)')

def main(argv):
	sys.stdout.write("node-load\n\n")
	if len(sys.argv) != 2:
		sys.stdout.write("Error: Missing parameter\n")
		sys.stdout.write("Usage: node-load <node IP address>\n")
		sys.exit()
	
	username = raw_input('Username: ')
	password = getpass('Password (leave blank to use SSH Key): ')
	sys.stdout.write(". - success\n")
	sys.stdout.write("x - error\n")

	deviceInventory = []
	dbcon = None
	
	# Open connection to db
	try:
		dbcon = sqlite3.connect('lattice.db')
    
    	populateDB(dbcon)
		# Regex for routable IP addresses (1.0.0.0-223.255.255.255)
		inetRegex = re.compile("^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-1][0-9]|22[0-3])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$") 
		hostAddress = sys.argv[1]

		# Open device, retrieve Serial Number and Model
		if inetRegex.match(str(hostAddress)):
			sys.stdout.write('.')
			sys.stdout.flush()
			if password != '':
				dev = Device(host=hostAddress.rstrip('\n'),user=username,passwd=password)
			else:
				dev = Device(host=hostAddress.rstrip('\n'),user=username)
			dev.open()	
			deviceInventory.append({"IP Address":str(hostAddress).rstrip('\n'),"Serial Number":dev.facts['serialnumber'],"Model":dev.facts['model']})
			print "\nIP Address    ", deviceInventory[0]['IP Address'] 
			print "Serial Number ", deviceInventory[0]['Serial Number']
			print "Model         ", deviceInventory[0]['Model']
			portInventory = EthPortTable(dev)
			portInventory.get()
			count = 0
			# Dump interfaces
			print "Interfaces:"
			for port in portInventory:
				print port.name
				cur.execute("INSERT INTO PortTable(PortName) VALUES(?)",(port.name,))
			dbcon.commit()
			dev.close()
		else:	
			sys.stdout.write("x")
			sys.stdout.flush()
			deviceInventory.append({"IP Address":str(hostAddress).rstrip('\n'),"Serial Number":"IP Address Error","Model":"N/A"})

	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)	
	
	finally:
		if dbcon:
			dbcon.close()

if __name__ == "__main__":
   main(sys.argv[1:])