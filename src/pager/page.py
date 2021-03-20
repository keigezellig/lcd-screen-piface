import abc
import logging
from typing import List, Dict

from blinker import signal

from lcd_control.piface_controller import PiFaceController

log = logging.getLogger(__name__)


class Page(metaclass=abc.ABCMeta):
    def __init__(self, lcd_controller: PiFaceController):
        self._lcd_controller: PiFaceController = lcd_controller

    @abc.abstractmethod
    def display(self, is_update=False):
        pass

    @abc.abstractmethod
    def set_content(self, content: Dict):
        pass

    def handle_button(self, sender, button: int):
        pass


class NonModalPage(Page, metaclass=abc.ABCMeta):
    def __init__(self, lcd_controller: PiFaceController):
        super().__init__(lcd_controller=lcd_controller)

    def handle_button(self, sender, button: int):
        if button == PiFaceController.ROCKER_LEFT:
            signal(name='previous_page').send()
        elif button == PiFaceController.ROCKER_RIGHT:
            signal(name='next_page').send()
        elif button == PiFaceController.ROCKER_PRESS:
            signal(name='home_page').send()


class SimplePage(NonModalPage):
    def __init__(self, lcd_controller: PiFaceController):
        super().__init__(lcd_controller)
        self._content: Dict = {}

    def display(self, is_update=False):
        self._lcd_controller.display_text([self._content['line1'], self._content['line2']], location=(0, 0),
                                          should_clear=not is_update)

    def set_content(self, content: Dict):
        if ('line1' not in content) or ('line2' not in content):
            raise ValueError('Content of a simple page should contain a dictionary with "line1" and "line2" keys')

        self._content = content


class ActionPage(NonModalPage):
    _MAX_ACTIONS = 5

    def __init__(self, lcd_controller: PiFaceController):
        super().__init__(lcd_controller)
        self._content: Dict = {}

    def display(self, is_update=False):
        caption: str = self._content['caption']
        actions: List[Dict] = self._content['actions']

        self._lcd_controller.display_text(textlines=[caption], location=(0, 0), should_clear=not is_update)

        for idx, action in enumerate(actions):
            if 'label' in action:
                self._lcd_controller.display_text(textlines=[action['label']], location=(1, idx * 2),
                                                  should_clear=False)
            if 'bitmap' in action:
                self._lcd_controller.display_bitmap(index=idx, location=(1, idx * 2))

    def handle_button(self, sender, button: int):
        super().handle_button(sender=sender, button=button)
        self._execute_action(button=button)

    def _execute_action(self, button: int):
        actions = self._content['actions']
        if len(actions) > 0 and button < len(actions):
            action = actions[button]
            module_name = action['action'].split('.')[0]
            function = action['action'].split('.')[1]
            log.debug(f"Executing action: {module_name}.{function}")
            module = __import__(module_name)
            func = getattr(module, function)
            func(self, self._lcd_controller)

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


class InputPage(Page):

    def __init__(self, lcd_controller: PiFaceController):
        super().__init__(lcd_controller)
        self._content: Dict = {}

    def display(self, is_update=False):
        # self._lcd_controller.get_input(input_string=self._content['input_string'], on_result_received=self._content['on_input_received_action'])
        pass

    def handle_button(self, sender, button: int):
        pass

    """
    'content': {'input_string': "Blabla %f", 'on_input_received_action': <function>'} 
    """

    def set_content(self, content: Dict):
        if ('input_string' not in content) or ('on_input_received_action' not in content):
            raise ValueError(
                'Content of a input page should contain a dictionary with "input_string" and "on_input_received_action" keys')
        self._content = content
