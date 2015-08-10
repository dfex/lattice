#!/usr/bin/python
# Experimental parser

import argh
import sys

def add(args):
    "Adds a new node"
    pass

def delete(args):
    "Deletes a node"
    pass

def list():
    "Returns a list of nodes"
    pass

def create():
    "Creates a service definition"
    pass

def attach():
    "Attaches a service to a port"
    pass

def detach():
    "Detaches a service from a port"

def reinit():
    "Re-initialises the lattice db"
    pass

parser = argh.ArghParser()
parser.add_commands([add, delete, list], namespace='node', title='Node Operations')
parser.add_commands([create, attach, detach], namespace='service', title='Service Operations')
parser.add_commands([reinit])


if __name__ == '__main__':
    parser.dispatch()
    