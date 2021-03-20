import logging
from typing import List, Dict, Optional

from blinker import signal

from lcd_control.piface_controller import PiFaceController
from pager.page import Page, SimplePage, ActionPage, InputPage

log = logging.getLogger(__name__)


class PageController:
    def __init__(self, lcd_controller: PiFaceController):
        self._pages: List[Page] = []
        self._lcd_controller: PiFaceController = lcd_controller
        self._current_page_index: int = 0

        signal('button_pressed').connect(self._handle_button)
        signal('previous_page').connect(self._previous_page)
        signal('next_page').connect(self._next_page)
        signal('home_page').connect(self._home_page)

    def add_page(self, content: Dict):
        page: Optional[Page] = None

        if 'line1' in content and 'line2' in content:
            page = SimplePage(self._lcd_controller)
        elif 'caption' in content and 'actions' in content:
            page = ActionPage(self._lcd_controller)
        elif 'input_string' in content and 'on_input_received_action' in content:
            page = InputPage(self._lcd_controller)
        else:
            raise ValueError("Unknown page type")

        page.set_content(content=content)
        self._pages.append(page)

    def update_page(self, new_content: dict, page_index: Optional[int] = None):
        index = page_index
        if page_index is None:
            index = self._current_page_index
        
        page = self._pages[index]
        page.set_content(new_content)
        if self._current_page_index == page_index:
            self._refresh_current_page()

    def display(self, page_index=None):
        if page_index is not None:
            if page_index < 0 or page_index > len(self._pages) - 1:
                raise IndexError("Invalid page number")
            else:
                self._current_page_index = page_index

        self._display_current_page()

    def _refresh_current_page(self):
        log.debug(f"Refreshing: {self._current_page_index}")
        self._pages[self._current_page_index].display(is_update=True)

    def _display_current_page(self):
        log.debug(f"Displaying page: {self._current_page_index}")
        self._pages[self._current_page_index].display(is_update=False)

    def _handle_button(self, sender, button: int):
        if len(self._pages) > 0:
            current_page: Page = self._pages[self._current_page_index]
            current_page.handle_button(sender, button)

    def _previous_page(self, sender):
        if self._current_page_index > 0:
            self._current_page_index -= 1
        else:
            self._current_page_index = len(self._pages) - 1

        self._display_current_page()

    def _next_page(self, sender):
        self._current_page_index = (self._current_page_index + 1) % len(self._pages)
        self._display_current_page()

    def _home_page(self, sender):
        self._current_page_index = 0
        self._display_current_page()

