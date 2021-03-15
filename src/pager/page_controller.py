import logging
from typing import List, Dict, Optional

from lcd_control.piface_controller import PiFaceController
from pager.page import Page, SimplePage, ActionPage

log = logging.getLogger(__name__)


class PageController:
    def __init__(self, lcd_controller: PiFaceController):
        self._pages: List[Page] = []
        self._lcd_controller: PiFaceController = lcd_controller
        self._current_page_index: int = 0

        self._setup_buttons()

    def add_page(self, content: Dict):
        page: Optional[Page] = None

        if 'line1' in content and 'line2' in content:
            page = SimplePage(self._lcd_controller)
        elif 'caption' in content and 'actions' in content:
            page = ActionPage(self._lcd_controller)
        else:
            raise ValueError("Unknown page type")

        page.set_content(content=content)
        self._pages.append(page)

    def update_page(self, page_index: Optional[int] = None, new_content: dict):
        index = page_index
        if page_index = None:
            index = self._current_page_index
        
        page = self._pages[index]
        page.set_content(new_content)
        if self._current_page_index == page_index:
            self._refresh_current_page()

    def _setup_buttons(self):
        self._lcd_controller.set_button_eventhandler(button=PiFaceController.ROCKER_LEFT,
                                                     handler=self._handle_browse_button)
        self._lcd_controller.set_button_eventhandler(button=PiFaceController.ROCKER_RIGHT,
                                                     handler=self._handle_browse_button)
        self._lcd_controller.set_button_eventhandler(button=PiFaceController.ROCKER_PRESS,
                                                     handler=self._handle_browse_button)
        self._lcd_controller.set_button_eventhandler(button=PiFaceController.BUTTON_0,
                                                     handler=self._handle_action_button)
        self._lcd_controller.set_button_eventhandler(button=PiFaceController.BUTTON_1,
                                                     handler=self._handle_action_button)
        self._lcd_controller.set_button_eventhandler(button=PiFaceController.BUTTON_2,
                                                     handler=self._handle_action_button)
        self._lcd_controller.set_button_eventhandler(button=PiFaceController.BUTTON_3,
                                                     handler=self._handle_action_button)
        self._lcd_controller.set_button_eventhandler(button=PiFaceController.BUTTON_4,
                                                     handler=self._handle_action_button)

    def _handle_browse_button(self, sender, **kwargs):
        button = kwargs['button']
        if button == PiFaceController.ROCKER_LEFT:
            self._previous_page()
        elif button == PiFaceController.ROCKER_RIGHT:
            self._next_page()
        elif button == PiFaceController.ROCKER_PRESS:
            self._home_page()

    def _handle_action_button(self, sender, **kwargs):
        current_page = self._pages[self._current_page_index]
        if isinstance(current_page, ActionPage):
            button = kwargs['button']
            current_page.execute_action(button)

    def _previous_page(self):
        if self._current_page_index > 0:
            self._current_page_index -= 1
        else:
            self._current_page_index = len(self._pages) - 1

        self._display_current_page()

    def _next_page(self):
        self._current_page_index = (self._current_page_index + 1) % len(self._pages)
        self._display_current_page()

    def _home_page(self):
        self._current_page_index = 0
        self._display_current_page()

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
