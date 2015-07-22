from switch import Switch
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
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

    def switch_detail(self):
        """Populates information on the device
        """
        sys_info_table = self.connection.rpc.get_software_information()
        # For non-VC capable devices eg: EX3200
        # self.host_name = sys_info_table.findtext('host-name')
        self.host_name = sys_info_table.findtext('multi-routing-engine-item/software-information/host-name')
        hw_info_table = self.connection.rpc.get_chassis_inventory()
        self.serial_number = hw_info_table.findtext('chassis/serial-number')
        self.model = hw_info_table.findtext('chassis/description')

    def configure_port(self, port_name, port_description):
        """Sets the description of a given port
        """
        rpc_call = '<configuration> <interfaces> <interface> <name>' + port_name + '</name> <description>' + port_description + '</description> </interface> </interfaces> </configuration>'
        self.connection.bind(cu=Config)
        self.connection.cu
        self.connection.cu.load(rpc_call, format="xml")  
        self.connection.cu.commit()

    def configure_svlan(self, vlan_id, vlan_name, vlan_description):
        """Create Service VLAN on switch
        """
        # Fix RPC call
        # rpc_call = '<configuration> <interfaces> <interface> <name>' + port_name + '</name> <description>' + port_description + '</description> </interface> </interfaces> </configuration>'
        svlan_vars={}
        svlan_vars['vlan_stag'] = vlan_id
        svlan_vars['vlan_name'] = vlan_name
        svlan_vars['vlan_description'] = vlan_description
        cu = Config(self.connection)
        cu.load(template_path='service-templates/junos/ex/dot1ad-vlan.conf', template_vars=svlan_vars, merge=True)  
        cu.commit()       
        
    def __init__(self, ip_address, user_name, password):
        self.ip_address = ip_address
        self.user_name = user_name
        self.password = password
        self._connected = False
        self._connection = self._connect()
        self.switch_type = 'junos-ex'
        self.model=''
        self.host_name=''
        self.status='UNINITIALISED'
        self.connection_method='NETCONF over ssh'
        self.configuration = Config(self)
        self.switch_detail()
        
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