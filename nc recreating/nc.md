nc is powerful tool that allows powerful connection between our hosts.

The connection here consists of `server` and `client`

server characteristics:
- It will contain `-l` option of course as it will be listening for the upcomming conenctions
- It can contain `-e` option in order to execute command on the client once the connection is established


> You can use any of both TCP & UDP connection

Of course specifying the port is a must...

example usage:

server : `python.exe '.\nc.py' -l -p 50000 -e 'whoami'`

client : `python.exe '.\nc.py' -p 50000`