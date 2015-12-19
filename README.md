[![GitHub release](https://img.shields.io/github/release/sepro/Flask-SmartLight.svg)](https://github.com/sepro/Flask-SmartLight) ![License](http://img.shields.io/:license-mit-blue.svg)

Flask-SmartLight Readme
=======================

Flask-SmartLight is a Python Flask app to turn a computer (e.g. a raspberry pi) connected to a BlinkStick Square into
a remote controlled smart light.

Installation
------------

Python >= 3.3 and pip3 are required

    sudo apt-get install python3
    sudo apt-get install pip3 *or* sudo apt-get install python-pip3
    

Install virtualenv

    sudo pip3 install virtualenv


Clone the repository into a directory CookieRunner

    git clone https://github.com/sepro/Flask-SmartLight.git Flask-SmartLight

Set up the virtual environment
  
    virtualenv --python=python3 Flask-SmartLight/venv

Activate the virtual environment

    cd Flask-SmartLight/
    source venv/bin/activate

Install the requirements

    pip3 install -r requirements.txt

Copy the configuration template to config.py

    cp config.template.py config.py

Change settings in config.py

Setting up usb for non-root on Raspberry pi
-------------------------------------------

    # add a group called usb and add the user to this group
    # replace <username> with the user's name
    sudo groupadd usb
    sudo usermod -G usb -a <username>
    
    # give this group access to usb devices
    sudo nano /etc/udev/rules.d/99-com.rules
    
    # **add** the line below
    SUBSYSTEM=="usb", GROUP="usb", MODE="0666"
    
    # restart the device with
    sudo reboot
    