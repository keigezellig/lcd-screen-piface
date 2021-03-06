import abc
import logging
from typing import List, Dict

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


class SimplePage(Page):
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


class ActionPage(Page):
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

    def execute_action(self, button: int):
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
