#!/bin/bash
sudo apt install python3-pip
sudo pip3 install virtualenv
virtualenv venv --python=python3.6
source venv/bin/activate
venv/bin/pip3 install -r requirements.txt
