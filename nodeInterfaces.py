#!/usr/bin/python

vendors = {}

# add in extra vendor connection methods as they arise
# maybe change to a factory pattern to handle multiple methods for different vendor outputs
vendors.update(juniper='j-netconf')
vendors.update(arista='eos-api')
vendors.update(cisco-nx='c-netconf')
vendors.update(brocade='expect')