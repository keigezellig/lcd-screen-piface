import threading
from threading import main_thread
from time import sleep

import pifacecad

BUTTON_0 = 0
BUTTON_1 = 1
BUTTON_2 = 2
BUTTON_3 = 3
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


    def display(self, page):

        if page < 0 or page > len(self.__pages) - 1:
            raise IndexError("Invalid page number")

        self.__display_current_page()

    def clean_up(self):
        print("Clean up")
        self.__listener.deactivate()


    def __initialize_buttons(self):

        self.__listener.register(pin_num=ROCKER_LEFT, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__goto_previous_page)
        self.__listener.register(pin_num=ROCKER_RIGHT, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__goto_next_page)
        self.__listener.register(pin_num=BUTTON_0, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__button_0_pressed)
        self.__listener.register(pin_num=BUTTON_1, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__button_1_pressed)
        self.__listener.register(pin_num=BUTTON_2, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__button_2_pressed)
        self.__listener.register(pin_num=BUTTON_3, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__button_3_pressed)

        self.__listener.activate()


    def __button_0_pressed(self, event):
        page = self.__pages[self.__current_page]
        action = page['actions'][0]
        print(action['label'])

    def __button_1_pressed(self, event):
        page = self.__pages[self.__current_page]
        action = page['actions'][1]
        print(action['label'])

    def __button_2_pressed(self, event):
        page = self.__pages[self.__current_page]
        action = page['actions'][2]
        print(action['label'])

    def __button_3_pressed(self, event):
        page = self.__pages[self.__current_page]
        action = page['actions'][3]
        print(action['label'])


    def __goto_previous_page(self, event):
        if self.__current_page > 0:
            self.__current_page -= 1
        else:
            self.__current_page = len(self.__pages) - 1

        self.__display_current_page()

    def __goto_next_page(self, event):
        self.__current_page = (self.__current_page + 1) % len(self.__pages)
        self.__display_current_page()


    def __display_current_page(self):
        print("Display page {page}".format(page=self.__current_page))
        page = self.__pages[self.__current_page]
        self.__lcd.clear()
        self.__lcd.write(page['text'])







