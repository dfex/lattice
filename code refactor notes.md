Code Refactor Notes:

## Notes
* In a separate file, provide a list of vendors and the connection methods defined - one spot for extensibility
* In the initial NodeObject struct, the vendor type will be defined so as to know in advance the connection method (SSH/Netconf (Cisco/Juniper), REST(Arista))
* The connections will need to be made roughly equivalent eg:
	* SSH/Netconf Connection == REST/Auth Process
	* Netconf RPC == REST GET
	* SSH/Netconf Close() == REST ?? (invalidate session? - maybe just a code stub that returns true) 
* Debug parameter - all functions dump "Entering <function name>, parameter list: <parameter> = <value>"
* Debug log - dedicated debug log file

##Open DB 
* given a db name/ip address and/or username/password
* connect to a db
* return db object/file descriptor
* interchangeable between db types (sqlite, mysql)
* error handling

##Populate DB 
* given a db object/file descriptior
* toy function to inject table data into db object
* will be deprecated over time - just used for building db and testing sqlite3/mysql functionality
* should be native SQL?  db agnostic
* returns true or false
* error handling?

##Close DB
* given a db object/fd
* close the db
* return true or false
* db agnostic
* error handling

##OpenNode - interchangeable between node types
* given a Node object (maybe a struct?) with IP address/DNS name, username and password and node type (vendor/connection method)
* open a connection to the node
* return a NodeConnection object
* node agnostic (start with Junos, Arista and IOS-NX?)
* error handling

##ReadNodeInfo
* given a NodeConnection object
* return a dict of node elements that won't change often (device facts - serial number, model, code versions) and write directly to node table
* node/vendor agnostic
* error handling

##ReadPortInfo
* given a NodeConnection object
* return a dict of nodePort elements and write directly to db PortTable
* vendor agnostic
* error handling

##CloseNode 
* given a NodeConnection object
* close the Node connection
* interchangeable between node types
* error handling

