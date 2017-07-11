import threading
from threading import main_thread
from time import sleep

import pifacecad

BUTTON_0 = 0
BUTTON_1 = 1
BUTTON_2 = 2
BUTTON_3 = 3
BUTTON_4 = 4
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
                                 callback=self.__goto_previous_page)
        self.__listener.register(pin_num=ROCKER_RIGHT, direction=pifacecad.IODIR_FALLING_EDGE,
                                 callback=self.__goto_next_page)
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
        page = self.__pages[self.__current_page]
        action = page['actions'][button_no]
        module_name = action['action'].split('.')[0]
        function = action['action'].split('.')[1]
        module = __import__(module_name)
        func = getattr(module, function)
        func(self)



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
        self.__lcd.set_cursor(0, 0)
        self.__lcd.write(page['text'])
        for i in range(0, 5):
            label = page['actions'][i]['label'][0]
            self.__lcd.set_cursor(i*2, 1)
            self.__lcd.write(label)

        self.__lcd.cursor_off()








