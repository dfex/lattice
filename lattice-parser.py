#!/usr/bin/python
# Experimental parser

import argparse

def listNodes():
    pass

lattice_parser = argparse.ArgumentParser(description='Virtual cross-connect provisioner')
subparsers = lattice_parser.add_subparsers(help='commands')

# reinit command
reinit_parser = subparsers.add_parser('reinit', help='Re-initiliase the lattice DB')
reinit_parser.add_argument('--force', action='store_true', default=False, help='Do not ask for confirmation')

# node command
node_parser = subparsers.add_parser('node', help='Node operations')
node_parser.add_argument('list', action='store', help='List all nodes')
node_parser.add_argument('add', action='store', help='Add a new node')
node_parser.add_argument('delete', action='store', help='Delete an existing node')

# port command
#port_parser = subparsers.add_parser('port', help='Port operations')
#port_parser.add_argument('list', action='store', help='List all ports')
#port_parser.add_argument('add', action='store', help='Add a new port')
#port_parser.add_argument('delete', action='store', help='Delete an existing port')

# subinterface command
#subinterface_parser = subparsers.add_parser('subint', help='Sub-interface operations')
#subinterface_parser.add_argument('list', action='store', help='List all subinterfaces')
#subinterface_parser.add_argument('add', action='store', help='Add a new subinterface')
#subinterface_parser.add_argument('delete', action='store', help='Delete an existing subinterface')

latticeArgs = lattice_parser.parse_args()

print latticeArgs

#    sys.stdout.write("Usage: lattice reinit\n")
#    sys.stdout.write("Usage: lattice node add <ip address>\n")
#    sys.stdout.write("Usage: lattice node delete <ip address>\n")
#    sys.stdout.write("Usage: lattice node list\n")
#    sys.stdout.write("Usage: lattice subinterface create <node> <port> <ID>\n")
#    sys.stdout.write("Usage: lattice subinterface delete <node> <port> <ID>\n")
#    sys.stdout.write("Usage: lattice subinterface list\n")
#    sys.stdout.write("Usage: lattice service create <service-name> <service type>\n")
#    sys.stdout.write("Usage: lattice service delete <id>\n")
#    sys.stdout.write("Usage: lattice service attach <service-name> <port> <ID>\n")
#    sys.stdout.write("Usage: lattice service detach <service-name> <port> <ID>\n")
#    sys.stdout.write("Usage: lattice service list\n")
