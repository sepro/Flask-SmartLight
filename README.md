[![GitHub release](https://img.shields.io/github/release/Flask-SmartLight/rubidium.svg)]() [![Github Releases](https://img.shields.io/github/downloads/sepro/Flask-SmartLight/latest/total.svg)]() 

Flask-SmartLight Readme
=======================

Flask-SmartLight is a Python Flask app to turn a computer (e.g. a raspberry pi) connected to a BlinkStick Square into
a remote controlled smart light.

Installation
------------

Python >= 3.3 and pip3 are required

    sudo apt-get install python3
    sudo apt-get install pip3

Install virtualenv

    sudo pip3 install virtualenv


Clone the repository into a directory CookieRunner

    git clone https://github.com/sepro/Flask-SmartLight.git Flask-SmartLight

Set up the virtual environment
  
    virtualenv --python=python3 Flask-SmartLight/

Activate the virtual environment

    cd Flask-SmartLight/
    source bin/activate

Install the requirements

    pip3 install -r requirements.txt

Copy the configuration template to config.py

    cp config.template.py config.py

Change settings in config.py