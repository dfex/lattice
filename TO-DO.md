##TODO:

* ~~open up connection to switch~~
* ~~query interfaces~~
* ~~import them into sqlite db~~
* ~~Fix foreign key constraints~~
* ~~Re-factor node-load and break out re-useable functions~~
* Spin local instance(s) of vSRX to run tests against and launch with VBoxManage if required
* Dump out EthPortTable and Device.facts() and line up against DB tables for import
* Test multi-field row insertion (currently committed)
* Import all relevant device information into db schema required for "Service" creation and deletion (eg: populate nodeTable, portTable etc)
* Add multiple device import (break this out into new program)
* Add test functions for device programmability / Service creation
* Create a "service" between two nodes that is either:
	* an 802.1q tagged or untagged VLAN
	* an 802.1ad double-tagged VLAN will an all-to-one mapping of CVLANs
	* an 802.1ad double-tagged VLAN with one-to-one mapping of individual CVLANs
* Build lattice service types as either "Point-to-Point" or "Multipoint" (easy icon for recognition)
* Add functionality to add and delete all system elements (Locations, Nodes, Ports, Sub-Interfaces, Services, Customers, Users) - ensure deletion of parent removes all child entities
* Add RESTful API hooks for functions
* Add multi-threading for device import

* Phase 2: 
* Update device interactions such that they could operate in a multi-vendor environment (using Node type field to distinguish)
* Test-driven Web app in Django or lighter weight - selenium integration
* Add a "flare" table so that Customer can have an icon associated with their connection
* Add custom logic for certain end-points (eg: AWS, Azure or GCE login credentials)
* Phase 3: iphone app in Swift.  Connections should be wizard-based full-screen rather than rows of config information (eg: swipe between steps)

**References:
* http://zetcode.com/db/sqlitepythontutorial/
