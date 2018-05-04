import datetime
import threading
from time import sleep

import pifacecad
import subprocess
from blinker import signal


class IntervalTimer(threading.Thread):
    def __init__(self, interval_in_seconds, function):
        super().__init__()
        self._isStopped = threading.Event()
        self._interval_in_seconds = interval_in_seconds
        self._timer_function = function

    def run(self):
        while not self._isStopped.is_set():
            sleep(self._interval_in_seconds)
            self._timer_function()

        self._isStopped.clear()

    def stop(self):
        self._isStopped.set()


class Page:
    def __init__(self):
        self.__lines = []

    @property
    def lines(self):
        return self.__lines

    @lines.setter
    def lines(self, value):
        self.__lines = value


class PageController:
    def __init__(self):
        self.__pages = []
        self.__active_page_id = None
        self.__page_changed = signal('page_changed')
        self.__text_updated = signal('text_updated')
        self.__text_updated.connect(self.__on_text_updated)

    def add_page(self, lines):
        page = Page()
        page.lines = lines
        self.__pages.append(page)

    def set_active_page(self, id):
        new = self.__pages[id]
        self.__active_page_id = id
        self.__page_changed.send(self, page=new, clear=True)

    def __on_text_updated(self, **kw):
        page_id = kw['id']
        text = kw['text']

        self.__pages[page_id].lines = text
        new = self.__pages[page_id]
        if self.__active_page_id == page_id:
            self.__page_changed.send(self, page=new, clear=False)


class DisplayController:
    def __init__(self, lcd):
        self.__lcd = lcd
        self.__page_changed = signal('page_changed')
        self.__page_changed.connect(self.__display_page)

    def __display_page(self, sender, **kw):
        text = kw['page'].lines
        self.__lcd.display_text(textlines=text, location=None, should_clear=kw['clear'])




class PiFaceController:
    BUTTON_0 = 0
    BUTTON_1 = 1
    BUTTON_2 = 2
    BUTTON_3 = 3
    BUTTON_4 = 4
    ROCKER_PRESS = 5
    ROCKER_LEFT = 6
    ROCKER_RIGHT = 7

    def __init__(self):
        self.__piface = pifacecad.PiFaceCAD()
        self.__piface.lcd.backlight_on()
        self.__piface.lcd.cursor_off()
        self.__piface.lcd.blink_off()

        self.__button0_pressed = signal('button0_pressed')
        self.__button1_pressed = signal('button1_pressed')
        self.__button2_pressed = signal('button2_pressed')
        self.__button3_pressed = signal('button3_pressed')
        self.__button4_pressed = signal('button4_pressed')
        self.__rocker_pressed = signal('rocker_pressed')
        self.__rocker_left_pressed = signal('rocker_left_pressed')
        self.__rocker_right_pressed = signal('rocker_right_pressed')

    def init(self):
        listener = pifacecad.SwitchEventListener(chip=self.__piface)
        for i in range(8):
            listener.register(i, pifacecad.IODIR_FALLING_EDGE, self.__handle_button)

        listener.activate()

    def __handle_button(self, event):
        if event.pin_num == self.BUTTON_0:
            self.__button0_pressed.send(self)
        elif event.pin_num == self.BUTTON_1:
            self.__button1_pressed.send(self)
        elif event.pin_num == self.BUTTON_2:
            self.__button2_pressed.send(self)
        elif event.pin_num == self.BUTTON_3:
            self.__button3_pressed.send(self)
        elif event.pin_num == self.BUTTON_4:
            self.__button4_pressed.send(self)
        elif event.pin_num == self.ROCKER_PRESS:
            self.__rocker_pressed.send(self)
        elif event.pin_num == self.ROCKER_LEFT:
            self.__rocker_left_pressed.send(self)
        elif event.pin_num == self.ROCKER_RIGHT:
            self.__rocker_right_pressed.send(self)

    def display_text(self, textlines, location, should_clear):
        if len(textlines[0]) < 16:
            textlines[0] = '{:16}'.format(textlines[0])

        if len(textlines[1]) < 16:
            textlines[1] = '{:16}'.format(textlines[1])

        lcd = self.__piface.lcd
        if should_clear:
            lcd.clear()

        if location is not None and len(textlines) == 1:
            lcd.set_cursor(location[1], location[0])
            lcd.write(textlines[0])
        else:
            for i, item in enumerate(textlines):
                lcd.set_cursor(0, i)
                lcd.write(item)

    def scroll_right(self, number_of_positions=1):
        lcd = self.__piface.lcd
        for j in range(number_of_positions):
            lcd.move_left()

    def scroll_left(self, number_of_positions=1):
        lcd = self.__piface.lcd
        for j in range(number_of_positions):
            lcd.move_right()

    def home(self):
        lcd = self.__piface.lcd
        lcd.home()

    def display_scrolling_text(self, textlines, direction, number_of_positions, delay):
        lcd = self.__piface.lcd
        self.display_text(textlines=textlines, location=None, should_clear=True)
        if direction != "both":
            for j in range(number_of_positions):
                if direction == "left":
                    lcd.move_right()
                    sleep(delay)
                elif direction == "right":
                    lcd.move_left()
                    sleep(delay)
        else:
            for k in range(number_of_positions):
                lcd.move_left()
                sleep(delay)

            for l in range(number_of_positions * 2):
                lcd.move_right()
                sleep(delay)

            lcd.home()


GET_IP_CMD = "hostname --all-ip-addresses"
curr_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')


def get_my_ip():
    return run_cmd(GET_IP_CMD)[:-1]


def display_ip(sender):
    pageController.set_active_page(0)


def display_time(sender=None):
    pageController.set_active_page(1)

def update_time(sender=None):
    updated_text = signal('text_updated')
    curr_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    updated_text.send(sender=None, id=0, text=["Current time", curr_time])


if __name__ == '__main__':
    piFaceController = PiFaceController()
    displayController = DisplayController(lcd=piFaceController)
    pageController = PageController()

    pageController.add_page(["IP: {ip}".format(ip=get_my_ip()), "S/W: 3.0.323234a"])
    pageController.add_page(["Current time", curr_time])

    btn_0 = signal('button0_pressed')
    btn_1 = signal('button1_pressed')

    btn_0.connect(display_ip)
    btn_1.connect(display_time)

    timer = IntervalTimer(interval_in_seconds=1, function=update_time)
    timer.start()

    pageController.set_active_page(0)
    piFaceController.init()
