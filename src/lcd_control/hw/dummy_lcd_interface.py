import logging
from typing import List, Tuple, Optional

from lcd_control.hw.lcd_interface import LcdInterface

log = logging.getLogger(__name__)


class DummyInterface(LcdInterface):
    def display_screen(self, text_lines: List[str], location: Tuple[int, int], should_clear: bool):
        log.debug(f"display_screen({text_lines}, {location}, {should_clear}")

    def display_text(self, text: str, location: Optional[Tuple[int, int]] = None, should_clear_row_first=True):
        log.debug(f"display_text({text}, {location}, {should_clear_row_first}")

    def load_bitmap(self, bitmap: List[int], index: int):
        pass

    def display_bitmap(self, index: int, location: Tuple[int, int] = None):
        pass

    def display_scrolling_text(self, text_lines: List[str], direction: str, number_of_positions: int, delay: int):
        pass

    def scroll_left(self, number_of_positions: int):
        pass

    def scroll_right(self, number_of_positions: int):
        pass

    def home(self):
        pass

    def clear(self):
        pass

    def backlight_on(self):
        pass

    def backlight_off(self):
        pass

    def cursor_on(self):
        pass

    def cursor_off(self):
        pass

    def blink_on(self):
        pass

    def blink_off(self):
        pass

    def get_input(self, input_string):
        pass
