# lcd-screen-piface
A 'higher level API' for a Piface CAD 2 LCD module

Contains:
- [Piface controller](/lcd_control): The basic API to the LCD. It is basically a wrapper around the Piface CAD libraries with some extra functionalties to make it work with multiple threads
- [Pager](/pager): A module which can be used to created paged screens more easily. This is also a showcase for the use of controller.

## Usage in your own projects
# TODO

## How to run the pager example
**You need a RPi and the Piface CAD 2 addon module**
- Clone this repo on your Pi
- Install the Piface CAD libraries on the Rpi (see [here](https://github.com/piface/pifacecad/))
- Run `make env` to make an virtual environment which installs all necessary python dependencies
- Run the example by executing `python3 pager_example` on the Pi from the `pager` subdirectory

