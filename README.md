# Resource Locks
Resources Management Lock System 


# Specifications

Python environment for running: Python 3
Commands examples:

	Server Side:
		
		- python lock_server.py <server-port> <resource-number> <lock-number> <blocked-resources> <time>

		e.g:
			python lock_server.py 9999 10 2 2 4	

		Info:
			<server-port> - Server Port;
			<resource-number> - Number of existing resources;
			<lock-number> - Number of maximum resource lock, after that the resource stays inactive;
			<blocked-resources> - Number of resources that can be blocked at the same time;
			<time> - Time that the resource will be blocked;

	Client Side:
		python lock_client.py <server-ip> <server-port> <client-id>

		Info:
			<server-ip> - Server IP;
			<server-port> - Server Port;
			<client-id> - Client Id;

