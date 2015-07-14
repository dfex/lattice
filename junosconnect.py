from jnpr.junos import Device
from os import getenv


class Junos_Device(Node):
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
        table = []
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
			table.append(entry)
        return table

    @property
    def chassis_table(self):
        """A chassis inventory

        :returns: Chassis Inventory
        :rtype: list
        """
        sys_info_table = self.connection.rpc.get_software_information()
        host_name = sys_info_table.findtext('host-name')
        table = []
        version_entry = {}
        old_table = self.connection.rpc.get_chassis_inventory()
        for old_entry in old_table:
			entry = dict(serialnumber=old_entry.findtext('serial-number').strip(),
			             model=old_entry.findtext('description').strip(),
			             hostname=host_name)
			table.append(entry)
        return table


    def __init__(self, *args, **kwargs):
        self.hostname = args[0] if len(args) else kwargs.get('host')
        self.user = kwargs.get('username')
        self.password = kwargs.get('password')
        self.timeout = kwargs.get('timeout')
        self._connected = False
        self._connection = self._connect()
        self.model=''
        self.host_name=''
        self.status='UNINITIALISED'

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
        	dev = Device(self.hostname, user=self.user)
        else:
        	dev = Device(self.hostname, user=self.user, password=self.password)
        dev.open()
        dev.timeout = self.timeout
        return dev