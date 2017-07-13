import threading
from threading import main_thread
from time import sleep

import pifacecad

BUTTON_0 = 0
BUTTON_1 = 1
BUTTON_2 = 2
BUTTON_3 = 3
BUTTON_4 = 4
ROCKER_PRESS = 5
ROCKER_LEFT = 6
ROCKER_RIGHT = 7

end_barrier = threading.Barrier(2)


class PagedScreen():
    __pages = []
    __current_page = 0

    def __init__(self, cad, pages):
        self.__is_listener_active = False
        print("loading screen...")
        self.__pages = pages
        self.__current_page = 0
        self.__lcd = cad.lcd
        self.__listener = pifacecad.SwitchEventListener(chip=cad)

        self.__initialize_buttons()

    def display(self, page=None):

        if page is not None:
            if page < 0 or page > len(self.__pages) - 1:
                raise IndexError("Invalid page number")
            else:
                self.__current_page = page

        self.__display_current_page()

    def clean_up(self):
        print("Clean up")
        self.__listener.deactivate()

    def __initialize_buttons(self):

        self.__listener.register(pin_num=ROCKER_LEFT, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__button_pressed)
        self.__listener.register(pin_num=ROCKER_RIGHT, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__button_pressed)
        self.__listener.register(pin_num=ROCKER_PRESS, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__button_pressed)

        self.__listener.register(pin_num=BUTTON_0, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__button_pressed)
        self.__listener.register(pin_num=BUTTON_1, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__button_pressed)
        self.__listener.register(pin_num=BUTTON_2, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__button_pressed)
        self.__listener.register(pin_num=BUTTON_3, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__button_pressed)
        self.__listener.register(pin_num=BUTTON_4, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__button_pressed)
        self.__listener.activate()

    def __button_pressed(self, event):

        button_no = event.pin_num
        if button_no == ROCKER_LEFT:
            self.__goto_previous_page()
            return
        if button_no == ROCKER_RIGHT:
            self.__goto_next_page()
            return
        if button_no == ROCKER_PRESS:
            self.__goto_page_0()
            return


        page = self.__pages[self.__current_page]
        if len(page['actions']) > 0 and button_no < len(page['actions']):
            action = page['actions'][button_no]
            module_name = action['action'].split('.')[0]
            function = action['action'].split('.')[1]
            module = __import__(module_name)
            func = getattr(module, function)
            func(self)

    def __goto_previous_page(self):
        if self.__current_page > 0:
            self.__current_page -= 1
        else:
            self.__current_page = len(self.__pages) - 1

        self.__display_current_page()

    def __goto_page_0(self):
        self.__current_page = 0
        self.__display_current_page()

    def __goto_next_page(self):
        self.__current_page = (self.__current_page + 1) % len(self.__pages)
        self.__display_current_page()

    def __display_current_page(self):
        print("Display page {page}".format(page=self.__current_page))
        page = self.__pages[self.__current_page]
        self.__lcd.clear()
        self.__lcd.backlight_on()
        self.__lcd.set_cursor(row=0, col=0)
        self.__lcd.write(page['text'])

        if len(page['actions']) > 0:
            last_action_index = min(5, len(page['actions']))
            for i in range(0, last_action_index):
                self.__lcd.set_cursor(row=1, col=i * 2)
                action = page['actions'][i]

                if 'label' in action:
                    label = action['label'][0]
                    self.__lcd.write(label)
                if 'bitmap' in action:
                    bitmap = pifacecad.LCDBitmap(action['bitmap'])
                    self.__lcd.store_custom_bitmap(i, bitmap=bitmap)
                    self.__lcd.write_custom_bitmap(i)

        self.__lcd.cursor_off()
