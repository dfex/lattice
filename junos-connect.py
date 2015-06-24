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
        old_table = self.connection.rpc.get_interface_information(interface-name="[xgf]e*")
        for old_entry in old_table:
			if old_entry.tag != 'physical-interface':
                continue
            entry = dict(name=old_entry.findtext('name').strip(),
                         admin-status=old_entry.findtext('admin-status').strip(),
                         oper-status=old_entry.findtext('oper-status').strip(),
                         description=old_entry.findtext('description').strip(),
                         mtu=old_entry.findtext('mtu').strip(),
                         speed=old_entry.findtext('speed').strip())
            table.append(entry)
        return table


    def __init__(self, *args, **kwargs):
        self.hostname = args[0] if len(args) else kwargs.get('host')
        self.user = kwargs.get('user', getenv('USER'))
        self.password = kwargs.get('password')
        self.timeout = kwargs.get('timeout')
        self.vpn = kwargs.get('vpn', 'default')

    def _connect(self):
        """Connect to a device.

        :returns: a connection to a Juniper Networks device.
        :rtype: ``Device``
        """
        if self.password='':
        	dev = Device(self.hostname, user=self.user)
        else:
        	dev = Device(self.hostname, user=self.user, password=self.password)
        dev.open()
        dev.timeout = self.timeout
        return dev