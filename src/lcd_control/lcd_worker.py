import logging
from queue import Queue
from time import sleep
from typing import Any, Dict, Tuple

from blinker import signal
from lcd_control.hw.lcd_interface import LcdInterface

log = logging.getLogger(__name__)


class LCDWorker:
    def __init__(self, lcd: LcdInterface, qsize: int = 1, delay_between_processing_messages=0, ):
        self._queue: Queue = Queue(maxsize=qsize)
        self._lcd = lcd
        self._delay_between_processing_messages = delay_between_processing_messages
        self._return_value_available = signal('return_value_available')


    def setup(self):
        self._lcd.setup()
        self._lcd.backlight_on()
        self._lcd.cursor_off()
        self._lcd.blink_off()

    def get_lcd(self) -> LcdInterface:
        return self._lcd

    def schedule_command(self, message: Tuple[str, Dict[str, Any]]):
        self._queue.put(message)

    def start(self):
        log.debug("Starting lcd command processing thread")
        while True:
            # Get command and parameters from queue
            command: str
            parameters: Dict[str, Any]

            command, parameters = self._queue.get()
            try:
                # Get correct method out of command
                lcd_method = getattr(self._lcd.__class__, command)
                # Execute command
                if command == 'display_text':
                    lcd_method(self._lcd, parameters['text'], parameters['location'], parameters['should_clear_row_first'])
                if command == 'display_screen':
                    lcd_method(self._lcd, parameters['text_lines'], parameters['should_clear'], parameters['location'])
                elif command == 'scroll_left':
                    lcd_method(self._lcd, parameters['number_of_positions'])
                elif command == 'scroll_right':
                    lcd_method(self._lcd, parameters['number_of_positions'])
                elif command == 'display_scrolling_text':
                    lcd_method(self._lcd, parameters['text_lines'], parameters['direction'],
                                                     parameters['number_of_positions'], parameters['delay'])
                elif command == 'home':
                    lcd_method(self._lcd)
                elif command == 'clear':
                    lcd_method(self._lcd)
                elif command == 'backlight_on':
                    lcd_method(self._lcd)
                elif command == 'backlight_off':
                    lcd_method(self._lcd)
                elif command == 'cursor_on':
                    lcd_method(self._lcd)
                elif command == 'cursor_off':
                    lcd_method(self._lcd)
                elif command == 'blink_on':
                    lcd_method(self._lcd)
                elif command == 'blink_off':
                    lcd_method(self._lcd)
                elif command == 'load_bitmap':
                    lcd_method(self._lcd, parameters['bitmap_data'], parameters['index'])
                elif command == 'display_bitmap':
                    lcd_method(self._lcd, parameters['index'], parameters['location'])
                elif command == 'get_input':
                    result = lcd_method(self._lcd, parameters['input_string'])
                    on_result_received_handler = parameters['on_result_received']
                    self._return_value_available.connect(receiver=on_result_received_handler)
                    self._return_value_available.send(sender=command, result=result)
                    self._return_value_available.disconnect(receiver=on_result_received_handler)
                else:
                    log.warning(f"Command {command} not implemented")
            except Exception as e:
                log.error(f"Error: {e}", exc_info=True)
            finally:
                if self._delay_between_processing_messages > 0:
                    sleep(self._delay_between_processing_messages)
                self._queue.task_done()

            log.debug(f"Q-size: {self._queue.qsize()}")

    def stop(self):
        log.info("Stopping lcd command processing thread")
        self._queue.join()
        self._lcd.close()
