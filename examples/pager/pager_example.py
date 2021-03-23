# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)

# from lcd_control.hw.pifacecad_interface import PiFaceCadInterface
# from lcd_control.piface_controller import PiFaceController
# from pager.page_controller import PageController


import datetime
import logging
from time import sleep

from lcd_control.hw.dummy_lcd_interface import DummyInterface

log = logging.getLogger(__name__)
from lcd_control.hw.pifacecad_interface import PiFaceCadInterface
from lcd_control.piface_controller import PiFaceController
from pager.page_controller import PageController

from timer_functions import RepeatedTimer

lcd_controller: PiFaceController = PiFaceController(PiFaceCadInterface())
page_controller: PageController = PageController(lcd_controller=lcd_controller)
count_a: int = 0
count_b: int = 0


def actionA():
    lcd_controller.display_screen(textlines=["Action A"], location=None, should_clear=True)
    sleep(5)
    page_controller.display()


def actionB():
    lcd_controller.display_screen(textlines=["Action B"], location=None, should_clear=True)
    sleep(5)
    page_controller.display()


def actionC():
    lcd_controller.display_screen(textlines=["Action C"], location=None, should_clear=True)
    sleep(5)
    page_controller.display()


def actionD():
    lcd_controller.display_screen(textlines=["Action D"], location=None, should_clear=True)
    sleep(5)
    page_controller.display()


def actionE():
    lcd_controller.display_screen(textlines=["Action E"], location=None, should_clear=True)
    sleep(5)
    page_controller.display()


def play():
    lcd_controller.display_screen(textlines=["Play"], location=None, should_clear=True)
    sleep(5)
    page_controller.display()


def pause():
    lcd_controller.display_screen(textlines=["Pause"], location=None, should_clear=True)
    sleep(5)
    page_controller.display()


def stop():
    lcd_controller.display_screen(textlines=["Stop"], location=None, should_clear=True)
    sleep(5)
    page_controller.display()


def record():
    lcd_controller.display_screen(textlines=["Record"], location=None, should_clear=True)
    sleep(5)
    page_controller.display()


def standby():
    lcd_controller.display_screen(textlines=["Standby"], location=None, should_clear=True)
    sleep(5)
    page_controller.display()


def update_time(pager: PageController):
    curr_date = datetime.datetime.now().strftime("%d-%b-%Y")
    curr_time = datetime.datetime.now().strftime("%H:%M:%S")
    pager.update_page(page_index=0, new_content={"line1": curr_date, "line2": curr_time})

    global count_a
    pager.update_page(page_index=4, new_content={"line1": count_a})
    count_a += 1


def update_time_2(pager: PageController):
    global count_b
    pager.update_page(page_index=4, new_content={"line2": count_b})
    count_b += 2


def create_pages():
    bitmaps = {"play": [0x0, 0x8, 0xc, 0xe, 0xc, 0x8, 0x0, 0x0],
               "pause": [0x0, 0xa, 0xa, 0xa, 0xa, 0xa, 0x0, 0x0],
               "stop": [0x0, 0xe, 0xe, 0xe, 0xe, 0xe, 0x0, 0x0],
               "record": [0x0, 0xe, 0x1f, 0x1f, 0x1f, 0xe, 0x0, 0x0],
               "standby": [0x4, 0xe, 0x15, 0x15, 0x11, 0xe, 0x0, 0x0]}

    pages = [{"line1": "",
              "line2": ""},
             {"caption": "P1 (labels)",
              "actions": [{"label": "A", "action": actionA},
                          {"label": "B", "action": actionB},
                          {"label": "C", "action": actionC},
                          {"label": "D", "action": actionD},
                          {"label": "E", "action": actionE}]},
             {"caption": "P2 (bitmaps)",
              "actions": [{"bitmap": bitmaps["play"], "action": play},
                          {"bitmap": bitmaps["pause"], "action": pause},
                          {"bitmap": bitmaps["stop"], "action": stop},
                          {"bitmap": bitmaps["record"], "action": record},
                          {"bitmap": bitmaps["standby"], "action": standby}]},
             {"caption": "P3 (less actions)",
              "actions": [{"label": "A", "action": actionA},
                          {"label": "B", "action": actionB},
                          {"label": "C", "action": actionC}]},
             {"line1": "",
              "line2": ""},
             ]
    return pages


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(module)s.%(funcName)s - %(message)s')

    timer = RepeatedTimer(1.0, update_time, page_controller)
    timer2 = RepeatedTimer(2.0, update_time_2, page_controller)

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
        timer2.start()

        while True:
            sleep(0.1)

    except KeyboardInterrupt:
        timer2.stop()
        timer.stop()
        lcd_controller.close()
