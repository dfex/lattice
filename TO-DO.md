node add 192.168.100.1 username password node-type

capture above detail in node instance (Class)

set node_status of Node to NEW/UNREAD

connect to node 
- pull down extra detail like serial number and add it to node instance
- set node_status to READ(Y)
- write node detail to db
- pull down port information - port_add() - object relationship will be stored in db only - no need for class to have associations    
- set port_statuses to AVAILABLE
- write port detail to db


add the node instance detail into sql db?



##TODO

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
* ~~Define configuration templates for service creation (jinja2) - should they be templates, or a list of rpc calls?~~
* ~~Switch from camelCase to snake_case~~
* ~~Add functions to import all relevant device information into db schema required for "Service" creation and deletion (eg: populate nodeTable, portTable etc)~~
* ~~Resolve conundrum with node object being distinct from Junos class (makes sense for future node types)~~
* ~~Resolve issue with chassis_table "list" object~~
* ~~Update lattice.py to work with new object hierarchy~~
* ~~Confirm order of operations eg:~~ 
    * ~~Interface/CLI command~~
    * ~~nodeAdd()~~
    * ~~Attempt to connect to device~~
    * ~~Pull down node information~~
    * ~~Open db (inside function, or open and pass?)~~
    * ~~Add node information to nodeTable (open and close db, or pass db connection?)~~
    * ~~Pull down port information~~
    * ~~Add port information to portTable~~
    * ~~Close db connection (inside business logic, or part of controller?~~
* ~~Explore moving to structs/objects rather than passing individual variables - eg: when reading from a node return a populated node object eg: node.name, node.ipAddress etc., then just pass the entire node object to addnode() for writing to db~~
* ~~Update device interactions such that they could operate in a multi-vendor environment (using Node type field to distinguish)~~
* Add functions to write out from db to device configuration via j2 templates (? or just the required RPC calls?)
* Fix up parameter parsing if/elif/else hell with argparse lib
* Re-write lattice.py so that node addition handles port addition in same context (so ports can be tied back to node in db)
* Re-visit db schema and adjust functions to match - eg: referencing via PKs (IDs), only required/relevant fields for functions, and map to end-user operational flow (more tables, rigour around NOT NULL requirements)
* Break out service configuration from definition/type
* Confirm ELS and EX interface templates to apply to multiple services (eg: EX won't require sub-interface - either add to port, or add port to VLAN) - build j2 templates for each
* Add functionality to add and delete all system elements (Locations, Nodes, Ports, Sub-Interfaces, Services, Customers, Users) - ensure deletion of parent removes all child entities
* Be sure to add interface description with a formatted service identifier - check description-string limitations
* Create a "service" between two nodes that is either:
	* an 802.1q tagged or untagged VLAN
	* an 802.1ad double-tagged VLAN will an all-to-one mapping of CVLANs
	* an 802.1ad double-tagged VLAN with one-to-one mapping of individual CVLANs
* Build lattice service types as either "Point-to-Point" or "Multipoint" (easy icon for recognition)
* Add RESTful API hooks for functions
* Username/Password storage.  SSH Keys for Junos - REST on eOS?

##TOFIX:
* ~~Will need to adjust chassisInventory for multi-device/multiRE clusters or VCs down the track~~

##Phase 2 
* Test-driven Web app in Django or lighter weight - selenium integration
* Add a "flare" table so that Customer can have an icon associated with their connection
* Add custom logic for certain end-points (eg: AWS, Azure or GCE login credentials)
* Phase 3: iphone app in Swift.  Connections should be wizard-based full-screen rather than rows of config information (eg: swipe between steps)

References:

* http://zetcode.com/db/sqlitepythontutorial/
* http://blog.tylerc.me/code/2015/05/04/beyond-junos-eznc-pyez/
* http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/
* https://github.com/vshaumann/My-Data-Science-Resources
* https://www.juniper.net/techpubs/en_US/junos14.1/topics/task/configuration/qinq-tunneling-ex-series-cli-els.html
* https://www.juniper.net/techpubs/en_US/junos14.1/topics/task/configuration/l2pt-ex-series-cli-els.html
* http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api#restful