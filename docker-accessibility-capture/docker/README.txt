--> go to folder with Dockerfile and env folder in it
- activate python environment
- run 'invoke docker_console' to get a docker console
- from the docker console, go into docker-accessibility-capture/docker (where the docker-compose.yaml file is)

- run 'docker-machine ip'
	- take that IP and put it in the variable 
	- self.dock_master_ip = <docker-machine IP>
	- when sending to docker from the web client/server, the address is 
	 <docker-master IP>:8888
	 
- run 'docker-compose build'
- run 'docker-compose up'
- it will begin all of the containers and print out all output and errors from containers from that docker-compose up command, so dont ctl-C out of it until you're ready to be done

- you can now run any client stuff. see client_node.py for hints at what to do
- notes: client's must send an intro message with the address and port they are listening on to start
- note: a lot of the file doesn't exist errors will still crash the program, I haven't done error checking a lot yet. so be wary. You should see the errors in the output, though.

- if you end up accidently closing out of hte docker-compose up command before you're done, from a docker console, you can run 'docker logs serv' or 'docker logs emu1' to see the output of either container

- when done: run 'docker-compose down' to shut down docker containers

