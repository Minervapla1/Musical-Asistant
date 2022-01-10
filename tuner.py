# tuner.py
# Alexander Wood-Thomas, Jon Tsai
# adw75, jt765
# ECE5725 Final Project, 5/13/18
#   -Tuner tool for RPi Music Assistant. Shows how in tune the note being
#    received on the micrphone is, and can play a note for reference
# frequency detection code is courtesy of Scott Harden's open source project in
# real time audio visualization in Python: https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/

import pygame # Import pygame graphics library
import RPi.GPIO as GPIO
from pygame.locals import *
import numpy as np
import time
from gui_functions import *
import pyaudio
import math
import itertools
from metodosparatunertriadas import *
# import metodosparatunertriadas
from triadas import *
#from itertools import zip
#from itertools import izip
from tone_player import Note
# from main_menu import main_init
# 
# frequency = 440 # initial note frequency
# frequency2= 554.37
# note = "A" # initial note
# note2= "C#"
# note_ind = 39 # initial note index
# note_freqs = [4186.01, 3951.07, 3729.31, 3520, 3322.44,
#                 3135.96, 2959.96, 2793.83, 2637.02, 2489.02,
#                 2349.32, 2217.46, 2093, 1975.53, 1864.66,
#                 1760, 1661.22, 1567.98, 1479.98, 1396.91, 1318.51,
#                 1244.51, 1174.66, 1108.73, 1046.5, 987.77, 932.33,
#                 880, 830.61, 783.99, 739.99, 698.46, 659.26, 622.25,
#                 587.33, 554.37, 523.25, 493.88, 466.16, 440, 415.31,
#                 392, 370, 349.23, 329.63, 311.13, 293.67, 277.18,
#                 261.63, 246.94, 233.08, 220, 207.65, 196, 185,
#                 174.61, 164.81, 155.56, 146.83, 138.59, 130.81,
#                 123.47, 116.54, 110, 103.83, 98, 92.5, 87.31,
#                 82.41, 77.78, 73.42, 69.3, 65.41, 61.74, 58.27,
#                 55, 51.91, 49, 46.25, 43.65, 41.2, 38.89, 36.71,
#                 34.65, 32.7, 30.87, 29.14, 27.5]
# note_thrsh = [4068.54, 3840.19, 3624.66, 3421.22, 3229.2,
#                 3047.96, 2876.9, 2715.43, 2563.02, 2419.17,
#                 2283.39, 2155.23, 2034.27, 1920.1, 1812.33,
#                 1710.61, 1614.6, 1523.98, 1438.45, 1357.71,
#                 1281.51, 1209.59, 1141.7, 1077.62, 1017.13,
#                 960.05, 906.16, 855.3, 807.3, 761.99, 719.22,
#                 678.86, 640.75, 604.79, 570.85, 538.81,
#                 508.57, 480.02, 453.08, 427.65, 403.65,
#                 380.99, 359.61, 339.43, 320.38, 302.4,
#                 285.42, 269.4, 254.28, 240.01, 226.54,
#                 213.83, 201.83, 190.5, 179.81, 169.71,
#                 160.19, 151.2, 142.71, 134.7, 127.14,
#                 120.01, 113.27, 106.91, 100.91, 95.25,
#                 89.9, 84.86, 80.09, 75.6, 71.36, 67.35,
#                 63.57, 60, 56.64, 53.46, 50.46, 47.62,
#                 44.95, 42.43, 40.05, 37.8, 35.68, 33.68,
#                 31.79, 30, 28.32, 0]
# notes_list = ["C", "B", "Bb", "A", "Ab", "G", "F#", "F", "E", "Eb", "D", "C#"]
# third = False
# displays and sets up the tuner menu
def tuner_init(screen):
    global frequency
   
    global note
    
    global note_ind
    
    global freq
    triada = False
    screen.fill(white)
#     navi = main_init(screen)
    # Render and display all visual elements
    listen_button = show_botton(screen, "Start Listening", (160, 110), (120,40), white, button_font)
    play_button = show_botton(screen, "Play Note", (160,160), (80,40), white, button_font)
    minus_button = show_botton(screen, "-", (100,210), (30,30), white, button_font)

    text_surface = button_font.render("Frequency", True, black)
    freq_button = text_surface.get_rect(center=(160,210))
    screen.blit(text_surface, freq_button)

    plus_button = show_botton(screen, "+", (220,210), (30,30), white, button_font)
    back_button = show_botton(screen, "Back", (280,210), (50,50), white, button_font)

    triada_button = show_botton(screen, "Triada", (40,40), (50,30), white, button_font)

    text_surface = button_font.render(note, True, black)
    note_button = text_surface.get_rect(center=(120,30))
    screen.blit(text_surface, note_button)

    text_surface = button_font.render(str(frequency) + " Hz", True, black)
    hertz_button = text_surface.get_rect(center=(200,30))
    screen.blit(text_surface, hertz_button)
    update_freq(screen,frequency)
    pygame.display.flip()       # display workspace on screen

    # Check for button presses
    while True:
        for action in pygame.event.get():
            if (action.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                if click_in_button(back_button, pos):
                    # Return to main menu
                    print ("Back")
                    frequency= 440
                    note_ind=39
                    return True
                if click_in_button(listen_button, pos):
                    print ("Listening")
#                     update_freq(screen,frequency)
                    start_listening(screen)
#                     update_freq(screen,frequency)
                if click_in_button(play_button, pos):
                    # Play the specified note
                    print ("Play note")
                    update_freq(screen, frequency)
                    play_note(screen, frequency)
                if click_in_button(minus_button, pos):
                    # Decrease the frequency of the note to play
                    print ("-")
                    note_ind = min(note_ind+1,len(note_thrsh)-1)
                    frequency = note_freqs[note_ind]
                    update_freq(screen, frequency)
#                     frequencytuner = frequency
                if click_in_button(plus_button, pos):
                    # Increase the frequency of the note to play
                    print ("+")
                    note_ind = max(note_ind-1,0)
                    frequency = note_freqs[note_ind]
                    update_freq(screen, frequency)
#                     frequencytuner = frequency
                if click_in_button(triada_button, pos):
#                      # Increase the frequency of the note to play
                     print ("Triada")
                     triadas_init(screen)
                     frequency=440
                     note_ind=39
#                      frequency2= 6666#554.37
#                      note2= "C#ityum"
# update the frequency display
# def update_freq(screen, freq):
#     
#     freq_rect = pygame.Rect(200,30,80,20)
#     freq_rect.center = (200,30)
#     pygame.draw.rect(screen,white,freq_rect)
# 
#     text_surface = button_font.render("%4.0f Hz" % freq, True, black)
#     freq_button = text_surface.get_rect(center=(200,30))
#     screen.blit(text_surface, freq_button)
# 
#     index = get_note(freq)
#     note = notes_list[index % len(notes_list)]
#     note_rect = pygame.Rect(0,0,40,20)
#     note_rect.center = (120,30)
#     pygame.draw.rect(screen,white,note_rect)
# 
#     note_surface = button_font.render(note, True, black)
#     note_button = note_surface.get_rect(center=(120,30))
#     screen.blit(note_surface, note_button)
# 
#     freq_true = note_freqs[index]
#     margin = 0.1
#     tune_symbol = ' '
#     if (freq - freq_true > 0):
#         freq_step = 10
#         try:
#             freq_step = note_freqs[index-1]-note_freqs[index]
#         except:
#             freq_step = 200.0
#         if (freq-freq_true)/freq_step > margin:
#             tune_symbol = '#'
#     elif (freq - freq_true < 0):
#         freq_step = 10
#         try:
#             freq_step = note_freqs[index]-note_freqs[index+1]
#         except:
#             freq_step = 1.6
#         if (freq-freq_true)/freq_step < -margin:
#             tune_symbol = 'b'
# 
#     tune_rect = pygame.Rect(0,0,40,20)
#     tune_rect.center = (120, 50)
#     pygame.draw.rect(screen,white,tune_rect)
#     sharp_surface = button_font.render(tune_symbol, True, black)
#     sharp_text = sharp_surface.get_rect(center=(120,50))
#     screen.blit(sharp_surface, sharp_text)
# 
#     pygame.display.flip()
# 
# 
# 
# # listen for the note to be tuned
# # frequency detection courtesy of Scott Harden's project in real time audio visualization
# # in Python https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/
# def start_listening(screen):
# 
#     listen_button = show_botton(screen, "Stop Listening", (160, 110), (120,40), white, button_font)
# 
#     CHUNK = 4096 # number of data points to read at a time
#     RATE = 8000 # time resolution of the recording device (Hz)
# 
#     p=pyaudio.PyAudio() # start the PyAudio class
#     stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
#                   frames_per_buffer=CHUNK) #uses default input device
# 
#     listening = True
#     # create a numpy array holding a single read of audio data
#     while listening:
#         for action in pygame.event.get():
#             if (action.type is MOUSEBUTTONUP):
#                 pos = pygame.mouse.get_pos()
#                 if click_in_button(listen_button,pos):
#                     listening = False
# 
#         data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
#         data = data * np.hanning(len(data)) # smooth the FFT by windowing data
#         fft = abs(np.fft.fft(data).real)
#         fft = fft[:int(len(fft)/2)] # keep only first half
#         freq = np.fft.fftfreq(CHUNK,1.0/RATE)
#         freq = freq[:int(len(freq)/2)] # keep only first half
#         freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1
#         print("peak frequency: %d Hz"%freqPeak)
#         update_freq(screen,freqPeak)
# 
#     listen_button = show_botton(screen, "Start Listening", (160, 110), (120,40), white, button_font)
#     # close the stream gracefully
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
# 
# # plays a note at the frequency specified
# def play_note(screen, freq):
# 
#     play_button = show_botton(screen, "Stop Note", (160,160), (80,40), white, button_font)
#     playing = True
#     tone = Note(freq)
#     tone.play(-1)
#     while playing:
#         time.sleep(0.2)
#         for action in pygame.event.get():
#             if (action.type is MOUSEBUTTONUP):
#                 pos = pygame.mouse.get_pos()
#                 if click_in_button(play_button,pos):
#                     playing = False                    
#     
#     tone.stop()
#     
#     play_button =show_botton(screen, "Start Note", (160,160), (80,40), white, button_font)
# 
# # determine what note is being received
# # the frequency must be greater than 0
# def get_note(freq):
#     for i in range(len(note_thrsh)):
#         if freq > note_thrsh[i]:
#             return i
#     return "Not valid"