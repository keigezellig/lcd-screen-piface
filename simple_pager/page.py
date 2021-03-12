import logging
import threading
from queue import Queue
from time import sleep
from typing import List, Tuple

import pifacecad
from blinker import signal

from simple_pager.lcd_worker import LCDWorker

logger = logging.getLogger(__name__)


class Page:
    def __init__(self):
        self._lines = []

    @property
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, value):
        self._lines = value


class PageController:
    def __init__(self, lcd_controller):
        self._pages = []
        self._active_page_id = None
        self._lcd_controller = lcd_controller

    def add_page(self, lines):
        page = Page()
        page.lines = lines
        self._pages.append(page)

    def set_active_page(self, id):
        self._active_page_id = id
        self._display_page(page_id=self._active_page_id, should_clear=True)

    def _display_page(self, page_id, should_clear):
        self._lcd_controller.display_text(textlines=self._pages[page_id].lines, location=None,
                                          should_clear=should_clear)

    def goto_next_page(self):
        self.set_active_page(id=(self._active_page_id + 1) % len(self._pages))

    def goto_previous_page(self):
        if self._active_page_id >= 1:
            self.set_active_page(id=self._active_page_id - 1)
        else:
            self.set_active_page(id=len(self._pages) - 1)

    def update_text(self, page_id, new_lines):
        self._pages[page_id].lines = new_lines
        if self._active_page_id == page_id:
            self._display_page(page_id=self._active_page_id, should_clear=False)
