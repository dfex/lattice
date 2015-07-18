from junosconnect import Junos_Device
from aristaconnect import Arista_Device

class NodeFactory(object):
    def create_switch(self, switch_type, ip_address, login, password):
        if switch_type == 'junos-ex':
            return Junos_Device(ip_address, login, password)
        if switch_type == 'arista-eos':
            return Arista_Device(ip_address, login, password)
