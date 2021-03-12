import logging
import threading
from queue import Queue
from typing import List, Tuple

from blinker import signal

from simple_pager.lcd_worker import LCDWorker

log = logging.getLogger(__name__)


class QueuedPiFaceController:
    BUTTON_0 = 0
    BUTTON_1 = 1
    BUTTON_2 = 2
    BUTTON_3 = 3
    BUTTON_4 = 4
    ROCKER_PRESS = 5
    ROCKER_LEFT = 6
    ROCKER_RIGHT = 7

    def __init__(self):
        self._queue: Queue = Queue(maxsize=1)
        self._worker = LCDWorker(queue=self._queue)
        self._init_button_signals()

    def _init_button_signals(self):
        self.__button0_pressed = signal('button0_pressed')
        self.__button1_pressed = signal('button1_pressed')
        self.__button2_pressed = signal('button2_pressed')
        self.__button3_pressed = signal('button3_pressed')
        self.__button4_pressed = signal('button4_pressed')
        self.__rocker_pressed = signal('rocker_pressed')
        self.__rocker_left_pressed = signal('rocker_left_pressed')
        self.__rocker_right_pressed = signal('rocker_right_pressed')

    def _handle_button(self, event):
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

    def set_button_eventhandler(self, button, handler):
        signal_name = ''
        if self.BUTTON_0 <= button <= self.BUTTON_4:
            signal_name = 'button{button}_pressed'.format(button=button)
        elif button == self.ROCKER_PRESS:
            signal_name = 'rocker_pressed'
        elif button == self.ROCKER_LEFT:
            signal_name = 'rocker_left_pressed'
        elif button == self.ROCKER_RIGHT:
            signal_name = 'rocker_right_pressed'

        if signal_name == '':
            log.warning("Invalid button argument, will do nothing")

        signal(name=signal_name).connect(handler)

    def init(self):
        self._worker.init()
        self._worker.init_key_listener(key_handler=self._handle_button)
        threading.Thread(target=self._worker.process_lcd_commands, daemon=True).start()

    def display_text(self, textlines: List[str], location: Tuple[int, int], should_clear: bool):
        item = ('display_text', {'text_lines': textlines, 'location': location, 'should_clear': should_clear})
        self._queue.put(item)

    def scroll_right(self, number_of_positions=1):
        item = ('scroll_right', {'number_of_positions': number_of_positions})
        self._queue.put(item)

    def scroll_left(self, number_of_positions=1):
        item = ('scroll_left', {'number_of_positions': number_of_positions})
        self._queue.put(item)

    def home(self):
        item = ('home', {})
        self._queue.put(item)

    def display_scrolling_text(self, textlines, direction, number_of_positions, delay):
        item = ('display_scrolling_text',
                {'text_lines': textlines, 'direction': direction, 'number_of_positions': number_of_positions,
                 'delay': delay})
        self._queue.put(item)

    def backlight_on(self):
        item = ('backlight_on', {})
        self._queue.put(item)

    def backlight_off(self):
        item = ('backlight_off', {})
        self._queue.put(item)

    def cursor_on(self):
        item = ('cursor_on', {})
        self._queue.put(item)

    def cursor_off(self):
        item = ('cursor_off', {})
        self._queue.put(item)

    def blink_on(self):
        item = ('blink_on', {})
        self._queue.put(item)

    def blink_off(self):
        item = ('blink_off', {})
        self._queue.put(item)

    def clear(self):
        item = ('clear', {})
        self._queue.put(item)

    def close(self):
        self._queue.join()

