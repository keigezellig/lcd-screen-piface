import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import datetime
import logging
import subprocess
from time import sleep

from lcd_control.hw.pifacecad_interface import PiFaceCadInterface
from simple_pager.page import PageController
from lcd_control.piface_controller import PiFaceController
from simple_pager.timer_functions import RepeatedTimer

log = logging.getLogger(__name__)

GET_IP_CMD = "hostname --all-ip-addresses"
curr_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')


def get_my_ip():
    return run_cmd(GET_IP_CMD)[:-1]


def display_ip(sender):
    pageController.set_active_page(0)


def display_time(sender):
    pageController.set_active_page(1)


def display_sample(sender):
    pageController.set_active_page(2)


def change_text(sender):
    pageController.update_text(page_id=2, new_lines=["Changed text", "to something else"])


def next_page(sender):
    pageController.goto_next_page()


def previous_page(sender):
    pageController.goto_previous_page()


def home_page(sender):
    pageController.set_active_page(0)

def update_time():
    log.debug("TICK")
    curr_time = datetime.datetime.now().strftime("%S")
    pageController.update_text(page_id=1, new_lines=["Current time", curr_time])


def reboot(sender):
    piFaceController.display_text(textlines=["Rebooting in 5 secs"], location=None, should_clear=True)
    sleep(5)
    piFaceController.clear()
    piFaceController.backlight_off()
   # os.system("sudo reboot")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    piFaceController = PiFaceController(PiFaceCadInterface())
    pageController = PageController(lcd_controller=piFaceController)
    pageController.add_page(["IP: {ip}".format(ip=get_my_ip()), "S/W: 3.0.323234a"])
    pageController.add_page(["Current time", curr_time])
    pageController.add_page(["Sample text"])

    piFaceController.set_button_eventhandler(button=piFaceController.BUTTON_0, handler=display_ip)
    piFaceController.set_button_eventhandler(button=piFaceController.BUTTON_1, handler=display_time)
    piFaceController.set_button_eventhandler(button=piFaceController.BUTTON_2, handler=display_sample)
    piFaceController.set_button_eventhandler(button=piFaceController.BUTTON_3, handler=change_text)
    piFaceController.set_button_eventhandler(button=piFaceController.BUTTON_4, handler=reboot)
    piFaceController.set_button_eventhandler(button=piFaceController.ROCKER_LEFT, handler=previous_page)
    piFaceController.set_button_eventhandler(button=piFaceController.ROCKER_RIGHT, handler=next_page)
    piFaceController.set_button_eventhandler(button=piFaceController.ROCKER_PRESS, handler=home_page)

    timer = RepeatedTimer(1.0, update_time)

    try:
        piFaceController.start()
        piFaceController.display_scrolling_text(textlines=["Welcome to Acme LCD"], direction="right",
                                                number_of_positions=22,
                                                delay=.1)

        pageController.set_active_page(0)

        timer.start()

        while True:
            sleep(0.1)

    except KeyboardInterrupt:
        timer.stop()
        piFaceController.close()
