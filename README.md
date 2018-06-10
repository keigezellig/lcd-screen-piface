# lcd-screen-piface
Some modules to create screens more easily for a Piface CAD 2


- [Pager](/pager): A screen consisting of multiple pages with assignable actions to the PifaceCAD buttons

## Usage in your own projects
See the examples

## How to run the examples
**You need a RPi and the Piface CAD 2 addon module**
- Clone this repo on your Pi
- Install the Piface CAD libraries on the Rpi (see [here](https://github.com/piface/pifacecad/))
- Run `make env` to make an virtual environment which installs all necessary python dependencies
- Run an example by executing `python3 *_example` on the Pi where * is for example `pager`
