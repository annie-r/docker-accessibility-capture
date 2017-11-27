#!/bin/bash

# CouchdB configuation
export COUCHDBSERVER="http://127.0.0.1:5984"
export COUCHDBNAME="accessibility"

# Initialize test database if needed
python3 setup.py

# export FLASK_APP=server.py
# flask run