#!/usr/bin/env bash

echo "Program start."

update_requirements="false"

while getopts 'u' flag; do
    case "${flag}" in
    u)
        update_requirements="true"
        ;;
    *)
        echo "invalid argument $@"
        exit 1
        ;;
    esac
done

# move to script directory
cd ${BASH_SOURCE%/*}

if [ "$(git rev-parse HEAD)" = "$(git rev-parse origin/master)" ]; then
    echo "ADP But Better is up to date"

else
    echo "ADP But Better is NOT up to date with master"
    read -p "Would you like to update using git ? (y/n)" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # update local code
        echo "checking out master branch :"
        git checkout master
        echo "pulling changes :"
        git pull
        echo "running new script version right now"
        exec "$0" "-u"
        exit 1
    else
        echo "running out of date version..."
    fi
fi

if [ "$update_requirements" = "true" ]; then
    # install dependancies
    echo "updating python requirements"
    .venv/bin/pip3 install -r requirements.txt
fi

# run main script
.venv/bin/python3 main.py

echo "Program stop."
