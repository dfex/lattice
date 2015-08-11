#!/usr/bin/python

## lattice - network topology in sql

import re, sys, getopt
import sqlite3
from argh import named, ArghParser, expects_obj
from device_Factory import NodeFactory
import constants
from getpass import getpass
from pprint import pprint
from xor64 import encrypt, decrypt

def open_db():
    try:
        db_connection = sqlite3.connect('lattice.sqlite')
        return db_connection
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)	

def close_db(db_connection):
    db_connection.close()

@named('reinit')
def reinit_db():
    confirmation = raw_input("Re-initialise lattice db - are you sure? (y/n)")
    if confirmation.upper() == 'Y':
        print "Re-initialising db"
        print "Opening db"
        db_connection = open_db()
        print "Opened db"
        cur = db_connection.cursor()
        cur.execute("PRAGMA foreign_keys")
        print "Dropping existing tables"
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
        print "Populating schema"
        cur.execute("CREATE TABLE CustomerTable (CustomerID INTEGER PRIMARY KEY ASC, CustomerName TEXT, BillingEmailAddress TEXT, CustomerStatus TEXT);")
        cur.execute("CREATE TABLE UserTable (UserID INTEGER PRIMARY KEY ASC, UserName TEXT, UserPassword TEXT, UserStatus TEXT);")
        cur.execute("CREATE TABLE LocationTable (LocationID INTEGER PRIMARY KEY ASC, LocationName TEXT NOT NULL, RackID TEXT, RackUnit INTEGER, FacilityName TEXT NOT NULL, FacilityFloor TEXT, FacilityAddress TEXT NOT NULL, FacilityState TEXT NOT NULL, FacilityCountry TEXT NOT NULL, LocationStatus TEXT NOT NULL);")
        cur.execute("CREATE TABLE NodeTable (NodeID INTEGER PRIMARY KEY ASC, NodeName TEXT, NodeType TEXT NOT NULL, NodeIPAddress TEXT NOT NULL, LocationID INTEGER, NodeStatus TEXT, NodeUser TEXT, NodePass TEXT, FOREIGN KEY(LocationID) REFERENCES LocationTable(LocationID));")
        cur.execute("CREATE TABLE PortTable (PortID INTEGER PRIMARY KEY ASC, PortName TEXT NOT NULL, PortStatus TEXT, PortSpeed INTEGER, CustomerID TEXT, NodeID INTEGER, FOREIGN KEY(NodeID) REFERENCES NodeTable(NodeID));")
        cur.execute("CREATE TABLE ServiceTable (ServiceID INTEGER PRIMARY KEY ASC, ServiceName TEXT NOT NULL, ServiceType TEXT NOT NULL);")
        cur.execute("CREATE TABLE SubInterfaceTable (SubInterfaceID INTEGER PRIMARY KEY ASC, SubInterfaceUnit INTEGER, SubInterfaceVLANID INTEGER, ServiceID INTEGER, SubInterfaceStatus TEXT NOT NULL, PortID INTEGER, FOREIGN KEY(ServiceID) REFERENCES ServiceTable(ServiceID), FOREIGN KEY (PortID) REFERENCES PortTable(PortID));")
        cur.execute("CREATE TABLE AuthorisationTable (CustomerID INTEGER, UserName TEXT, AuthorisationRole TEXT, PortID INTEGER, SubInterfaceID INTEGER, FOREIGN KEY(CustomerID) REFERENCES CustomerTable(CustomerID), FOREIGN KEY(UserName) REFERENCES UserTable(UserName), FOREIGN KEY(PortID) REFERENCES PortTable(PortID), FOREIGN KEY(SubInterfaceID) REFERENCES SubInterfaceTable(SubInterfaceID));")
        cur.execute("CREATE TABLE ServiceMappingTable (ServiceID TEXT, SubInterfaceID TEXT, FOREIGN KEY(ServiceID) REFERENCES ServiceTable(ServiceID), FOREIGN KEY(SubInterfaceID) REFERENCES SubInterfaceTable(SubInterfaceID));")
        cur.execute("CREATE TABLE TransactionLog (TransactionID INTEGER PRIMARY KEY ASC, TransactionTimeStamp TEXT, UserID TEXT, IPAddress TEXT, EventType TEXT, PortID TEXT, SubInterfaceID TEXT, EventDescription TEXT);")
        print "Closing db"
        close_db(db_connection)
        print "DB closed"
    else:
        print "Confirmation cancelled"

def usage():
    sys.stdout.write("Usage: lattice reinit\n")
    sys.stdout.write("Usage: lattice node add <ip address>\n")
    sys.stdout.write("Usage: lattice node delete <ip address>\n")
    sys.stdout.write("Usage: lattice node list\n")
    sys.stdout.write("Usage: lattice subinterface create <node> <port> <ID>\n")
    sys.stdout.write("Usage: lattice subinterface delete <node> <port> <ID>\n")
    sys.stdout.write("Usage: lattice subinterface list\n")
    sys.stdout.write("Usage: lattice service create <service-name> <service type>\n")
    sys.stdout.write("Usage: lattice service delete <id>\n")
    sys.stdout.write("Usage: lattice service attach <service-name> <port> <ID>\n")
    sys.stdout.write("Usage: lattice service detach <service-name> <port> <ID>\n")
    sys.stdout.write("Usage: lattice service list\n")
    sys.stdout.write("\n")

@named('list')
def node_list():
    db_connection = open_db()
    cur = db_connection.cursor()
    cur.execute("SELECT NodeID, NodeName, NodeType, NodeIPAddress, LocationID, NodeStatus FROM NodeTable")
    node_Rows = cur.fetchall()
    for node in node_Rows:
        print node
    close_db(db_connection)

@named('add')
def node_add(switch):
    inet_Regex = re.compile("^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-1][0-9]|22[0-3])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$") 
    if inet_Regex.match(switch.ip_address):
        db_connection = open_db()
        cur = db_connection.cursor()
        cur.execute("INSERT INTO NodeTable(NodeName, NodeType, NodeIPAddress, LocationID, NodeStatus, NodeUser, NodePass) VALUES(?, ?, ?, ?, ?, ?, ?)",(switch.host_name, switch.switch_type, switch.ip_address, 'Lab', switch.status, switch.user_name, encrypt(constants.CONST_DBKEY, switch.password)))
        db_connection.commit()
        close_db(db_connection)
    else:
	    sys.stdout.write("node_add() ERROR: Invalid IP Address")
	    sys.exit(1)

@named('delete')
def node_delete(node_ip_address):
    # Probably should delete by Primary Key, even though nodeIPAddress will be unique
    inet_regex = re.compile("^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-1][0-9]|22[0-3])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$")
    if inet_regex.match(node_ip_address):
        db_connection = open_db()
        cur = db_connection.cursor()
        print "Deleting " + node_ip_address
        cur.execute("DELETE FROM NodeTable WHERE NodeIPAddress = ?",(node_ip_address,))
        db_connection.commit()
        close_db(db_connection)
    else:
        sys.stdout.write("node_delete() ERROR: Invalid IP Address")
        sys.exit(1)

def ports_add(switch, ports_table):
    db_connection = open_db()
    cur = db_connection.cursor()
    for port in ports_table:
        cur.execute("INSERT INTO PortTable(PortName, PortStatus, PortSpeed, CustomerID, NodeID) VALUES(?, ?, ?, ?, ?)",(port['name'], port['oper_status'], port['speed'], 'lattice', switch.host_name))
    db_connection.commit()
    close_db(db_connection)

@named('list')
def sub_interface_list():
    db_connection = open_db()
    cur = db_connection.cursor()
    cur.execute("SELECT SubInterfaceID, SubInterfaceUnit, SubInterfaceVLANID, SubInterfaceStatus, PortID FROM SubInterfaceTable")
    sub_interface_rows = cur.fetchall()
    for sub_interface in sub_interface_rows:
        print sub_interface
    close_db(db_connection)

@named('create')
def sub_interface_create(sub_interface_unit, sub_interface_vlan_id, service_id, sub_interface_status, port_id):
    db_connection = open_db()
    cur = db_connection.cursor()
    cur.execute("INSERT INTO SubInterfaceTable(SubInterfaceUnit, SubInterfaceVLANID, ServiceID, SubInterfaceStatus, PortID) VALUES(?, ?, ?, ?, ?)",(sub_interface_unit, sub_interface_vlan_id, service_id, sub_interface_status, port_id))
    db_connection.commit()
    close_db(db_connection)

@named('delete')
def sub_interface_delete(sub_interface_unit, port_id):
    db_connection = open_db()
    cur = db_connection.cursor()
    cur.execute("DELETE FROM SubInterfaceTable WHERE SubInterfaceUnit = ? AND portID = ?",(sub_interface_unit, port_id))
    db_connection.commit()
    close_db(db_connection)

@named('create')
def service_create(service_name, service_type):
    db_connection = open_db()
    cur = db_connection.cursor()
    cur.execute("INSERT INTO ServiceTable(ServiceName, ServiceType) VALUES(?, ?)", (service_name, service_type))
    db_connection.commit()
    close_db(db_connection)

@named('delete')
def service_delete(service_name):
    db_connection = open_db()
    cur = db_connection.cursor()
    cur.execute("DELETE FROM ServiceTable WHERE ServiceName = ?", (service_name,))
    db_connection.commit()
    close_db(db_connection)

@named('list')
def service_list():
    db_connection = open_db()
    cur = db_connection.cursor()
    cur.execute("SELECT ServiceID, ServiceName, ServiceType FROM ServiceTable")
    service_rows = cur.fetchall()
    for service in service_rows:
        print service
    close_db(db_connection)

@named('attach')
def service_attach(service_id, sub_interface_id):
    db_connection = open_db()
    cur = db_connection.cursor()
    cur.execute("UPDATE ServiceTable SET ServiceID = VALUES(?,) WHERE SubInterfaceID = VALUES(?,)",(service_id, subnterface_id))
    close_db(db_connection)
    db_connection.commit()

@named('detach')
def service_detach(service_id):
    db_connection = open_db()
    cur = db_connection.cursor()
    cur.execute("DELETE FROM ServiceTable WHERE ServiceID = ?",(service_id))
    close_db(db_connection)
    db_connection.commit()


#def main(argv):
#    sys.stdout.write("lattice\n\n")
#    lattice_Function=''
#    if len(sys.argv) <= 1:
#        usage()
#        exit(1)
#    else:
#        lattice_function = sys.argv[1]
    # Okay, this is getting ugly - fix up with argparse library or similar
    # Think through the grammar so that it makes sense when the REST API is added

parser = ArghParser()
parser.add_commands([node_add, node_delete, node_list],
                    namespace='node', 
                    namespace_kwargs={
                        'title': 'Node Operations', 
                        'description': 'Node Operations ', 
                        'help': 'Node Operations'
                    })
parser.add_commands([service_create, service_delete, service_attach, service_detach, service_list], 
                    namespace='service', 
                    namespace_kwargs={
                        'title': 'Service Operations', 
                        'description': 'Service Operations', 
                        'help': 'Service Operations'
                    })
parser.add_commands([sub_interface_create, sub_interface_delete, sub_interface_list], 
                    namespace='subinterface', 
                    namespace_kwargs={
                        'title': 'Port Operations', 
                        'description': 'Port Operations', 
                        'help': 'Port Operations'
                    })                    
parser.add_commands([reinit_db])



#    if lattice_function == 'reinit':
#        reinit_db()
#    elif lattice_function == 'node':
#        if len(sys.argv) >= 3:
#            if sys.argv[2]=='list':
#                print "Printing node list..."
#                node_list()
#            elif sys.argv[2]=='add':
#                # node add <type> <ip_address> <username> <password>
#                # Open device, retrieve Serial Number and Model
#                print "Adding node " + sys.argv[4] + "..."
#                switchFactory = NodeFactory()
#                # connect to device and populate new_switch object
#                new_switch = switchFactory.create_switch(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
#                # pass populated switch object to add_switch for importing into db
#                node_add(new_switch)
#                ports_table = new_switch.port_table
#                ports_add(new_switch, ports_table)
#            elif sys.argv[2]=='delete':
#                print "Deleting node " + sys.argv[3] + "..."
#                node_delete(sys.argv[3])
#            else:
#                print "Error: '" + sys.argv[2] + "' is an unknown node parameter\n"
#                usage()
#        else:
#            sys.stdout.write("Error: incorrect node parameters\n\n")
#            usage()
#    elif lattice_function == 'subinterface':
#        if len(sys.argv) >= 3:
#            if sys.argv[2]=='list':
#                print "Printing subinterface list..."
#                sub_interface_list()
#            elif sys.argv[2]=='create':
#                print "Creating subinterface " + sys.argv[3] + "..."
#                sub_interface_create(sys.argv[3], sys.argv[3], 'sid'+sys.argv[3], 'Active', 'ge-0/0/0')
#            elif sys.argv[2]=='delete':
#                print "Deleting subinterface " + sys.argv[3] + "..."
#                sub_interface_delete(sys.argv[3], 'ge-0/0/0')
#            elif sys.argv[2]=='attach':
#                print "Attaching subinterface " + sys.argv[3] + " to node " + sys.argv[4]
#            else:
#                print "Error: '" + sys.argv[2] + "' is an unknown service parameter\n"
#                usage()
#        else:
#            sys.stdout.write("Error: incorrect service parameters\n\n")
#            usage()
#    elif lattice_function == 'service':
#        if len(sys.argv) >= 3:
#            if sys.argv[2]=='list':
#                print "Printing service list..." 
#                service_list()
#            elif sys.argv[2]=='create':
#                print "Creating service " + sys.argv[3] + "..."
#                service_create(sys.argv[3], 'vpls')
#            elif sys.argv[2]=='delete':
#                print "Deleting service " + sys.argv[3] + "..."
#                service_delete(sys.argv[3])
#            else:
#                print "Error: '" + sys.argv[2] + "' is an unknown service parameter\n"
#                usage()
#        else:
#            sys.stdout.write("Error: incorrect service parameters\n\n")
#            usage()
#    else:
#        sys.stdout.write("Error: Missing parameter\n\n")
#        usage()

if __name__ == "__main__":
    parser.dispatch()
