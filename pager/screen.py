import logging
from typing import Dict

from lcd_control.piface_controller import PiFaceController

logger = logging.getLogger(__name__)


class Screen:
    def __init__(self, page_definitions, lcd_controller: PiFaceController):
        self._pages = page_definitions
        self._lcd_controller: PiFaceController = lcd_controller
        self._current_page: int = 0
        self._setup_browse_keys()

    def _setup_browse_keys(self):
        self._lcd_controller.set_button_eventhandler(button=PiFaceController.ROCKER_LEFT, handler=self._handle_browse_button)
        self._lcd_controller.set_button_eventhandler(button=PiFaceController.ROCKER_RIGHT, handler=self._handle_browse_button)
        self._lcd_controller.set_button_eventhandler(button=PiFaceController.ROCKER_PRESS, handler=self._handle_browse_button)
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

    def _handle_action_button(self, sender, **kwargs):
        button = kwargs['button']
        page = self._pages[self._current_page]
        if len(page['actions']) > 0 and button < len(page['actions']):
            action = page['actions'][button]
            module_name = action['action'].split('.')[0]
            function = action['action'].split('.')[1]
            module = __import__(module_name)
            func = getattr(module, function)
            func(self, self._lcd_controller)

    def _handle_browse_button(self, sender, **kwargs):
        button = kwargs['button']
        if button == PiFaceController.ROCKER_LEFT:
            self._previous_page()
        elif button == PiFaceController.ROCKER_RIGHT:
            self._next_page()
        elif button == PiFaceController.ROCKER_PRESS:
            self._home_page()

    def _previous_page(self):
        if self._current_page > 0:
            self._current_page -= 1
        else:
            self._current_page = len(self._pages) - 1

        self._display_current_page()

    def _next_page(self):
        self._current_page = (self._current_page + 1) % len(self._pages)
        self._display_current_page()

    def _home_page(self):
        self._current_page = 0
        self._display_current_page()

    def _display_current_page(self):
        logger.debug(f"Display page {self._current_page}")
        page = self._pages[self._current_page]
        self._lcd_controller.clear()
        self._lcd_controller.backlight_on()
        self._lcd_controller.display_text(textlines=[page['text']], location=(0, 0), should_clear=True)

        if len(page['actions']) > 0:
            last_action_index = min(5, len(page['actions']))
            for i in range(0, last_action_index):
                action = page['actions'][i]
                if 'label' in action:
                    label = action['label'][0]
                    self._lcd_controller.display_text(textlines=[label], location=(1, i * 2), should_clear=False)

                if 'bitmap' in action:
                    self._lcd_controller.load_bitmap(action['bitmap'], i)
                    self._lcd_controller.display_bitmap(index=i, location=(1, i * 2))
                    # bitmap = pifacecad.LCDBitmap(action['bitmap'])
                    # self.__lcd.store_custom_bitmap(i, bitmap=bitmap)
                    # self.__lcd.write_custom_bitmap(i)

        self._lcd_controller.cursor_off()

    def display(self, page=None):
        if page is not None:
            if page < 0 or page > len(self._pages) - 1:
                raise IndexError("Invalid page number")
            else:
                self._current_page = page

        self._display_current_page()
