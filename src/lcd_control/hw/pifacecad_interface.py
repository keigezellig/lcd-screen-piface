import logging
from time import sleep
from typing import List, Tuple, Callable, Optional

import pifacecad
from pifacecad import PiFaceCAD, SwitchEventListener, LCDBitmap

from lcd_control.hw.lcd_interface import LcdInterface

log = logging.getLogger(__name__)


class PiFaceCadInterface(LcdInterface):
    def __init__(self):
        super().__init__()
        self._maxRows = 2
        self._maxColumns = 16
        self._pi_face: Optional[PiFaceCAD] = None
        self._key_handler: Optional[Callable[[int], None]] = None
        self._key_listener: Optional[SwitchEventListener] = None

    def setup(self):
        super().setup()
        self._pi_face = pifacecad.PiFaceCAD()

    def close(self):
        if self._key_listener:
            log.info("Stopping key listener")
            self._key_listener.deactivate()


    def setup_key_listener(self, key_handler: Callable[[int], None]):
        super().setup_key_listener(key_handler=key_handler)

        self._key_handler = key_handler
        self._key_listener = pifacecad.SwitchEventListener(chip=self._pi_face)

        for i in range(8):
            self._key_listener.register(i, pifacecad.IODIR_ON, callback=self._handle_button_press)

        self._key_listener.activate()

    def _handle_button_press(self, event):
        log.debug(f"Button {event.pin_num} pressed")
        self._key_handler(event.pin_num)

    def display_text(self, text_lines: List[str], location: Optional[Tuple[int, int]], should_clear: bool):
        log.debug(f"display_text({text_lines}, {location}, {should_clear}")

        if len(text_lines[0]) < self._maxColumns:
            text_lines[0] = '{:16}'.format(text_lines[0])

        if len(text_lines) == self._maxRows and len(text_lines[1]) < self._maxColumns:
            text_lines[1] = '{:16}'.format(text_lines[1])

        if should_clear:
            self._pi_face.lcd.clear()

        if location is not None and len(text_lines) == 1:
            self._pi_face.lcd.set_cursor(location[1], location[0])
            self._pi_face.lcd.write(text_lines[0])
        else:
            for i, item in enumerate(text_lines):
                self._pi_face.lcd.set_cursor(0, i)
                self._pi_face.lcd.write(item)

    def load_bitmap(self, bitmap_data: List[int], index: int):
        if len(bitmap_data) != 8:
            raise ValueError('Bitmaps should be 5x8')
        if index < 0 or index > 7:
            raise ValueError("Index should be between 0 and 7 ")

        bitmap: LCDBitmap = LCDBitmap(bitmap_data)
        self._pi_face.lcd.store_custom_bitmap(char_bank=index, bitmap=bitmap)

    def display_bitmap(self, index: int, location: Tuple[int, int] = None):
        if index < 0 or index > 7:
            raise ValueError("Bitmap index should be between 0 and 7 ")

        if location is not None:
            row, col = location
            self._pi_face.lcd.set_cursor(col, row)

        self._pi_face.lcd.write_custom_bitmap(index)








    def display_scrolling_text(self, text_lines: List[str], direction: str, number_of_positions: int, delay: int):
        log.debug(f"_display_scrolling_text({text_lines}, {direction}, {number_of_positions},{delay}")
        self.display_text(text_lines=text_lines, location=None, should_clear=True)
        if direction != "both":
            for j in range(number_of_positions):
                if direction == "left":
                    self._pi_face.lcd.move_right()
                    sleep(delay)
                elif direction == "right":
                    self._pi_face.lcd.move_left()
                    sleep(delay)
        else:
            for k in range(number_of_positions):
                self._pi_face.lcd.move_left()
                sleep(delay)

            for l in range(number_of_positions * 2):
                self._pi_face.lcd.move_right()
                sleep(delay)

            self._pi_face.lcd.home()

    def scroll_left(self, number_of_positions: int):
        log.debug(f"scroll_left({number_of_positions}")
        for j in range(number_of_positions):
            self._pi_face.lcd.move_right()

    def scroll_right(self, number_of_positions: int):
        log.debug(f"scroll_left({number_of_positions}")
        for j in range(number_of_positions):
            self._pi_face.lcd.move_left()

    def home(self):
        self._pi_face.lcd.home()

    def clear(self):
        self._pi_face.lcd.clear()

    def backlight_on(self):
        self._pi_face.lcd.backlight_on()

    def backlight_off(self):
        self._pi_face.lcd.backlight_off()

    def cursor_on(self):
        self._pi_face.lcd.cursor_on()

    def cursor_off(self):
        self._pi_face.lcd.cursor_off()

    def blink_on(self):
        self._pi_face.lcd.blink_on()

    def blink_off(self):
        self._pi_face.lcd.blink_off()
