#!/usr/bin/env bash

# move to script directory
cd ${BASH_SOURCE%/*}

echo "Program start."

if [ "$(git rev-parse HEAD)" = "$(git rev-parse origin/master)" ]; then
    echo "ADP But Better is up to date"
else
    echo "ADP But Better is NOT up to date with master"
    read -p "Would you like to update using git ? (y/n)" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # update local code
        git pull origin/master
        # install dependancies
        .venv/bin/pip3.10 install -r requirements.txt
    else
        echo "running out of date version..."
    fi
fi

# run main script
.venv/bin/python3.10 main.py

echo "Program stop."
