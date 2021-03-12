import logging
import sys
import threading
from queue import Queue
from time import sleep
from typing import Any, Dict, List, Tuple

import pifacecad

# SUPPORTED_COMMANDS = ['display_text', 'scroll_left', 'scroll_right', 'home', 'display_scrolling_text', 'clear']
from pifacecad import PiFaceCAD

from simple_pager.hw.lcd_interface import LcdInterface

log = logging.getLogger(__name__)


class LCDWorker:
    def __init__(self, lcd: LcdInterface, qsize: int = 1, delay_between_processing_messages=0.25):
        self._queue: Queue = Queue(maxsize=qsize)
        self._lcd = lcd
        self._delay_between_processing_messages = delay_between_processing_messages

    def setup(self):
        self._lcd.setup()
        self._lcd.backlight_on()
        self._lcd.cursor_off()
        self._lcd.blink_off()

    def get_lcd(self) -> LcdInterface:
        return self._lcd

    def schedule_command(self, message: Tuple[str, Dict[str, Any]]):
        self._queue.put(message)

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
                # Get correct method out of command

                # Execute command
                if command == 'display_text':
                    self._lcd.display_text(parameters['text_lines'], parameters['location'], parameters['should_clear'])
                elif command == 'scroll_left':
                    self._lcd.scroll_left(parameters['number_of_positions'])
                elif command == 'scroll_right':
                    self._lcd.scroll_right(parameters['number_of_positions'])
                elif command == 'display_scrolling_text':
                    self._lcd.display_scrolling_text(parameters['text_lines'], parameters['direction'],
                                                     parameters['number_of_positions'], parameters['delay'])
                elif command == 'home':
                    self._lcd.home()
                elif command == 'clear':
                    self._lcd.clear()
                elif command == 'backlight_on':
                    self._lcd.backlight_on()
                elif command == 'backlight_off':
                    self._lcd.backlight_off()
                elif command == 'cursor_on':
                    self._lcd.cursor_on()
                elif command == 'cursor_off':
                    self._lcd.cursor_off()
                elif command == 'blink_on':
                    self._lcd.blink_on()
                elif command == 'blink_off':
                    self._lcd.blink_off()
                else:
                    log.warning(f"Command {command} not implemented")
            except Exception as e:
                log.error(f"Unexpected error: {e}", exc_info=True)
            finally:
                sleep(self._delay_between_processing_messages)
                self._queue.task_done()

            log.debug(f"Q-size: {self._queue.qsize()}")

    def close(self):
        self._queue.join()
        self._lcd.close()
