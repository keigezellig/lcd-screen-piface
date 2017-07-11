import pifacecad
from time import sleep

from pager import PagedScreen

cad = pifacecad.PiFaceCAD()
lcd = cad.lcd
lcd.backlight_on()

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


def createPagesForScreen():
    pages = [{"text": "This is page 1",
              "actions": [{"label": "A", "action": "pager_example.actionA"}, {"label": "B", "action": "pager_example.actionB"},
                          {"label": "C", "action": "pager_example.actionC"}, {"label": "D", "action": "pager_example.actionD"},
                          {"label": "E", "action": "pager_example.actionE"}]},
             {"text": "This is page 2",
              "actions": [{"label": "F", "action": "pager_example.actionA"}, {"label": "G", "action": "pager_example.actionB"},
                          {"label": "H", "action": "pager_example.actionC"}, {"label": "I", "action": "pager_example.actionD"},
                          {"label": "J", "action": "pager_example.actionE"}]}
             ]
    return pages


if __name__ == '__main__':

    screen1 = PagedScreen(cad=cad, pages=createPagesForScreen())
    # screen2 = PagedScreen(lcd=lcd, pages=getPagesForScreen2())
    screen1.display(page=0)
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        screen1.clean_up()
