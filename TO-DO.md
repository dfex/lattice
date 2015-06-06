##TODO:

* py script to open add a new switch - open up connection, query interfaces and import them into db
* functions to add and delete all elements (Locations, Nodes, Ports, Sub-Interfaces, Services, Customers, Users) - ensure deletion of parent removes all child entities
* build lattice service types as either "Point-to-Point" or "Multipoint" (easy icon for recognition)
* ultimately, first phase will be simple VLAN connectivity between one or more interfaces, but trunked VLANs on customer interfaces **will** be supported

* web app in Django for Phase 2
* Add a "flare" table so that Customer can have an icon associated with their connection
* Add custom logic for certain end-points (eg: AWS, Azure or GCE login credentials)
* Phase 3: iphone app in Swift.  Connections should be wizard-based full-screen rather than rows of config information (eg: swipe between steps)

**References:
* http://zetcode.com/db/sqlitepythontutorial/