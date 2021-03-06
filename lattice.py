#!/usr/bin/python

## lattice - network topology in sql

import re, sys, getopt
import sqlite3
from argh import named, ArghParser, expects_obj
from device_Factory import NodeFactory
from constants import service_types, device_types, CONST_DBKEY
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
        cur.execute("CREATE TABLE SubInterfaceTable (SubInterfaceID INTEGER PRIMARY KEY ASC, SubInterfaceUnit INTEGER, ServiceID INTEGER, SubInterfaceStatus TEXT, PortID INTEGER, FOREIGN KEY(ServiceID) REFERENCES ServiceTable(ServiceID), FOREIGN KEY (PortID) REFERENCES PortTable(PortID));")
        cur.execute("CREATE TABLE ServiceTable (ServiceID INTEGER PRIMARY KEY ASC, ServiceName TEXT NOT NULL, ServiceType TEXT NOT NULL);")
        cur.execute("CREATE TABLE AuthorisationTable (CustomerID INTEGER, UserName TEXT, AuthorisationRole TEXT, PortID INTEGER, SubInterfaceID INTEGER, FOREIGN KEY(CustomerID) REFERENCES CustomerTable(CustomerID), FOREIGN KEY(UserName) REFERENCES UserTable(UserName), FOREIGN KEY(PortID) REFERENCES PortTable(PortID), FOREIGN KEY(SubInterfaceID) REFERENCES SubInterfaceTable(SubInterfaceID));")
        cur.execute("CREATE TABLE TransactionLog (TransactionID INTEGER PRIMARY KEY ASC, TransactionTimeStamp TEXT, UserID TEXT, IPAddress TEXT, EventType TEXT, PortID TEXT, SubInterfaceID TEXT, EventDescription TEXT);")
        print "Closing db"
        close_db(db_connection)
        print "DB closed"
    else:
        print "Confirmation cancelled"

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
def node_add(type, ip_address, username, password):
    if type not in device_types:
        print "node_add error: " + type + " is an unknown device type"
        sys.exit(1)
    inet_Regex = re.compile("^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-1][0-9]|22[0-3])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$") 
    switchFactory = NodeFactory()
    # connect to device and populate new_switch object
    new_switch = switchFactory.create_switch(type, ip_address, username, password)
    # populate ports_table object to pass to ports_add for importing into db later
    ports_table = new_switch.port_table

    if inet_Regex.match(ip_address):
        db_connection = open_db()
        cur = db_connection.cursor()
        cur.execute("INSERT INTO NodeTable(NodeName, NodeType, NodeIPAddress, LocationID, NodeStatus, NodeUser, NodePass) VALUES(?, ?, ?, ?, ?, ?, ?)",(new_switch.host_name, new_switch.switch_type, new_switch.ip_address, 'Lab', new_switch.status, new_switch.user_name, encrypt(CONST_DBKEY, new_switch.password)))
        db_connection.commit()
        close_db(db_connection)
        ports_add(new_switch, ports_table)
    else:
	    sys.stdout.write("node_add() ERROR: Invalid IP Address")
	    sys.exit(1)

@named('delete')
def node_delete(ip_address):
    # Probably should delete by Primary Key, even though nodeIPAddress *should* be unique (multi-tenant solutions?)
    inet_regex = re.compile("^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-1][0-9]|22[0-3])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$")
    if inet_regex.match(ip_address):
        db_connection = open_db()
        cur = db_connection.cursor()
        # Determine the NodeID from the IP Address
        cur.execute("SELECT NodeID FROM NodeTable WHERE NodeIPAddress = ?",(ip_address,))
        node_id = cur.fetchone()
        # Delete all Ports associated with that NodeID 
        cur.execute("SELECT PortID FROM PortTable WHERE NodeID = ?",(node_id[0],))    
        port_id_rows = cur.fetchall()
        for port_id in port_id_rows:
            ports_delete(port_id[0])
        # Now remove Node
        cur.execute("DELETE FROM NodeTable WHERE NodeIPAddress = ?",(ip_address,))
        db_connection.commit()
        close_db(db_connection)
    else:
        sys.stdout.write("node_delete() ERROR: Invalid IP Address")
        sys.exit(1)

@named('add')
def ports_add(switch, ports_table):
    db_connection = open_db()
    cur = db_connection.cursor()
    node_ip = str(switch.ip_address)
    for port in ports_table:
        cur.execute("SELECT NodeID FROM NodeTable WHERE NodeIPAddress = ?", (node_ip,))
        node_id = cur.fetchone()
        cur.execute("INSERT INTO PortTable(PortName, PortStatus, PortSpeed, CustomerID, NodeID) VALUES(?, ?, ?, ?, ?)",(port['name'], port['oper_status'], port['speed'], 'lattice', node_id[0]))
    db_connection.commit()
    close_db(db_connection)

@named('list')
def ports_list():
    db_connection = open_db()
    cur = db_connection.cursor()
    cur.execute("SELECT PortID, PortName, PortStatus, PortSpeed, CustomerID, NodeID FROM PortTable")
    node_Rows = cur.fetchall()
    for node in node_Rows:
        print node
    close_db(db_connection)

@named('delete')
def ports_delete(port_id):
    db_connection = open_db()
    cur = db_connection.cursor()
    # Delete dependent sub-interfaces
    cur.execute("SELECT SubInterfaceID FROM SubInterfaceTable WHERE PortID = ?",(port_id,))
    sub_interface_id_rows = cur.fetchall()
    for sub_interface_id in sub_interface_id_rows:
        sub_interface_delete(sub_interface_id[0])
    cur.execute("DELETE FROM PortTable WHERE PortID = ?", (port_id,))
    db_connection.commit()
    close_db(db_connection)

@named('list')
def sub_interface_list():
    db_connection = open_db()
    cur = db_connection.cursor()
    cur.execute("SELECT SubInterfaceID, SubInterfaceUnit, ServiceID, SubInterfaceStatus, PortID FROM SubInterfaceTable")
    sub_interface_rows = cur.fetchall()
    for sub_interface in sub_interface_rows:
        print sub_interface
    close_db(db_connection)

@named('create')
def sub_interface_create(node_name, port_name, sub_interface_unit):
    db_connection = open_db()
    cur = db_connection.cursor()
    # These should be stand-alone functions - eg: getService(SubInterfaceID) - refactor later
    cur.execute("SELECT NodeID FROM NodeTable WHERE NodeName = ?", (node_name,))
    node_id = cur.fetchone()
    if str(node_id) == 'None':
        print "Error: Invalid node specified"
        exit(1)    
    cur.execute("SELECT PortID FROM PortTable WHERE NodeID = ? AND PortName = ?", (node_id[0],port_name))
    port_id = cur.fetchone()
    if str(port_id) =='None':
        print "Error: Invalid port specified"
        exit(1)
    cur.execute("SELECT SubInterfaceID FROM SubInterfaceTable WHERE SubInterfaceUnit = ? and PortID = ?",(sub_interface_unit, port_id[0]))
    existing_subinterface_id = str(cur.fetchone())
    # Confirm that the sub-interface unit is unique on this PortID (and hence node)
    if existing_subinterface_id == 'None':
        cur.execute("INSERT INTO SubInterfaceTable(SubInterfaceUnit, PortID) VALUES(?, ?)",(sub_interface_unit, port_id[0]))
        db_connection.commit()
        close_db(db_connection)
    else:
        print "Error: specified sub-interface unit already exists on this interface"

@named('delete')
def sub_interface_delete(sub_interface_id):
    db_connection = open_db()
    cur = db_connection.cursor()
    # These should be stand-alone functions - eg: getService(SubInterfaceID) - refactor later
    cur.execute("SELECT ServiceID FROM SubInterfaceTable WHERE SubInterfaceID = ?",(sub_interface_id,))
    service_id = cur.fetchone() #One-to-one mapping between service and sub-interface
    service_detach(service_id[0], sub_interface_id)
    cur.execute("DELETE FROM SubInterfaceTable WHERE SubInterfaceID = ?",(sub_interface_id,))
    db_connection.commit()
    close_db(db_connection)

@named('create')
def service_create(service_name, service_type):
    if service_type in service_types:
        db_connection = open_db()
        cur = db_connection.cursor()
        cur.execute("INSERT INTO ServiceTable(ServiceName, ServiceType) VALUES(?, ?)", (service_name, service_type))
        db_connection.commit()
        close_db(db_connection)
    else:
        print "Error in service creation: invalid service type specified.  Valid service types are: " + str(service_types)

@named('delete')
def service_delete(service_id):
    db_connection = open_db()
    cur = db_connection.cursor()
    # Error checking
    cur.execute("SELECT SubInterfaceID FROM SubInterfaceTable WHERE ServiceID = ?", (service_id,))
    sub_interface_id_rows = cur.fetchall()
    for sub_interface_id in sub_interface_id_rows:
        service_detach(service_id, sub_interface_id[0])
    cur.execute("DELETE FROM ServiceTable WHERE ServiceID = ?", (service_id))
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
    cur.execute("UPDATE SubInterfaceTable SET ServiceID = ? WHERE SubInterfaceID = ?",(service_id, sub_interface_id))
    db_connection.commit()
    close_db(db_connection)
    # device configuration section (maybe break out into dedicated function?)
    db_connection = open_db()
    cur = db_connection.cursor()
    cur.execute("SELECT ServiceType, ServiceName FROM ServiceTable WHERE ServiceID = ?",(service_id,))
    service_type_result = cur.fetchone()
    cur.execute("SELECT PortID FROM SubInterfaceTable WHERE SubInterfaceID = ?",(sub_interface_id,))
    port_id_result = cur.fetchone()
    cur.execute("SELECT NodeID, PortName FROM PortTable WHERE PortID = ?",(port_id_result[0],))
    node_id_result = cur.fetchone()    
    cur.execute("SELECT NodeType, NodeIPAddress, NodeUser, NodePass FROM NodeTable WHERE NodeID = ?",(node_id_result[0],))
    node_creds = cur.fetchone()
    if service_type_result[0] == 'qinq':
        nodeFactory = NodeFactory()
        switch_instance = nodeFactory.create_switch(node_creds[0], node_creds[1], node_creds[2], decrypt(CONST_DBKEY, node_creds[3]))
        print "Port: " + node_id_result[1]
        switch_instance.create_port(node_id_result[1], 'Automated')
        print "SVLAN ID: " + str(int(sub_interface_id)+1000)
        print "VLAN Name: " + "v"+str(int(sub_interface_id)+1000)
        switch_instance.create_svlan(str(int(sub_interface_id)+1000), service_type_result[1], "Automated")
        switch_instance.bind_service(sub_interface_id, service_type_result[1], node_id_result[1])
        switch_instance.commit_configuration
    close_db(db_connection)    

@named('detach')
def service_detach(service_id, sub_interface_id):
    db_connection = open_db()
    cur = db_connection.cursor()
    cur.execute("UPDATE SubInterfaceTable SET ServiceID = ? WHERE SubInterfaceID = ?",(None, sub_interface_id))
    db_connection.commit()
    close_db(db_connection)
    # Need to reach out to affected nodes and update configuration

parser = ArghParser()
parser.add_commands([node_add, node_delete, node_list],
                    namespace='node', 
                    namespace_kwargs={
                        'title': 'Node Operations', 
                        'description': 'Node Operations ', 
                        'help': 'Node Operations'
                    })
parser.add_commands([ports_add, ports_list, ports_delete],
                    namespace='port', 
                    namespace_kwargs={
                        'title': 'Port Operations', 
                        'description': 'Port Operations ', 
                        'help': 'Port Operations'
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

if __name__ == "__main__":
    parser.dispatch()
