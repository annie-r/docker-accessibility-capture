1. Reinstall the Python environment and dependencies. I added 2. (You can remove the env35 folder like below or if you know of some other way, feel free)

virtualenv -p python3 env35
source env35/bin/activate
pip3 install -r requirements3.txt


2. Run the web server & initialize the database with a few test records: 
cd docker-accessibility-capture/web
./run.sh

3. Run the docker containers 

4. Open 'localhost:5000'

