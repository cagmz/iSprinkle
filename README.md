# iSprinkle

## Warning: still under development and may or may not be a working build.

iSprinkle is an IoT sprinkler controller for the Raspberry Pi made using Bootstrap, Angular, and Flask. It's a web application that is hosted on the RPi itself and aims to reduce water usage by fetching the latest weather forecast and adjusting the user's set schedule using a ratio of the past weekly temperature and their desired watering duration.

Features:
- Dashboard with watering usage graph
- Advanced schedule
- Manual station activation
- Administration page with uptime and local IP

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contribute](#contribute)
- [License](#license)

## Install
This application can be run on both a RPi and a PC (the latter for testing).

1. Clone this repo:

        git clone https://github.com/cagmz/iSprinkle.git


2. CD into the repo, create a virtual environment, and activate it:

        sudo pip3 install virtualenv && virtualenv venv && source venv/bin/activate


3. Install iSprinkle dependencies:
   - On an RPi, use:

        ```
        pip install -r requirements.txt
        ```
        
   - If GPIO isn't available (eg on a PC), use:

        ```
        pip install -r requirements.no-gpio.txt
        ```


## Usage
Normal usage:
```
python3 iSprinkle.py
```

For running in the background, use:
```
nohup python3 iSprinkle.py &
```

Access from any web browser connected to your LAN:
```
<your RPi's local IP>:8080
```

## Contribute

PRs accepted.

## License

MIT © Richard McRichface
