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

## Something like:
class Person:
    def __init__(self):
        self.name = None self.gender = None
    
    def getName(self): 
        return self.name
        
    def getGender(self):
        return self.gender


class Male(Person):
    def __init__(self, name):
        print "Hello Mr." + name


class Female(Person):
    def __init__(self, name):
        print "Hello Miss." + name


class Factory:
    def getPerson(self, name, gender):
        if gender == 'M':
            return Male(name)
        if gender == 'F':
            return Female(name)
￼￼
if __name__ == '__main__': 
    factory = Factory()
    person = factory.getPerson("Chetan", "M")
    
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

