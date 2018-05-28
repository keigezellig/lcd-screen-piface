import datetime
import os
import subprocess
from time import sleep

from simple_pager import PiFaceController, PageController

GET_IP_CMD = "hostname --all-ip-addresses"
curr_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

piFaceController = PiFaceController()
pageController = PageController(lcd_controller=piFaceController)


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


def reboot(sender):
    piFaceController.display_text(textlines=["Rebooting in 5 secs"], location=None, should_clear=True)
    sleep(5)
    piFaceController.clear()
    piFaceController.backlight_off()
    os.system("sudo reboot")


def run_example():
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

    piFaceController.display_scrolling_text(textlines=["Welcome to Acme LCD"], direction="right",
                                            number_of_positions=22,
                                            delay=.1)

    piFaceController.init()
    pageController.set_active_page(0)
