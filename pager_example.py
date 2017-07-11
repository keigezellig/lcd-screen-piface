import pifacecad
from time import sleep

from pager import PagedScreen

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


def createPagesForScreen():
    pages = [{"text": "This is page 1",
              "actions": [{"label": "A", "action": "actionA"}, {"label": "B", "action": "actionB"},
                          {"label": "C", "action": "actionC"}, {"label": "D", "action": "actionD"},
                          {"label": "E", "action": "actionE"}]},
             {"text": "This is page 2",
              "actions": [{"label": "A2", "action": "actionA"}, {"label": "B2", "action": "actionB"},
                          {"label": "C2", "action": "actionC"}, {"label": "D2", "action": "actionD"},
                          {"label": "E2", "action": "actionE"}]}
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
