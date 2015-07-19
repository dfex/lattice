from switch import Switch
import requests

class Arista_Device(Switch):
    """Arista devices class

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
        # IMPLEMENT ME!
        return port_table

    @property
    def switch_detail(self):
        """A chassis inventory

        :returns: Chassis Inventory
        :rtype: list
        """
        table = []
        # IMPLEMENT ME!
        return chassis_table
        

    def __init__(self, *args, **kwargs):
        self.hostname = args[0] if len(args) else kwargs.get('host')
        self.user = kwargs.get('username')
        self.password = kwargs.get('password')
        self.timeout = kwargs.get('timeout')
        self._connected = False
        self._connection = self._connect()
        self.switch_type = 'arista-eos'
        self.model=''
        self.host_name=''
        self.status='UNINITIALISED'
        self.connection_method='eAPI via REST'     


    def __enter__(self):
		self._connection = self._connect()
		return self

    def __exit__(self, exctype, excisnt, exctb):
		if self._connection:
			self._connection.close()

    def _connect(self):
        """Connect using eAPI/REST

        :returns: a connection to an Asrista Networks device.
        :rtype: ``Device``
        """
        if self.password=='':
        	pass
        	# IMPLEMENT ME!
        else:
            pass
        	# IMPLEMENT ME!
        # MORE STUFF!
        return dev