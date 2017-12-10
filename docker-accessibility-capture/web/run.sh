#!/bin/bash

# CouchdB configuation
export COUCHDBSERVER="http://127.0.0.1:5984"
export COUCHDBNAME="accessibility"
export FILESERVER="/Users/Amanda/GitHub/docker-accessibility-capture/docker-accessibility-capture/shared_files"

# Initialize test database if needed
python3 setup.py

export FLASK_APP=server.py
# export FLASK_DEBUG=1
flask run