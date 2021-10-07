import abc
import logging
from typing import List, Dict, Optional

from blinker import signal

from lcd_control.piface_controller import PiFaceController

log = logging.getLogger(__name__)


class Page(metaclass=abc.ABCMeta):
    def __init__(self, lcd_controller: PiFaceController):
        self._lcd_controller: PiFaceController = lcd_controller

    @abc.abstractmethod
    def display(self, should_clear: bool):
        pass

    @abc.abstractmethod
    def set_content(self, content: Dict):
        pass

    def handle_button(self, sender, button: int):
        pass


class NonModalPage(Page, metaclass=abc.ABCMeta):
    def __init__(self, lcd_controller: PiFaceController):
        super().__init__(lcd_controller=lcd_controller)

    # def handle_button(self, sender, button: int):
    #     if button == PiFaceController.ROCKER_LEFT:
    #         signal(name='previous_page').send()
    #     elif button == PiFaceController.ROCKER_RIGHT:
    #         signal(name='next_page').send()
    #     elif button == PiFaceController.ROCKER_PRESS:
    #         signal(name='home_page').send()


class SimplePage(NonModalPage):
    def __init__(self, lcd_controller: PiFaceController):
        super().__init__(lcd_controller)
        self._content: List = []

    def display(self, should_clear):
        self._lcd_controller.display_screen(textlines=self._content, should_clear=should_clear)

    def set_content(self, content: Dict):
        if 'line1' not in content and 'line2' not in content:
            raise ValueError("Content should contain keys 'line1' or 'line2'")

        if not self._content:
            self._content.append('' if 'line1' not in content else content['line1'])
            self._content.append('' if 'line2' not in content else content['line2'])
        else:
            line1: Optional[str] = None if 'line1' not in content else content['line1']
            line2: Optional[str] = None if 'line2' not in content else content['line2']
            if line1 and line1 != self._content[0]:
                self._content[0] = line1
            if line2 and line2 != self._content[1]:
                self._content[1] = line2


class ActionPage(NonModalPage):
    _MAX_ACTIONS = 3

    def __init__(self, lcd_controller: PiFaceController):
        super().__init__(lcd_controller)
        self._content: Dict = {}

    def display(self, should_clear):
        caption: str = self._content['caption']
        actions: List[Dict] = self._content['actions']

        self._lcd_controller.display_text(text=caption, location=(0, 0))
        # self._lcd_controller.display_screen(textlines=[caption], location=(0, 0), should_clear=should_clear)
        self._lcd_controller.display_text(text='', location=(1,0), should_clear_row_first=True)

        start_idx_position: int = 1
        for idx, action in enumerate(actions):
            location = (1, (idx * 2) + start_idx_position)
            if 'label' in action:
                self._lcd_controller.display_text(text=action['label'], location=location)

            if 'bitmap' in action:
                self._lcd_controller.display_bitmap(index=idx, location=location)

    def handle_button(self, sender, button: int):
        super().handle_button(sender=sender, button=button)
        # Hacky way to use button 1,2,3 instead of 0,1,2,3,4 (since 0 and 4 are now used for switching pages)
        if button > PiFaceController.BUTTON_0 and button < PiFaceController.BUTTON_4:
            self._execute_action(button=button)

    def _execute_action(self, button: int):
        # Hacky way to use button 1,2,3 instead of 0,1,2,3,4 (since 0 and 4 are now used for switching pages)
        actions = self._content['actions']
        if len(actions) > 0 and button < len(actions):
            action = actions[button-1]['action']
            action()

        # 0,1,2

    def set_content(self, content: Dict):
        if ('caption' not in content) or ('actions' not in content):
            raise ValueError('Content of a action page should contain a dictionary with "caption" and "action" keys')

        if len(content['actions']) == 0:
            log.warning("This action page contains no actions")

        if len(content['actions']) > self._MAX_ACTIONS:
            log.warning(f"Only {self._MAX_ACTIONS} actions possible. Other actions will be ignored")

        self._content['caption'] = content['caption']
        self._content['actions'] = content['actions'][:5]
        self._load_bitmaps(self._content['actions'])

    def _load_bitmaps(self, actions):
        bitmaps: List[List[int]] = [action['bitmap'] for action in actions if 'bitmap' in action]

        for idx, bitmap in enumerate(bitmaps):
            self._lcd_controller.load_bitmap(bitmap, idx)
