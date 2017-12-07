--> go to folder with Dockerfile and env folder in it
- activate python environment
- run invoke docker_console three times (it's easiest)
- from one of the docker consoles, go into docker-accessibility-capture/docker (where the docker-compose.yaml file is)

- run 'docker-machine ip'
	- take that IP and put it in the variable 
	- self.dock_master_ip = <docker-machine IP>
	- when sending to docker from the web client/server, the address is 
	 <docker-master IP>:8888
	 
- run 'docker-compose build'
- run 'docker-compose up'
- ctrl - C to get out of the command once it succeeds in building emu1 and serv
- got to another docker console, run 'docker exec serv python code/master_node.py'
- in the last console, run 'docker exec emu1 python code/docker_emu_node.py'
