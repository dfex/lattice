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

## This version is a better starting point:
class Switch(object):
    def connection(self):
        print ("Not implemented in base class")
    def describe(self):
        print "My IP is: {}".format(self.ip_address)
        print "Connect to me via {} with the username {} and password {}".format(self.connection_method, self.login, self.password)
    def port_table(self):
        print ("Not implemented in base class")
    def chassis_table(self):
        print ("Not implemented in base class")

            
class Junos(Switch):
    def __init__(self, ip_address, login, password):
        self.ip_address = ip_address
        self.login = login
        self.password = password
        self.connection_method = "netconf/ssh"
        

class Arista(Switch):
    def __init__(self, ip_address, login, password):
        self.ip_address = ip_address
        self.login = login
        self.password = password
        self.connection_method = "eAPI/REST"        


class NodeFactory:
    def createSwitch(self, switch_type, ip_address, login, password):
        if switch_type == 'junos-ex':
            return Junos(ip_address, login, password)
        if switch_type == 'arista-eos':
            return Arista(ip_address, login, password)
         
factory = NodeFactory()
lab_box = factory.createSwitch("junos-ex", "192.168.1.1", "ben", "secret")
    
# or even http://python-3-patterns-idioms-test.readthedocs.org/en/latest/Factory.html
# http://programmers.stackexchange.com/questions/166699/python-factory-function-best-practices
# http://ginstrom.com/scribbles/2007/10/08/design-patterns-python-style/
# http://davidcorne.com/2013/01/21/builder-pattern/
# https://github.com/faif/python-patterns/blob/master/abstract_factory.py

class A(object):
    def __init__(self):
        self.a = "Hello"
class B(object):
    def __init__(self):
        self.a = " World"
myfactory = {
   "greeting" : A,
   "subject"  : B,
}
>>> print myfactory["greeting"]().a
Hello

