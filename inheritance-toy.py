## Inheritance toy
## Seems backwards - Switch() class should have a factory method to instantiate a Junos() instance

class Switch(object):
    def __init__(self, switch_type, ip_address, login, password):
        self.ip_address = ip_address
        self.login = login
        self.password = password
        self.type = switch_type
        
    def describe(self):
        print "I'm an {}, connect via {}, at {} using login {} and password {}".format(self.type, self.connection_method, self.ip_address, self.login, self.password)


            
class Junos(Switch):
    def __init__(self, switch_type, ip_address, login, password):
        self.connection_method = 'Netconf over SSH'
        Switch.__init__(self, switch_type, ip_address, login, password)
        
    def describe(self):   
        Switch.describe(self)

