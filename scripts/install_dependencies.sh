#!/bin/bash

# Install python 3 if not already installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Installing..."
    sudo apt update
    sudo apt install -y python3 python3-dev
else
    echo "Python 3 is already installed."
fi

# check if python3-venv is installed
if ! dpkg -l | grep -q python3-venv; then
    echo "python3-venv is not installed. Installing..."
    sudo apt install -y python3-venv
else
    echo "python3-venv is already installed."
fi

#install pip if not already installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Installing..."
    sudo apt install -y python3-pip
else
    echo "pip3 is already installed."
fi

# Install PDM if not already installed
if ! command -v pdm &> /dev/null; then
    echo "PDM is not installed. Installing..."
    curl -sSLO https://pdm-project.org/install-pdm.py
    curl -sSL https://pdm-project.org/install-pdm.py.sha256 | shasum -a 256 -c -
    # Run the installer
    python3 install-pdm.py
    rm install-pdm.py
else
    echo "PDM is already installed."
fi