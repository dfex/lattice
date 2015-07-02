##TODO:

* ~~open up connection to switch~~
* ~~query interfaces~~
* ~~import them into sqlite db~~
* ~~Fix foreign key constraints~~
* ~~Re-factor node-load and break out re-useable functions~~
* ~~spin local instance(s) of vSRX to run tests against and launch with VBoxManage if required~~
* ~~Build Class for XML RPC calls~~
* ~~Fix junosconnect class property fields to allow for ObjectType "None" to be returned, but strip() to still be used when values exist - eg: Interface Description~~
* ~~Fix junosconnect inventory retrieval code (device hostname and serial number need to be merged from two XML RPC calls)~~
* ~~Remove EthPortTable and Facts and revert to XML RPC calls - removes dependency on PyEZ field definitions~~
* ~~Test multi-field row insertion (currently committed)~~
* ~~Re-factor/build - each run is an atomic operation to populate db - add device & read ports, create service, bind ports to a service~~
* ~~Add a nuke database parameter (to remove duplicate crap)~~
* Add functions to import all relevant device information into db schema required for "Service" creation and deletion (eg: populate nodeTable, portTable etc)
* Confirm order of operations eg: 
    * Interface/CLI command
    * nodeAdd()
    * Attempt to connect to device
    * Pull down node information
    * Open db (inside function, or open and pass?)
    * Add node information to nodeTable (open and close db, or pass db connection?)
    * Pull down port information
    * Add port information to portTable
    * Close db connection (inside business logic, or part of controller?
* Add functions to write out from db to device configuration
* Create a "service" between two nodes that is either:
	* an 802.1q tagged or untagged VLAN
	* an 802.1ad double-tagged VLAN will an all-to-one mapping of CVLANs
	* an 802.1ad double-tagged VLAN with one-to-one mapping of individual CVLANs
* Build lattice service types as either "Point-to-Point" or "Multipoint" (easy icon for recognition)
* Add functionality to add and delete all system elements (Locations, Nodes, Ports, Sub-Interfaces, Services, Customers, Users) - ensure deletion of parent removes all child entities
* Add RESTful API hooks for functions
* Add multi-threading for device import where it makes sense


##TOFIX:
* Will need to adjust chassisInventory for multi-device/multiRE clusters or VCs
* Re-visit db schema and map to end-user operational flow (more tables, rigour around NOT NULL requirements)
* Break out service configuration from definition/type


* Phase 2: 
* Update device interactions such that they could operate in a multi-vendor environment (using Node type field to distinguish)
* Test-driven Web app in Django or lighter weight - selenium integration
* Add a "flare" table so that Customer can have an icon associated with their connection
* Add custom logic for certain end-points (eg: AWS, Azure or GCE login credentials)
* Phase 3: iphone app in Swift.  Connections should be wizard-based full-screen rather than rows of config information (eg: swipe between steps)

**References:
* http://zetcode.com/db/sqlitepythontutorial/
* http://blog.tylerc.me/code/2015/05/04/beyond-junos-eznc-pyez/
* http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/
* https://github.com/vshaumann/My-Data-Science-Resources