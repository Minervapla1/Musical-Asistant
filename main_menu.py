# main_menu.py
# Alexander Wood-Thomas, Jon Tsai
# adw75, jt765
# ECE5725 Final Project, 5/13/18
#   -contains all functionality for the main menu of the RPi Music Assistant

import pygame # Import pygame graphics library
import os # for OS calls
import RPi.GPIO as GPIO
from pygame.locals import *
import numpy as np
from gui_functions import *

title_font = pygame.font.Font(None,36)

# displays the main menu
# returns an integer depending on which menu to transition to
def main_init(screen):
    screen.fill(white)

    metro_button = show_botton(screen, "Metronome", (60,120), (80,80), white, button_font)
    tuner_button = show_botton(screen, "Tuner", (160, 120), (80,80), white, button_font)
    rec_button = show_botton(screen, "Recorder", (260,120), (80,80), white, button_font)
    quit_button = show_botton(screen, "Quit", (280,210), (50,50), red, button_font)

    text_surface = title_font.render("RPi Music Assistant", True, black)
    title_button = text_surface.get_rect(center=(160,30))
    screen.blit(text_surface,title_button)

    pygame.display.flip()       # display workspace on screen

    # Check for button presses
    while True:
        for action in pygame.event.get():
            if (action.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                if click_in_button(quit_button, pos):
                    # Quit the program
                    print ("Button pressed. Exiting the program")
                    #GPIO.cleanup()
                    return 0
                if click_in_button(metro_button, pos):
                    # Load the metronome
                    #metro_init(screen)
                    print ("Metronome")
                    return 1
                if click_in_button(tuner_button, pos):
                    # Load the tuner
                    #tuner_init(screen)
                    print ("Tuner")
                    return 2
                if click_in_button(rec_button, pos):
                    # Load the recorder
                    #rec_list_init(screen)
                    print ("Recorder")
                    return 3
#                 if click_in_button(back2_button, pos):              
#                     print ("back to tuner")
#                     return 2#devuelve tuner(init)
