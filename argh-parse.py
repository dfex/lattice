#!/usr/bin/python
# Experimental parser

import argh
import sys
from argh.decorators import expects_obj

#@expects_obj
def add(args):
    "Adds a new node"
    pass

#@expects_obj
def delete(args):
    "Deletes a node"
    pass

#@expects_obj
def list():
    "Returns a list of nodes"
    pass

#@expects_obj
def create():
    "Creates a service definition"
    pass

#@expects_obj
def attach():
    "Attaches a service to a port"
    pass

#@expects_obj
def detach():
    "Detaches a service from a port"

def reinit():
    "Re-initialises the lattice db"
    pass

parser = argh.ArghParser()
parser.add_commands([add, delete, list], namespace='node')
parser.add_commands([create, attach, detach], namespace='service')
parser.add_commands([reinit])


if __name__ == '__main__':
    parser.dispatch()
    