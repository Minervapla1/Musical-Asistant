# recording_list.py
# Alexander Wood-Thomas, Jon Tsai
# adw75, jt765
# ECE5725 Final Project, 5/13/18
#   -Displays recordings stored on device. Can play the recordings,
#    and can also make new recordings
#from __future__ import division
import pygame # Import pygame graphics library
import RPi.GPIO as GPIO
import os
from pygame.locals import *
import numpy as np
from recorder import record_init
from gui_functions import *
import subprocess
import wave
import pyaudio
import time
import math



page = 0 # page of recordings to display
rec_list = [] # array for files
rec_buttons = [] # array for files' display buttons
last_page = 0 # last page of files


# display initial screen
def rec_list_init(screen):
    screen.fill(white)
    global page
    global rec_list
    global rec_buttons
    global last_page

    # Render and display all visual elements
    new_button = show_botton(screen, "Record", (45,210), (70, 50), white, button_font)

    prev_button = show_botton(screen, "Prev Page", (125,210), (75, 50), white, button_font)

    next_button = show_botton(screen, "Next Page", (208,210), (75, 50), white, button_font)

    back_button = show_botton(screen, "Back", (280,210), (50, 50), white, button_font)

    text_surface = button_font.render("Recordings", True, black)
    rec_button = text_surface.get_rect(center=(60,30))
    screen.blit(text_surface, rec_button)

    rec_list = os.listdir("/home/pi/final_project/recordings")
    rec_buttons = show_recordings(screen,page)
    last_page = int(math.ceil(len(rec_list) // 3.0) - 1)

    pygame.display.flip()       # display workspace on screen

    # Check for button presses
    while True:
        for action in pygame.event.get():
            if (action.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                if click_in_button(back_button, pos):
                    # Return to main menu
                    print ("Back")
                    return False
                if click_in_button(new_button, pos):
                    # Go to recording screen
                    print ("Make new recording")
                    return True
                if click_in_button(prev_button, pos):
                    # Go to previous page of recordings
                    print("Prev Page")
                    page = max(0,page - 1)
                    rec_buttons = show_recordings(screen,page)
                if click_in_button(next_button, pos):
                    # Go to next page of recordings
                    print ("Next page")
                    page = min(last_page,page + 1)#si no hay mas paginas no pasa
                    rec_buttons = show_recordings(screen,page)
                for i in range(len(rec_buttons)):
                    if rec_buttons[i] and click_in_button(rec_buttons[i], pos):
                        filename = '/home/pi/final_project/recordings/'+str(rec_list[page*3+i])
                        play_file(screen,filename, page)
                        print (filename)
# display the recordings onto the screen
def show_recordings(screen,page):
    pygame.draw.rect(screen,white,pygame.Rect(0,40,320,130))

    global rec_list
    rec_list = os.listdir("/home/pi/final_project/recordings")
    num_rec = len(rec_list)

    x_pos = 20
    y_pos = 60
    recording_buttons = []

    for i in range(page*3, page*3+3):
        if i < num_rec:
            text_surface = button_font.render(rec_list[i], True, black)
            txt_button = text_surface.get_rect(topleft=(x_pos,y_pos+40*(i%3)))
            txt_button.height = 40
            screen.blit(text_surface, txt_button)
            recording_buttons.append(txt_button)
        else:
            recording_buttons.append(False)

    global last_page
    last_page = int(math.ceil(len(rec_list) // 3.0) - 1)

    pygame.display.flip()
    return recording_buttons

# play the selected file
def play_file(screen, filename, page):
    # open the file for reading
    wf = wave.open(filename, 'rb')
    chunk = min(wf.getnframes() // 10,8192)

    # create an audio object
    p = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    stream = p.open(format =
		    p.get_format_from_width(wf.getsampwidth()),
		    channels = wf.getnchannels(),
		    rate = wf.getframerate(),
                    frames_per_buffer = chunk,
		    output = True)

    # read data (based on the chunk size)
    data = wf.readframes(chunk)

    # display the play control buttons
    stop_button = show_botton(screen, "Stop", (280,90), (50, 50), white, button_font)
    pause_button = show_botton(screen, "Pause", (280,150), (50,50), white, button_font)
    delete_button = show_botton(screen, "Delete", (280, 30), (50,50), white, button_font)

    # play stream (looping from beginning of file to the end)
    playing = True
    delete = False
    while data != '' and playing:
	# writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)

        # check for the playing buttons being pressed
        for action in pygame.event.get():
            if (action.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                if click_in_button(stop_button, pos):
                    # Return to main menu
                    playing = False
                if click_in_button(delete_button, pos):
                    playing = False
                    delete = True
                if click_in_button(pause_button, pos):
                    paused = True
                    time.sleep(0.5)
                    pause_button =show_botton(screen, "Play", (280,150), (50,50), white, button_font)
                    while paused:
                        time.sleep(0.1)
                        for act in pygame.event.get():
                            if (act.type is MOUSEBUTTONUP):
                                position = pygame.mouse.get_pos()
                                if click_in_button(pause_button, position):
                                    paused = False
                                    pause_button =show_botton(screen, "Pause", (280,150), (50,50), white, button_font)
                                if click_in_button(stop_button,position):
                                    paused = False
                                    playing = False
                                if click_in_button(delete_button,position):
                                    paused = False
                                    playing = False
                                    delete = True

    # cleanup stuff.
    stream.close()
    p.terminate()
    pygame.draw.rect(screen, white, pygame.Rect(245,0,80,177))

    global rec_buttons

    if delete:
        cmd = 'rm "' + filename + '"'
        print(cmd)
        subprocess.call(cmd,shell=True)
        rec_buttons = show_recordings(screen,page)

    pygame.display.flip()
    
    