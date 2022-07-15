#!/usr/bin/env bash

RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m'

OK="${GREEN} > ${NC}"
WARNING="${ORANGE} > ${NC}"
ERROR="${RED} > ${NC}"

echo "you are installing adp but better on your machine, proceed at your own risk"

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "${OK}running auto install script for ${BLUE}MacOS${NC}"
    py_error="$(python3 -c 'import sys; print(0) if sys.version_info.major == 3 and sys.version_info.minor >= 9 else print(1)')"
    if [[ $py_error == "1" ]]; then
        echo "${ERROR}python version error = ${BLUE}$(python3 --version)${NC}"
        echo "${ERROR}please install python3 in version >= 3.9"
        echo "${ERROR}managing python versions can be a pain, maybe this tool can help you : https://github.com/pyenv/pyenv"
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

elif [[ "$OSTYPE" == "linux"* ]]; then
    echo -e "${OK}running auto install script for ${BLUE}Linux${NC}"
    py_error="$(python3 -c 'import sys; print(0) if sys.version_info.major == 3 and sys.version_info.minor >= 9 else print(1)')"
    if [[ $py_error == "1" ]]; then
        echo -e "${ERROR}python version error = ${BLUE}$(python3 --version)${NC}"
        echo -e "${ERROR}please install python3 in version >= 3.9"
        echo -e "${ERROR}managing python versions can be a pain, maybe this tool can help you : https://github.com/pyenv/pyenv"
        exit 1
    else
        echo -e "${OK}valid python version detected = ${BLUE}$(python3 --version)${NC}"
    fi

    echo -e "${OK}creating python virtual environment"
    python3 -m venv .venv

    echo -e "${OK}updating local project with git"
    git checkout master
    git pull

    echo -e "${OK}updating python requirements"
    .venv/bin/pip3 install -r requirements.txt

    echo -e "${OK}initializing settings file"
    python3 -c "from adp_wrapper.constants import reset_settings as res_set; res_set()"
    code config.json

    echo -e "${OK}done."

    echo -e "${WARNING} current shell : ${BLUE}${SHELL}${NC}"

    echo -e "${OK}you can now add the ${BLUE}run.sh${NC} file to your shortcuts by copying this line to your ${BLUE}~/.zshrc${NC} (or ~./bashrc)"
    alias_command="alias adp=\"$(pwd)/run.sh\""
    echo -e "\t${alias_command}"

else

    echo "operating system (${OSTYPE}) not yet supported for automatic install"
fi
