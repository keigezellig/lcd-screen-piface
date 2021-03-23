import abc
import logging
from typing import List, Tuple, Callable, Optional

log = logging.getLogger(__name__)


class LcdInterface(metaclass=abc.ABCMeta):
    def setup(self):
        log.info("Setting up LCD interface")

    def close(self):
        log.info("Closing LCD interface")

    def setup_key_listener(self, key_handler: Callable[[int], None]):
        log.info("Setting up keys")

    @abc.abstractmethod
    def display_screen(self, text_lines: List[str], location: Tuple[int, int], should_clear: bool):
        pass

    @abc.abstractmethod
    def display_text(self, text: str, location: Optional[Tuple[int, int]] = None, should_clear_row_first = True):
        pass

    @abc.abstractmethod
    def load_bitmap(self, bitmap: List[int], index: int):
        pass

    @abc.abstractmethod
    def display_bitmap(self, index: int, location: Tuple[int,int] = None):
        pass

    @abc.abstractmethod
    def display_scrolling_text(self, text_lines: List[str], direction: str, number_of_positions: int, delay: int):
        pass



    @abc.abstractmethod
    def scroll_left(self, number_of_positions: int):
        pass

    @abc.abstractmethod
    def scroll_right(self, number_of_positions: int):
        pass

    @abc.abstractmethod
    def home(self):
        pass

    @abc.abstractmethod
    def clear(self):
        pass

    @abc.abstractmethod
    def backlight_on(self):
        pass

    @abc.abstractmethod
    def backlight_off(self):
        pass

    @abc.abstractmethod
    def cursor_on(self):
        pass

    @abc.abstractmethod
    def cursor_off(self):
        pass

    @abc.abstractmethod
    def blink_on(self):
        pass

    @abc.abstractmethod
    def blink_off(self):
        pass

    @abc.abstractmethod
    def get_input(self, input_string):
        pass

