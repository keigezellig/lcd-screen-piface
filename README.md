# lcd-screen-piface
A 'higher level API' for a Piface CAD 2 LCD module

Contains:
- [Piface controller](/lcd_control): The basic API to the LCD. It is basically a wrapper around the Piface CAD libraries with some extra functionalties to make it work with multiple threads
- [Pager](/pager): A module which can be used to created paged screens more easily. This is also a showcase for the use of controller.

## Usage in your own projects
Add to you `requirements.txt` the following lines:
```
git+https://github.com/piface/pifacecad/#egg=pifacecad 
git+git://github.com/keigezellig/lcd-screen-piface#egg=lcd-screen-piface
```
The first line is to work around an issue that including `pifacecad` package in the setup.py doesn't work

## How to run the pager example
**You need a RPi and the Piface CAD 2 addon module**
- Clone this repo on your Pi
- Install the Piface CAD libraries on the Rpi (see [here](https://github.com/piface/pifacecad/))
- Run `make env` from the `examples` directory to make an virtual environment which installs all necessary python dependencies
- Run the example by executing `make run-pager` (also from the `examples` directory)

