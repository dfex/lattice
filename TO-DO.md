##TODO:

* ~~open up connection to switch~~
* ~~query interfaces~~
* ~~import them into sqlite db~~
* Fix foreign key constraints
* Re-factor node-load and break out re-useable functions
* Update db schema with all elements required for "Service" creation and deletion
* Add device programmability for Service creation
* Create a "service" between two nodes that is:
	* an 802.1q tagged or untagged VLAN
	* an 802.1ad double-tagged VLAN will an all-to-one mapping of CVLANs
	* an 802.1ad double-tagged VLAN with one-to-one mapping of individual CVLANs
* Create pull request/issue for the Description field to be added into JunosPyEZ EthPortTable
* Alternatively, build a parallel function that achieves the same result but with Description
* Build lattice service types as either "Point-to-Point" or "Multipoint" (easy icon for recognition)
* Add functionality to add and delete all system elements (Locations, Nodes, Ports, Sub-Interfaces, Services, Customers, Users) - ensure deletion of parent removes all child entities
* Update device interactions such that they could operate in a multi-vendor environment (using Node type field to distinguish)
* Web app in Django for Phase 2
* Add a "flare" table so that Customer can have an icon associated with their connection
* Add custom logic for certain end-points (eg: AWS, Azure or GCE login credentials)
* Phase 3: iphone app in Swift.  Connections should be wizard-based full-screen rather than rows of config information (eg: swipe between steps)

**References:
* http://zetcode.com/db/sqlitepythontutorial/