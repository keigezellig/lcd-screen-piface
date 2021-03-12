import logging
import sys
import threading
from queue import Queue
from time import sleep
from typing import Any, Dict, List, Tuple

import pifacecad

# SUPPORTED_COMMANDS = ['display_text', 'scroll_left', 'scroll_right', 'home', 'display_scrolling_text', 'clear']
from pifacecad import PiFaceCAD

log = logging.getLogger(__name__)


class LCDWorker:

    def __init__(self, queue: Queue):
        self._queue: Queue = queue
        self._piface: PiFaceCAD = None

    def init(self):
        self._piface = pifacecad.PiFaceCAD()
        self._backlight_on()
        self._cursor_off()
        self._blink_off()

    def init_key_listener(self, key_handler):
        listener = pifacecad.SwitchEventListener(chip=self._piface)
        for i in range(8):
            listener.register(i, pifacecad.IODIR_ON, key_handler)

        listener.activate()

    def process_lcd_commands(self):
        while True:
            # Get command and parameters from queue
            command: str = ""
            parameters: Dict[str, Any] = {}
            command, parameters = self._queue.get()
            # if command not in SUPPORTED_COMMANDS:
            #     log.warning(f"Command {command} not supported.")
            #     self._queue.task_done()

            try:
                # Execute command
                if command == 'display_text':
                    self._display_text(parameters['text_lines'], parameters['location'], parameters['should_clear'])
                elif command == 'scroll_left':
                    self._scroll_left(parameters['number_of_positions'])
                elif command == 'scroll_right':
                    self._scroll_right(parameters['number_of_positions'])
                elif command == 'display_scrolling_text':
                    self._display_scrolling_text(parameters['text_lines'], parameters['direction'],
                                                 parameters['number_of_positions'], parameters['delay'])
                elif command == 'home':
                    self._home()
                elif command == 'clear':
                    self._clear()
                elif command == 'backlight_on':
                    self._backlight_on()
                elif command == 'backlight_off':
                    self._backlight_off()
                elif command == 'cursor_on':
                    self._cursor_on()
                elif command == 'cursor_off':
                    self._cursor_off()
                elif command == 'blink_on':
                    self._blink_on()
                elif command == 'blink_off':
                    self._blink_off()

                else:
                    log.warning(f"Command {command} not implemented")
            except Exception as e:
                log.error(f"Unexpected error: {e}", exc_info=True)
            finally:
                sleep(0.25)
                self._queue.task_done()

            log.debug(f"Q-size: {self._queue.qsize()}")

    def _display_text(self, text_lines: List[str], location: Tuple[int, int], should_clear: bool):
        log.debug(f"display_text({text_lines}, {location}, {should_clear}")

        if len(text_lines[0]) < 16:
            text_lines[0] = '{:16}'.format(text_lines[0])

        if len(text_lines) == 2 and len(text_lines[1]) < 16:
            text_lines[1] = '{:16}'.format(text_lines[1])

        lcd = self._piface.lcd
        if should_clear:
            lcd.clear()

        if location is not None and len(text_lines) == 1:
            lcd.set_cursor(location[1], location[0])
            lcd.write(text_lines[0])
        else:
            for i, item in enumerate(text_lines):
                lcd.set_cursor(0, i)
                lcd.write(item)

    def _scroll_left(self, number_of_positions: int = 1):
        log.debug(f"scroll_left({number_of_positions}")
        lcd = self._piface.lcd
        for j in range(number_of_positions):
            lcd.move_right()

    def _scroll_right(self, number_of_positions: int = 1):
        log.debug(f"scroll_right({number_of_positions}")
        lcd = self._piface.lcd
        for j in range(number_of_positions):
            lcd.move_left()

    def _home(self):
        lcd = self._piface.lcd
        lcd.home()

    def _display_scrolling_text(self, text_lines: List[str], direction: str, number_of_positions: int, delay: int):
        log.debug(f"_display_scrolling_text({text_lines}, {direction}, {number_of_positions},{delay}")
        lcd = self._piface.lcd

        self._display_text(text_lines=text_lines, location=None, should_clear=True)
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

    def _clear(self):
        log.debug(f"clear()")
        self._piface.lcd.clear()

    def _backlight_on(self):
        log.debug(f"backlight_on()")
        self._piface.lcd.backlight_on()

    def _backlight_off(self):
        log.debug(f"backlight_off()")
        self._piface.lcd.backlight_off()

    def _cursor_on(self):
        log.debug(f"_cursor_on()")
        self._piface.lcd.cursor_on()

    def _cursor_off(self):
        log.debug(f"_cursor_off()")
        self._piface.lcd.cursor_off()

    def _blink_on(self):
        log.debug(f"_blink_on()")
        self._piface.lcd.blink_on()

    def _blink_off(self):
        log.debug(f"_blink_off()")
        self._piface.lcd.blink_off()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    q: Queue = Queue(maxsize=10)
    worker: LCDWorker = LCDWorker(queue=q)

    threading.Thread(target=worker.process_lcd_commands, daemon=True).start()

    try:
        while True:
            item = ('display_text', {'text_lines': ['bla', 'bla'], 'location': (0, 0), 'should_clear': False})
            q.put(item)

    except KeyboardInterrupt:
        q.join()
