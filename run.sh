#!/usr/bin/env bash

# move to script directory
cd ${BASH_SOURCE%/*}

echo "Program start."

# install dependancies
.clock_butler/bin/pip3.10 install -r requirements.txt

# run main script
.clock_butler/bin/python3.10 main.py

echo "Program stop."
