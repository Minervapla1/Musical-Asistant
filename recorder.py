# recorder.py
# Alexander Wood-Thomas, Jon Tsai
# adw75, jt765
# ECE5725 Final Project, 5/13/18
#   -Recorder tool for RPi Music Assistant. Can record the sounds received
#    by the micrphone and save as a file

import pygame # Import pygame graphics library
import os # for OS calls
from pygame.locals import *
import numpy as np
from gui_functions import *
import pyaudio
import wave
import datetime
import time

# display the recorder screen
def record_init(screen):
    screen.fill(white)

    # Render and display all visual elements
    start_button = show_botton(screen, "Start", (160,120), (60,60), white, button_font)
    back_button = show_botton(screen, "Back", (280,210), (50,50), white, button_font)


    text_surface = button_font.render("Rec", True, black)
    rec_button = text_surface.get_rect(center=(270,30))
    screen.blit(text_surface, rec_button)

    text_surface = button_font.render("00:00:00", True, black)
    time_button = text_surface.get_rect(center=(40,30))
    screen.blit(text_surface, time_button)

    pygame.display.flip()       # display workspace on screen

    # Check for button presses
    while True:
        for action in pygame.event.get():
            if (action.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                if click_in_button(back_button, pos):
                    # Return to recordings list
                    print ("Back")
                    return True
                if click_in_button(start_button, pos):
                    # Start the recording
                    print ("Start")
                    start_recording(screen)


    #GPIO.cleanup()

# begin recording audio and save to file
def start_recording(screen):
    # change the display
    stop_button = show_botton(screen, "Stop", (160,120), (60,60), white, button_font)
    text_surface = button_font.render("Rec", True, black)
    rec_button = text_surface.get_rect(center=(270,30))
    screen.blit(text_surface, rec_button)
    pygame.display.flip()

    audio = pyaudio.PyAudio()
    RATE = 8000
    CHUNK = 1024

    stream = audio.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,frames_per_buffer=CHUNK)
    frames = []

    recording = True
    start = time.time()

    # record audio
    while True and recording:
        data = stream.read(CHUNK)
        frames.append(data)

        current = time.time()

        # update visual elements
        if (current - start) % 1 < 0.5:
            pygame.draw.circle(screen,red, (300, 30), 6)
            pygame.draw.rect(screen,white,(20,10,80,30))
            rec_time = rec_duration(int(current - start))
            text_surface = button_font.render(rec_time, True, black)
            time_button = text_surface.get_rect(center=(40,30))
            screen.blit(text_surface, time_button)
        else:
            pygame.draw.circle(screen,white, (300, 30), 6)

        pygame.display.flip()

        # check for stop button press
        for action in pygame.event.get():
            if (action.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                if click_in_button(stop_button, pos):
                    recording = False

    print("Finished Recording.")

    # stop and write to file
    stream.stop_stream()
    stream.close()
    audio.terminate()

    now = datetime.datetime.now()
    filename = now.strftime("/home/pi/final_project/recordings/%Y-%m-%d %H-%M-%S.wav")

    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(1)
    waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # reset screen
    start_button = show_botton(screen, "Start", (160,120), (60,60), white, button_font)
    pygame.draw.circle(screen,white, (300, 30), 6)
    pygame.draw.rect(screen,white,(20,10,80,30))
    text_surface = button_font.render("00:00:00", True, black)
    time_button = text_surface.get_rect(center=(40,30))
    screen.blit(text_surface, time_button)
    pygame.display.flip()

# determine the hours, minutes, and seconds of the given length of time
def rec_duration(time_len):
    hrs = time_len / 3600
    mins = (time_len % 3600) / 60
    sec = time_len % 60

    duration = '%02.0f:%02.0f:%02.0f' % (hrs, mins, sec)
    return duration


