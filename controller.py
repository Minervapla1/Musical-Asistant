#from __future__ import division
import pygame # Import pygame graphics library
import os # for OS calls
from pygame.mixer import Sound, get_init, pre_init
os.putenv('SDL_VIDEODRIVER','fbcon') # Display on piTFT
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
pygame.init()
pre_init(44100, -16, 1, 1024)

import RPi.GPIO as GPIO
from pygame.locals import *
import numpy as np
from main_menu import main_init
from metronome import metro_init
from tuner import tuner_init
from recording_list import rec_list_init
from recorder import record_init




GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# quit button
def GPIO27_callback(channel):
    GPIO.cleanup()
    exit()

# check button clicks
def click_in_button(button, click):
    x,y = click
    if x < button.right and x > button.left and y > button.top and y < button.bottom:
        return True
    return False

# add quit button
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback)

# initialize and define constants
pygame.init()
pygame.mouse.set_visible(True)
size = width, height = 320, 240
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0

screen = pygame.display.set_mode(size)

# menu navigation
while True:
    # Display main menu
    navi = main_init(screen)

    if (navi == 0):
        # Exit out of the program
        GPIO.cleanup()
        exit()
    elif (navi == 1):
        # Open metronome
        metro_init(screen)
    elif (navi == 2):
        # Open tuner
        
        tuner_init(screen)
        
    else:
        # Open recordings list
        new_rec = rec_list_init(screen)

        # Check if making new recording
        while (new_rec):
            # Open recorder
            record_init(screen)

            # Go back to recordings list
            new_rec = rec_list_init(screen)

GPIO.cleanup()
