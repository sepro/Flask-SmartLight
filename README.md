[![GitHub release](https://img.shields.io/github/release/sepro/Flask-SmartLight.svg)](https://github.com/sepro/Flask-SmartLight) ![License](http://img.shields.io/:license-mit-blue.svg)

**NOTE**: This project has been archived. As the BlinkStick Square is supported by home assistant, this is a better way to control it using a smart phone. Albeit, lacking some of the animations included here. 

Flask-SmartLight Readme
=======================

Flask-SmartLight is a Python Flask app to turn a computer (e.g. a raspberry pi) connected to a BlinkStick Square into
a remote controlled smart light.

Installation
------------

Python >= 3.3 and pip3 are required


    sudo apt-get install python3
    sudo apt-get install pip3
    # or on some systems 
    sudo apt-get install python-pip3
      

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

Running the app
---------------

I ran into trouble running the app using the uwsgi version included in raspbian. The solution was to run uwsgi in the
virtual environment trough supervisor and hook that up to nginx.

Install **supervisor** and **nginx**

    sudo apt-get supervisor nginx
    
Install **uwsgi** through pip3 *within the virtual environment*

    # Activate the virtual environment if this isn't done so
    cd Flask-SmartLight/
    source venv/bin/activate

    # install uwsgi
    pip3 install uwsgi
    
To set up supervisor create a file called */etc/supervisor/conf.d/smartlight.conf*

    sudo nano /etc/supervisor/conf.d/smartlight.conf
    
Add these setting to this file: make sure to replace /home/sepro/git/Flask-SmartLight with the path on your machine!

    [program:smartlight]
    command=uwsgi -s /tmp/smartlight.sock -w smartlight:app --enable-threads -H /home/sepro/git/Flask-SmartLight/venv/ --uid www-data --gid www-data --chmod-socket=777
    directory=/home/sepro/git/Flask-SmartLight
    environment=PATH="/home/sepro/git/Flask-SmartLight/venv/bin"
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/smartlight.err.log
    stdout_logfile=/var/log/smartlight.out.log


To set up nginx create a file called */etc/nginx/sites-available/smartlight*

    sudo nano /etc/nginx/sites-available/smartlight

Add these settings to this file, it will bind the app to port 8000


    server {
            listen 8000 default_server;
            listen [::]:8000 default_server;
    
            server_name _;
            location / { try_files $uri @smartlight; }
            location @smartlight {
                include uwsgi_params;
                uwsgi_pass unix:/tmp/smartlight.sock;
            }
    }

Create a link to this file in /etc/nginx/sites-enabled

    sudo ln -s /etc/nginx/sites-available/smartlight /etc/nginx/sites-enabled/smartlight
    
Restart the deamons
  
    sudo service supervisor restart
    sudo service nginx restart
    
Check the supervisor log if everything is working

    cat /var/log/smartlight.err.log


Setting up usb for non-root on Raspberry pi
-------------------------------------------

    # add a group called usb and add the user to this group
    # replace <username> with the user's name
    sudo groupadd usb
    sudo usermod -a -G usb <username>
    
    # give this group access to usb devices
    sudo nano /etc/udev/rules.d/99-com.rules
    
    # **add** the line below
    SUBSYSTEM=="usb", GROUP="usb", MODE="0666"
    
    # restart the device with
    sudo reboot
    
