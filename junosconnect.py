from switch import Switch
from jnpr.junos import Device
from os import getenv

class Junos_Device(Switch):
    """Base class for Junos devices.

    :attr:`hostname`: router hostname
    :attr:`user`: user for logging into `hostname`
    :attr:`password`: password for logging into `hostname`
    """

    @property
    def connection(self):
        """
        returns the connection
        """
        return self._connection

    @property
    def port_table(self):
        """A list of Ethernet Ports

        :returns: Ethernet Ports
        :rtype: list
        """
        port_table = []
        old_table = self.connection.rpc.get_interface_information(interface_name='[fgx]e-*')
        for old_entry in old_table:
			if old_entry.tag != 'physical-interface':
				continue
			entry = dict(name=old_entry.findtext('name').strip(),
			             admin_status=old_entry.findtext('admin-status').strip(),
			             oper_status=old_entry.findtext('oper-status').strip(),
			             description='None' if old_entry.findtext('description')==None else old_entry.findtext('description').strip(),
			             mtu=old_entry.findtext('mtu').strip(),
			             speed=old_entry.findtext('speed').strip())
			port_table.append(entry)
        return port_table

    @property
    def chassis_table(self):
        """A chassis inventory

        :returns: Chassis Inventory
        :rtype: list
        """
        sys_info_table = self.connection.rpc.get_software_information()
        host_name = sys_info_table.findtext('host-name')
        chassis_table = []
        old_table = self.connection.rpc.get_chassis_inventory()
        for old_entry in old_table:
			entry = dict(serial_number=old_entry.findtext('serial-number').strip(),
			             model=old_entry.findtext('description').strip(),
			             hostname=host_name)
			chassis_table.append(entry)
        return chassis_table


    def __init__(self, ip_address, user_name, password):
        self.ip_address = ip_address
        self.user_name = user_name
        self.password = password
        self._connected = False
        self._connection = self._connect()
        self.model=''
        self.host_name=''
        self.status='UNINITIALISED'
        self.connection_method='NETCONF over ssh'       
#class Junos(Switch):
#    def __init__(self, ip_address, login, password):
#        self.ip_address = ip_address
#        self.login = login
#        self.password = password
#        self.connection_method = "netconf/ssh"


    def __enter__(self):
		self._connection = self._connect()
		return self

    def __exit__(self, exctype, excisnt, exctb):
		if self._connection:
			self._connection.close()


    def _connect(self):
        """Connect using NETCONF over SSH

        :returns: a connection to a Juniper Networks device.
        :rtype: ``Device``
        """
        if self.password=='':
        	dev = Device(self.ip_address, user=self.user_name)
        else:
        	dev = Device(self.ip_address, user=self.user_name, password=self.password)
        dev.open()
#       dev.timeout = self.timeout
        return dev