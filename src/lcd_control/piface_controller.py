import logging
import threading
from typing import List, Tuple, Optional

from blinker import signal

from lcd_control.hw.lcd_interface import LcdInterface
from lcd_control.lcd_worker import LCDWorker

log = logging.getLogger(__name__)


class PiFaceController:
    BUTTON_0 = 0
    BUTTON_1 = 1
    BUTTON_2 = 2
    BUTTON_3 = 3
    BUTTON_4 = 4
    ROCKER_PRESS = 5
    ROCKER_LEFT = 6
    ROCKER_RIGHT = 7

    def __init__(self, lcd_interface: LcdInterface):
        self._worker = LCDWorker(lcd=lcd_interface)
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

    def start(self):
        log.info("Starting PifaceController")
        self._worker.get_lcd().setup_key_listener(self._handle_button)
        self._worker.setup()
        threading.Thread(target=self._worker.start, daemon=True).start()

    def _handle_button(self, button: int):
        if button == self.BUTTON_0:
            self.__button0_pressed.send(self, button=button)
        elif button == self.BUTTON_1:
            self.__button1_pressed.send(self, button=button)
        elif button == self.BUTTON_2:
            self.__button2_pressed.send(self, button=button)
        elif button == self.BUTTON_3:
            self.__button3_pressed.send(self, button=button)
        elif button == self.BUTTON_4:
            self.__button4_pressed.send(self, button=button)
        elif button == self.ROCKER_PRESS:
            self.__rocker_pressed.send(self, button=button)
        elif button == self.ROCKER_LEFT:
            self.__rocker_left_pressed.send(self, button=button)
        elif button == self.ROCKER_RIGHT:
            self.__rocker_right_pressed.send(self, button=button)

    def unset_button_eventhandler(self, button, handler):
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

        signal(name=signal_name).disconnect(handler)

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

    def display_text(self, textlines: List[str], location: Optional[Tuple[int, int]], should_clear: bool):
        item = ('display_text', {'text_lines': textlines, 'location': location, 'should_clear': should_clear})
        self._worker.schedule_command(item)

    def load_bitmap(self, bitmap_data: List[int], index: int):
        log.debug(bitmap_data)
        item = ('load_bitmap', {'bitmap_data': bitmap_data, 'index':index})
        self._worker.schedule_command(item)

    def display_bitmap(self, index: int, location: Tuple[int, int] = None):
        item = ('display_bitmap', {'index': index, 'location': location})
        self._worker.schedule_command(item)

    def scroll_right(self, number_of_positions=1):
        item = ('scroll_right', {'number_of_positions': number_of_positions})
        self._worker.schedule_command(item)

    def scroll_left(self, number_of_positions=1):
        item = ('scroll_left', {'number_of_positions': number_of_positions})
        self._worker.schedule_command(item)

    def home(self):
        item = ('home', {})
        self._worker.schedule_command(item)

    def display_scrolling_text(self, textlines, direction, number_of_positions, delay):
        item = ('display_scrolling_text',
                {'text_lines': textlines, 'direction': direction, 'number_of_positions': number_of_positions,
                 'delay': delay})
        self._worker.schedule_command(item)

    def backlight_on(self):
        item = ('backlight_on', {})
        self._worker.schedule_command(item)

    def backlight_off(self):
        item = ('backlight_off', {})
        self._worker.schedule_command(item)

    def cursor_on(self):
        item = ('cursor_on', {})
        self._worker.schedule_command(item)

    def cursor_off(self):
        item = ('cursor_off', {})
        self._worker.schedule_command(item)

    def blink_on(self):
        item = ('blink_on', {})
        self._worker.schedule_command(item)

    def blink_off(self):
        item = ('blink_off', {})
        self._worker.schedule_command(item)

    def clear(self):
        item = ('clear', {})
        self._worker.schedule_command(item)

    def get_input(self, input_string: str, on_result_received):
        item = ('get_input', {'input_string': input_string, 'on_result_received': on_result_received})
        self._worker.schedule_command(item)

    def close(self):
        log.info("Stopping PifaceController")
        self._worker.stop()
