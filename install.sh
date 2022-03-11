#!/usr/bin/env bash

RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m'

OK="${GREEN} > ${NC}"
WARNING="${ORANGE} > ${NC}"
ERROR="${RED} > ${NC}"

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "${OK}runing MacOS install script"
    py_error="$(python3 -c 'import sys; print(1) if sys.version_info.major < 3 and sys.version_info.minor < 10 else print(0)')"
    if [[ $py_error == "1" ]]; then
        echo "${ERROR}python version error = ${BLUE}$(python3 --version)${NC}"
        echo "${ERROR}please install python in version >= 3.10.0"
        echo "${ERROR}using 'brew install python@3.10'"
        exit 1
    else
        echo "${OK}valid python version detected = ${BLUE}$(python3 --version)${NC}"
    fi

    echo "${OK}creating python virtual environment"
    python3 -m venv .venv

    echo "${OK}updating local project with git"
    git checkout master
    git pull

    echo "${OK}updating python requirements"
    .venv/bin/pip3 install -r requirements.txt

    echo "${OK}initializing settings file"
    python3 -c "from adp_wrapper.constants import reset_settings as res_set; res_set()"
    code config.json

    echo "${OK}done."

    echo "${OK}you can now add the ${BLUE}run.sh${NC} file to your shortcuts by copying this line to your ${BLUE}~/.zshrc${NC}"
    alias_command="alias adp=\"$(pwd)/run.sh\""
    echo "\t${alias_command}"

    read -p "Would you like to do it now ? (y/n)" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo $alias_command >>~/.zshrc
        code ~/.zshrc
    fi

else

    echo "${ERROR}operating system not yet supported for automatic install"
fi
