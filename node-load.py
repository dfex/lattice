#!/usr/bin/python

## node-load - import device interfaces into sqlite db

import re, sys, getopt
from jnpr.junos import Device
from jnpr.junos.op.ethport import EthPortTable
from getpass import getpass
from pprint import pprint

##def openNode():
	## 

##def closeNode():
	##
	
##def retrievePorts():
	##
	
##def openNodeDB():
	##

##def closeNodeDB():
	##


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
		
		dev.close()
	else:	
		sys.stdout.write("x")
		sys.stdout.flush()
		deviceInventory.append({"IP Address":str(hostAddress).rstrip('\n'),"Serial Number":"IP Address Error","Model":"N/A"})

if __name__ == "__main__":
   main(sys.argv[1:])