#!/usr/bin/python
# Experimental parser

import argh

def node():
    "Perfoms operations on a node"
    pass

def service():
    "Allows service definition, attachment and removal"
    pass

def reinit():
    "Re-initialises the lattice db"
    pass

parser = argh.ArghParser()
parser.add_commands([reinit, node, service])

if __name__ == '__main__':
    parser.dispatch()
    