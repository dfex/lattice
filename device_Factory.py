import junosconnect
import aristaconnect

class Node(object):
    """Node factory for device connections

    :attr:`node_type`: node type (junos_ex, arista_eos etc)
    :attr:`node_ip_address`: node ip address
    :attr:`node_username`: username for logging into node
    :attr:`password`: password for logging into node
    """
    def __init__(self, node_type, node_ip_address, node_username, node_password)
        #return eval(type + "()")
        if self.type='junos_ex': return Junos_Device(node_ip_address, node_username, node_password)
        if self.type='arista_eos': return Arista_Device(node_ip_address, node_username, node_password)
        assert 0, 'Bad node type: ' + self.type


# Create a node (ip, user, pass)
# Sub-class with a specific node type
# On init, open a connection to the node.
# Populate serial number/chassis inventory into object
# Write object to SQL
# Get port table from object and populate dict
# Write port table to SQL
# Close object
# Read some OOP/Pattern books        
