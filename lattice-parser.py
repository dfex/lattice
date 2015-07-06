#!/usr/bin/python
# Experimental parser

import argparse

def listNodes():
    pass

#lattice_parser = argparse.ArgumentParser(description='Virtual cross-connect provisioner')
#subparsers = lattice_parser.add_subparsers(help='commands')

# reinit command
#reinit_parser = subparsers.add_parser('reinit', help='Re-initiliase the lattice DB')
#reinit_parser.add_argument('--force', action='store_true', default=False, help='Do not ask for confirmation')

# node command
#node_parser = subparsers.add_parser('node', help='Node operations')
#node_subparser = subparsers.add_subparsers('node', help='Node operations')

#node_subparser.add_argument('list', action='store', help='List all nodes')
#node_subparser.add_argument('add', action='store', help='Add a new node')
#node_subparser.add_argument('delete', action='store', help='Delete an existing node')



lattice_parser = argparse.ArgumentParser(add_help=False)

lattice_parser.add_argument('reinit', default=listNodes(), help='Re-initialise the lattice DB')
lattice_parser.add_argument('--force', default=False, required=False, action='store_true', dest="force", help='Do not ask for confirmation')

main_parser = argparse.ArgumentParser(description='Virtual cross-connect provisioner')

command_subparsers = main_parser.add_subparsers(title="Command", dest="service_command")
node_parser = command_subparsers.add_parser("node", help="Node commands", parents=[lattice_parser])
port_parser = command_subparsers.add_parser("port", help="Port commands", parents=[lattice_parser])
subinterface_parser = command_subparsers.add_parser("subinterface", help="Subinterface commands", parents=[lattice_parser])


node_list_subparser = node_parser.add_subparsers(title="list", dest="list_command")
#node_add_subparser = node_parser.add_subparsers(title="add", dest="list_command")
#node_delete_subparser = node_parser.add_subparsers(title="delete", dest="list_command")

action_parser = node_list_subparser.add_parser("second", help="second", parents=[lattice_parser])

args = main_parser.parse_args()   


#parent_parser = argparse.ArgumentParser(add_help=False)                                                                                                  
#parent_parser.add_argument('--user', '-u',                                                                                                               
#                    default=getpass.getuser(),                                                                                                           
#                    help='username')                                                                                                                     
#parent_parser.add_argument('--debug', default=False, required=False,                                                                                     
#                           action='store_true', dest="debug", help='debug flag')                                                                         
#main_parser = argparse.ArgumentParser()                                                                                                                  
#service_subparsers = main_parser.add_subparsers(title="service",                                                                                         
#                    dest="service_command")                                                                                                              
#service_parser = service_subparsers.add_parser("first", help="first",                                                                                    
#                    parents=[parent_parser])                                                                                                             
#action_subparser = service_parser.add_subparsers(title="action",                                                                                         
#                    dest="action_command")                                                                                                               
#action_parser = action_subparser.add_parser("second", help="second",                                                                                     
#                    parents=[parent_parser])                                                                                                             
#args = main_parser.parse_args()   




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
