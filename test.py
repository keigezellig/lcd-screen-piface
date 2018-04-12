import pifacecad, sys, os, subprocess
from time import sleep
import datetime
from threading import Timer


GET_IP_CMD = "hostname --all-ip-addresses"
curr_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def display_text(lcd, textlines, location, should_clear):
  if should_clear:
    lcd.clear()

  if location is not None and len(textlines) == 1:
    lcd.set_cursor(location[1], location[0])
    lcd.write(textlines[0])
  else:
    for i, item in enumerate(textlines):
      lcd.set_cursor(0, i)
      lcd.write(item)

def display_scrolling_text(lcd, textlines, direction, number_of_positions, delay):
  
  for i, item in enumerate(textlines):
    lcd.set_cursor(0, i)
    lcd.write(item)

  if direction != "both":
    for j in range(number_of_positions):
      if direction == "left": 
        lcd.move_right()
        sleep(delay)
      elif direction == "right": 
        lcd.move_left()
        sleep(delay) 
  else:
    for k in range(number_of_positions):
       lcd.move_left()
       sleep(delay)

    for l in range(number_of_positions*2):
       lcd.move_right()
       sleep(delay)

    lcd.home()



def handle_button(event):
    if event.pin_num == 6:
       event.chip.lcd.move_right()
    elif event.pin_num == 7:
      event.chip.lcd.move_left()
    elif event.pin_num == 5:
      event.chip.lcd.home()
      event.chip.lcd.see_cursor()
    elif event.pin_num == 4:
      display_text(lcd=event.chip.lcd, textlines=["Rebooting in 5 secs"], location=None, should_clear=True)
      sleep(5)
      event.chip.lcd.clear()
      event.chip.lcd.backlight_off()
      os.system("sudo reboot")
    else:
      text = get_text(event.pin_num)
      display_text(lcd=event.chip.lcd, textlines=text, location=None, should_clear=True)

def get_text(button):
    if button == 0:
      return ["IP: {ip}".format(ip=get_my_ip()), "S/W: 3.0.323234a"]
    if button == 1:
      return ["Current time", curr_time]
      
    return ["You pressed: "+str(button)]


def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')


def get_my_ip():
    return run_cmd(GET_IP_CMD)[:-1]



def foo():
    
    print(curr_time)
    Timer(10, foo).start()

foo()

cad = pifacecad.PiFaceCAD()
cad.lcd.backlight_on()
cad.lcd.cursor_off()
cad.lcd.blink_off()

listener = pifacecad.SwitchEventListener(chip=cad)
for i in range(8):
    listener.register(i, pifacecad.IODIR_FALLING_EDGE, handle_button)

listener.activate()

display_scrolling_text(lcd=cad.lcd, textlines=["Welcome to Triptracker"], direction="right", number_of_positions=22, delay=.3)

