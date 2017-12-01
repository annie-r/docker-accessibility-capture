#!/bin/bash

# CouchdB configuation
export COUCHDBSERVER="http://127.0.0.1:5984"
export COUCHDBNAME="accessibility"

export FLASK_APP=server.py
export FLASK_DEBUG=1
flask run