from jnpr.junos import Device
from os import getenv


class Junos(object):
    """Base class for Junos devices.

    :attr:`hostname`: router hostname
    :attr:`user`: user for logging into `hostname`
    :attr:`password`: password for logging into `hostname`
    :attr:`timeout`: time to wait for a response
    :attr:`connection`: connection to `hostname`
    """

    @property
    def connection(self):
        """
        returns the connection
        """
        return self._connection

    @property
    def arp_table(self):
        """A list of ARP entries.

        :returns: ARP entries
        :rtype: list
        """
        table = []
        old_table = self.connection.rpc.get_arp_table_information(vpn=self.vpn)
        for old_entry in old_table:
            if old_entry.tag != 'arp-table-entry':
				continue
            entry = dict(ip_address=old_entry.findtext('ip-address').strip(),
                         interface=old_entry.findtext('interface-name').strip(),
                         hostname=self.hostname.strip(),
                         vpn=self.vpn,
                         mac_address=old_entry.findtext('mac-address').strip())
            table.append(entry)
        return table

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
			             description=old_entry.findtext('description'),
			             mtu=old_entry.findtext('mtu').strip(),
			             speed=old_entry.findtext('speed').strip())
			table.append(entry)
        return table

    @property
    def chassisInventory(self):
        """A chassis inventory

        :returns: Chassis Inventory
        :rtype: list
        """
        table = []
        version_entry = {}
# spaghetti - we just want the hostname
#       version_info_table = self.connection.rpc.get_software_information()
#       for version_entry_info in version_info_table:
#        	if version_entry_info.tag != 'software-information':
#        		continue
#			version_entry = dict(hostname=version_entry_info.findtext('host-name'))

        old_table = self.connection.rpc.get_chassis_inventory()
        for old_entry in old_table:
			entry = dict(serialnumber=old_entry.findtext('serial-number'),
			             model=old_entry.findtext('description'))
#			             hostname=version_entry['hostname'])
			table.append(entry)
        return table


    def __init__(self, *args, **kwargs):
        self.hostname = args[0] if len(args) else kwargs.get('host')
        self.user = kwargs.get('user', getenv('USER'))
        self.password = kwargs.get('password')
        self.timeout = kwargs.get('timeout')
        self.vpn = kwargs.get('vpn', 'default')
        self._connected = False
        self._connection = self._connect()

    def __enter__(self):
		self._connection = self._connect()
		return self

    def __exit__(self, exctype, excisnt, exctb):
		if self._connection:
			self._connection.close()


    def _connect(self):
        """Connect to a device.

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