# gui_functions.py
# Alexander Wood-Thomas, Jon Tsai
# adw75, jt765
# Final Project, 5/13/18

# This file defines functions to help with displaying the GUI

import pygame
from pygame.locals import *
import numpy as np
pygame.init()
# constant color definitions for use in GUI objects
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
pygame.font.init()
# two standard fonts
my_font = pygame.font.SysFont("FreeMono, Monospace", 12) # large font for home screen buttons
button_font = pygame.font.Font(None, 21)

# Modular function for displaying a button. It displays a button with a single
# line of text. Arguments include center position, size, font color, and font size.
# Returns a rect object for click detection.
def show_botton(screen, text, loc, size, color, font_size):
    
    text_surface = font_size.render(text, True, black)
    button_text= text_surface.get_rect(center=loc)
    button_area = Rect((0,0), size)
    button_area.center = loc

    border_area = button_area.copy()
    border_size = 4
    border_area.width = border_area.width+border_size
    border_area.height = border_area.height+border_size
    border_area.center = button_area.center

    pygame.draw.rect(screen, black, border_area)
    pygame.draw.rect(screen, color, button_area)

    screen.blit(text_surface, button_text)
    pygame.display.flip()
    return button_area

# Takes a button Rect object and a click coordinate. Returns true if the click
# is on the button.
def click_in_button(button, click):
    x,y = click
    if x < button.right and x > button.left and y > button.top and y < button.bottom:
        return True
    return False