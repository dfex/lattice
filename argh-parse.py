#!/usr/bin/python
# Experimental parser

import argh
import sys

def add(ip_address, node_type, username, password, ):
    "Adds a new node"
    pass

def delete(ip_address):
    "Deletes a node"
    pass

def list():
    "Returns a list of nodes"
    pass

def create(type, id):
    "Creates a service definition"
    pass

def attach(serviceid, port):
    "Attaches a service to a port"
    pass

def detach(serviceid, port):
    "Detaches a service from a port"

def reinit():
    "Re-initialises the lattice db"
    pass

parser = argh.ArghParser()
parser.add_commands([add, delete, list], 
                    namespace='node', 
                    namespace_kwargs={
                        'title': 'Node Operations', 
                        'description': 'Node Operations ', 
                        'help': 'Node Operations'
                    })
parser.add_commands([create, attach, detach], 
                    namespace='service', 
                    namespace_kwargs={
                        'title': 'Service Operations', 
                        'description': 'Service Operations', 
                        'help': 'Service Operations'
                    })
                    
parser.add_commands([reinit])


if __name__ == '__main__':
    parser.dispatch()
    