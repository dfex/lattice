#switch.py

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
