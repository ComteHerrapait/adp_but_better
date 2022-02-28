#!/usr/bin/env bash

# move to script directory
cd ${BASH_SOURCE%/*}

echo "Program start."

# install dependancies
.venv/bin/pip3.10 install -r requirements.txt

# run main script
.venv/bin/python3.10 main.py

echo "Program stop."
