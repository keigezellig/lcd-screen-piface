import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from lcd_control.hw.pifacecad_interface import PiFaceCadInterface
from lcd_control.piface_controller import PiFaceController
from pager.screen import Screen

import logging
from time import sleep


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


def createPagesForScreen():
    bitmaps = {"play": [0x0, 0x8, 0xc, 0xe, 0xc, 0x8, 0x0, 0x0],
               "pause": [0x0, 0xa, 0xa, 0xa, 0xa, 0xa, 0x0, 0x0],
               "stop": [0x0, 0xe, 0xe, 0xe, 0xe, 0xe, 0x0, 0x0],
               "record": [0x0, 0xe, 0x1f, 0x1f, 0x1f, 0xe, 0x0, 0x0],
               "standby": [0x4, 0xe, 0x15, 0x15, 0x11, 0xe, 0x0, 0x0]}

    pages = [{"text": "P0 (labels)",
              "actions": [{"label": "A", "action": "pager_example.actionA"},
                          {"label": "B", "action": "pager_example.actionB"},
                          {"label": "C", "action": "pager_example.actionC"},
                          {"label": "D", "action": "pager_example.actionD"},
                          {"label": "E", "action": "pager_example.actionE"}]},
             {"text": "P1 (bitmaps)",
              "actions": [{"bitmap": bitmaps["play"], "action": "pager_example.play"},
                          {"bitmap": bitmaps["pause"], "action": "pager_example.pause"},
                          {"bitmap": bitmaps["stop"], "action": "pager_example.stop"},
                          {"bitmap": bitmaps["record"], "action": "pager_example.record"},
                          {"bitmap": bitmaps["standby"], "action": "pager_example.standby"}]},
             {"text": "P2 with no actions",
              "actions": []},
             {"text": "P3 (less actions)",
              "actions": [{"label": "A", "action": "pager_example.actionA"},
                          {"label": "B", "action": "pager_example.actionB"},
                          {"label": "C", "action": "pager_example.actionC"}]}
             ]
    return pages


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    lcd_controller: PiFaceController = PiFaceController(PiFaceCadInterface())
    screen: Screen = Screen(page_definitions=createPagesForScreen(), lcd_controller=lcd_controller)

    try:
        lcd_controller.start()
        lcd_controller.display_scrolling_text(textlines=["Welcome to Acme LCD"], direction="right",
                                   number_of_positions=22,
                                   delay=.1)
        screen.display(1)

        while True:
            sleep(0.1)

    except KeyboardInterrupt:
        lcd_controller.close()
