#!/bin/bash

#clone repo
git clone https://github.com/shelbylpz/linking_park.git
cd linking_park

# Create env and install requirements
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run app
python3 app/__init__.py