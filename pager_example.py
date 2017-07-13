import threading

import pifacecad
from time import sleep

from pager import PagedScreen

global end_barrier
end_barrier = threading.Barrier(2)
cad = pifacecad.PiFaceCAD()
lcd = cad.lcd


def actionA(pager):
    lcd.clear()
    lcd.write("Action A")
    sleep(5)
    pager.display()


def actionB(pager):
    lcd.clear()
    lcd.write("Action B")
    sleep(5)
    pager.display()


def actionC(pager):
    lcd.clear()
    lcd.write("Action C")
    sleep(5)
    pager.display()


def actionD(pager):
    lcd.clear()
    lcd.write("Action D")
    sleep(5)
    pager.display()


def actionE(pager):
    lcd.clear()
    lcd.write("Action E")
    sleep(5)
    pager.display()

def play(pager):
    lcd.clear()
    lcd.write("Play")
    sleep(5)
    pager.display()

def pause(pager):
    lcd.clear()
    lcd.write("Pause")
    sleep(5)
    pager.display()

def stop(pager):
    lcd.clear()
    lcd.write("Stop")
    sleep(5)
    pager.display()

def record(pager):
    lcd.clear()
    lcd.write("Record")
    sleep(5)
    pager.display()

def standby(pager):
    lcd.clear()
    lcd.write("Standby")
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

    screen1 = PagedScreen(cad=cad, pages=createPagesForScreen())

    try:
        lcd.backlight_on()
        screen1.display(page=0)
        end_barrier.wait()
    except KeyboardInterrupt:
        screen1.clean_up()
        cad.lcd.write("Goodbye")
        sleep(2)
        cad.lcd.clear()
        cad.lcd.backlight_off()
        cad.lcd.cursor_off()
