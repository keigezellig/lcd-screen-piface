import os, sys

# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)

# from lcd_control.hw.pifacecad_interface import PiFaceCadInterface
# from lcd_control.piface_controller import PiFaceController
# from pager.page_controller import PageController


import logging
from time import sleep
import datetime

from lcd_control.hw.pifacecad_interface import PiFaceCadInterface
from lcd_control.piface_controller import PiFaceController
from pager.page_controller import PageController

from timer_functions import RepeatedTimer


def actionA(pager, lcd):
    lcd.display_text(textlines=["Action A"], location=None, should_clear=True)
    sleep(5)
    pager.display()


def actionB(pager, lcd):
    lcd.display_text(textlines=["Action B"], location=None, should_clear=True)
    sleep(5)
    pager.display()


def actionC(pager, lcd):
    lcd.display_text(textlines=["Action C"], location=None, should_clear=True)
    sleep(5)
    pager.display()


def actionD(pager, lcd):
    lcd.display_text(textlines=["Action D"], location=None, should_clear=True)
    sleep(5)
    pager.display()


def actionE(pager, lcd):
    lcd.display_text(textlines=["Action E"], location=None, should_clear=True)
    sleep(5)
    pager.display()


def play(pager, lcd):
    lcd.display_text(textlines=["Play"], location=None, should_clear=True)
    sleep(5)
    pager.display()


def pause(pager, lcd):
    lcd.display_text(textlines=["Pause"], location=None, should_clear=True)
    sleep(5)
    pager.display()


def stop(pager, lcd):
    lcd.display_text(textlines=["Stop"], location=None, should_clear=True)
    sleep(5)
    pager.display()


def record(pager, lcd):
    lcd.display_text(textlines=["Record"], location=None, should_clear=True)
    sleep(5)
    pager.display()


def standby(pager, lcd):
    lcd.display_text(textlines=["Standby"], location=None, should_clear=True)
    sleep(5)
    pager.display()


def update_time(pager: PageController, lcd):
    curr_date = datetime.datetime.now().strftime("%d-%b-%Y")
    curr_time = datetime.datetime.now().strftime("%H:%M:%S")
    pager.update_page(page_index=0, new_content={"line1": curr_date, "line2": curr_time})


def create_pages():
    bitmaps = {"play": [0x0, 0x8, 0xc, 0xe, 0xc, 0x8, 0x0, 0x0],
               "pause": [0x0, 0xa, 0xa, 0xa, 0xa, 0xa, 0x0, 0x0],
               "stop": [0x0, 0xe, 0xe, 0xe, 0xe, 0xe, 0x0, 0x0],
               "record": [0x0, 0xe, 0x1f, 0x1f, 0x1f, 0xe, 0x0, 0x0],
               "standby": [0x4, 0xe, 0x15, 0x15, 0x11, 0xe, 0x0, 0x0]}

    pages = [{"line1": "",
              "line2": ""},
             {"caption": "P1 (labels)",
              "actions": [{"label": "A", "action": "pager_example.actionA"},
                          {"label": "B", "action": "pager_example.actionB"},
                          {"label": "C", "action": "pager_example.actionC"},
                          {"label": "D", "action": "pager_example.actionD"},
                          {"label": "E", "action": "pager_example.actionE"}]},
             {"caption": "P2 (bitmaps)",
              "actions": [{"bitmap": bitmaps["play"], "action": "pager_example.play"},
                          {"bitmap": bitmaps["pause"], "action": "pager_example.pause"},
                          {"bitmap": bitmaps["stop"], "action": "pager_example.stop"},
                          {"bitmap": bitmaps["record"], "action": "pager_example.record"},
                          {"bitmap": bitmaps["standby"], "action": "pager_example.standby"}]},
             {"caption": "P3 (less actions)",
              "actions": [{"label": "A", "action": "pager_example.actionA"},
                          {"label": "B", "action": "pager_example.actionB"},
                          {"label": "C", "action": "pager_example.actionC"}]},
             ]
    return pages


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(module)s.%(funcName)s - %(message)s')

    lcd_controller: PiFaceController = PiFaceController(PiFaceCadInterface())
    page_controller: PageController = PageController(lcd_controller=lcd_controller)
    timer = RepeatedTimer(1.0, update_time, page_controller, lcd_controller)

    try:
        lcd_controller.start()
        page_definitions = create_pages()
        for page_def in page_definitions:
            page_controller.add_page(page_def)

        lcd_controller.display_scrolling_text(textlines=["Welcome to Acme LCD"], direction="right",
                                              number_of_positions=22,
                                              delay=.1)
        page_controller.display()
        timer.start()

        while True:
            sleep(0.1)

    except KeyboardInterrupt:
        timer.stop()
        lcd_controller.close()
