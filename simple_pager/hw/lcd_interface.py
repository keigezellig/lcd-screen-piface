import abc
import logging
from typing import List, Tuple, Callable

log = logging.getLogger(__name__)


class LcdInterface(metaclass=abc.ABCMeta):
    def setup(self):
        pass

    def close(self):
        pass

    def init_key_listener(self, key_handler: Callable[[int], None]):
        pass

    @abc.abstractmethod
    def display_text(self, text_lines: List[str], location: Tuple[int, int], should_clear: bool):
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
