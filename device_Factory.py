import junosconnect
import aristaconnect

class Node(node_type, node_ip_address, node_username, node_password):
    """Node factory for device connections

    :attr:`node_type`: node type (junos_ex, arista_eos etc)
    :attr:`node_ip_address`: node ip address
    :attr:`node_username`: username for logging into node
    :attr:`password`: password for logging into node
    """
    def __init__(self, node_type, node_ip_address, node_username, node_password)
        self.type=node_type
        self.ip_address=node_ip_address
        self.username=node_username
        self.password=node_password
        self.serial_number=''
        self.model=''
        self.host_name=''
        self.status='UNINITIALISED'
        #return eval(type + "()")
        if self.type='junos_ex': return Junos()
        if self.type='arista_eos': return Arista()
        assert 0, 'Bad node type: ' + self.type
        
