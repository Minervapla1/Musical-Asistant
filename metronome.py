# metronome.py
# Alexander Wood-Thomas, Jon Tsai
# adw75, jt765
# ECE5725 Final Project, 5/13/18
#   -displays the metronome tool for RPi Music Assistant. Provides visual
#    and audio output for metronome functionality, with buttons to change
#    beats per minute (bpm) rate

import pygame # Import pygame graphics library
import RPi.GPIO as GPIO
from pygame.locals import *
import numpy as np
import time
from gui_functions import *
import pyaudio
import math
import itertools
#from itertools import izip
import subprocess

bpm = 100 # initial beats per minute

# display the initial screen
def metro_init(screen):
    global bpm

    angle = 0 # angle for bouncing line

    screen.fill(white)

    # Render and display all visual elements
    minus_button = show_botton(screen, "-", (100,210), (30,30), white, button_font)

    text_surface = button_font.render("BPM", True, black)
    change_BPM = text_surface.get_rect(center=(160,210))
    screen.blit(text_surface, change_BPM)

    plus_button = show_botton(screen, "+", (220,210), (30,30), white, button_font)

    back_button = show_botton(screen, "Back", (280,210), (50,50), white, button_font)

    corchea_button = show_botton(screen, "1/2", (280,65), (30,30), white, button_font)
    semicorchea_button = show_botton(screen, "1/4", (280,95), (30,30), white, button_font)
    three_button = show_botton(screen, "3s", (280,125), (30,30), white, button_font)
    five_button = show_botton(screen, "5s", (280,155), (30,30), white, button_font)
    
    two_four_button = show_botton(screen, "2/4", (20,70), (25,25), white, button_font)
    six_eight_button = show_botton(screen, "6/8", (50,70), (25,25), white, button_font)
    three_four_button = show_botton(screen, "3/4", (20,100), (25,25), white, button_font)
    nine_eight_button = show_botton(screen, "9/8", (50,100), (25,25), white, button_font)
    four_four_button = show_botton(screen, "4/4", (20,130), (25,25), white, button_font)
    twelve_eight_button = show_botton(screen, "12/8", (50,130), (25,25), white, button_font)

    
    stop_button = show_botton(screen, "Stop", (30,210), (40,40), white, button_font)
    
    
    text_surface = button_font.render(str(bpm) + " BPM", True, black)
    bpm_button = text_surface.get_rect(center=(280,30))
    screen.blit(text_surface, bpm_button)
    
    text_surface = button_font.render("COMPÁS", True, black)
    bpm_button = text_surface.get_rect(center=(35,30))
    screen.blit(text_surface, bpm_button)

    pygame.display.flip()       # display workspace on screen

    start = time.time()
    tick_start = time.time()

    ticking = False
    ticking2 = False
    ticking3 = False
    ticking_2 = False
    ticking_4 = False
    ticking5 = False
    ticking6 = False
    ticking7 = False
    ticking8 = False
    ticking9 = False
    ticking10 = False
    corcheas=False 
    semicorcheas=False
    tresillos = False
    quintillos = False
    tipocompas= 0
#     count=0
    
    cmd = 'aplay -q /home/pi/Downloads/med.wav &'
    

    cmd2 = 'aplay -q /home/pi/Downloads/subdivision.wav &'
    
    cmd3 = 'aplay -q /home/pi/Downloads/fuerte.wav &'
    
    


    # Check for button presses
    while True:
        time.sleep(0.016)
        for action in pygame.event.get():
            if (action.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                if click_in_button(back_button, pos):
                    # Return to main menu
                    return True
                if click_in_button(minus_button, pos):
                    # Decrease the bpm
                    bpm = bpm - 5
                    update_bpm(screen, bpm)
                if click_in_button(plus_button, pos):
                    # Increase the bpm
                    bpm = bpm + 5
                    update_bpm(screen, bpm)
                if click_in_button(corchea_button,pos): 
                    print ("corcheas")
                    corcheas = True
                    
                    semicorcheas=False
                    tresillos = False
                    quintillos = False

                if click_in_button(semicorchea_button,pos): 
                    print ("Semicorcheas")
                    semicorcheas = True
                    
                    corcheas=False 
                    tresillos = False
                    quintillos = False

                if click_in_button(three_button,pos): 
                    print ("Tresillos")
                    tresillos = True
                    
                    corcheas=False 
                    semicorcheas=False
                    quintillos = False

                if click_in_button(five_button,pos): 
                    print ("Quintillos")
                    quintillos = True
                    
                    corcheas=False 
                    semicorcheas=False
                    tresillos = False
                    
                if click_in_button(four_four_button,pos): 
                    print ("4/4")
                    tipocompas= 1
                if click_in_button(three_four_button,pos): 
                    print ("3/4")
                    tipocompas= 2
                if click_in_button(six_eight_button,pos): 
                    print ("6/8")
                    tipocompas= 3
                
                if click_in_button(two_four_button,pos): 
                    print ("2/4")
                    tipocompas= 4
                
                if click_in_button(nine_eight_button,pos): 
                    print ("9/8")
                    tipocompas= 5
                
                
                if click_in_button(twelve_eight_button,pos): 
                    print ("12/8")
                    tipocompas= 6
                if click_in_button(stop_button,pos): 
                    
                    tipocompas= 0
                    corcheas=False 
                    semicorcheas=False
                    tresillos = False
                    quintillos = False
                    pygame.draw.circle(screen, white, (180,30), 8)
                    pygame.draw.circle(screen, white, (210,30), 8)
                    pygame.draw.circle(screen, white, (130,30), 10)
                   
                        
        #Display blinking dot and play a beat at the bpm rate
        current_time = time.time()
        frequency=bpm/60.0/2
        tick_freq=bpm/60.0

        period_time = (current_time - start) % (1.0/tick_freq)#tiempo dentro del periodo tiene que ser menor que 0.1
        if (period_time < 0.1) and not ticking:
            pygame.draw.circle(screen, red, (160,30), 10)
            subprocess.call(cmd, shell=True)
            ticking = True
 # erase the dot after 0.1 sec
                 
        if (period_time >= 0.1) and ticking:
            pygame.draw.circle(screen, white, (160,30), 10)
            ticking = False
            
        
    
        t = current_time - start - 1/4.0/frequency
        angle = math.pi/4* (1-4*abs(round(t*frequency)-t*frequency))

        pygame.draw.rect(screen, white, (70, 80, 190, 100))
        start_pos = np.array((160, 180))
        L = 100
        end_pos = start_pos + L*np.array((math.sin(angle), -math.cos(angle)))
        pygame.draw.line(screen, black, start_pos, end_pos, 3)
        pygame.display.flip()
        
        
        if (corcheas == True) :
            period_time_corchea = (current_time - start) % (1.0/(2*tick_freq))
            if (period_time_corchea < (1.0/(2*tick_freq))*1/2-0.01) and not ticking_2:
                pygame.draw.circle(screen, red, (180,30), 8)
                subprocess.call(cmd2, shell=True)
                ticking_2 = True
            if (period_time_corchea >= (1.0/(2*tick_freq))*1/2-0.01) and ticking_2:
                pygame.draw.circle(screen, white, (180,30), 8)
                ticking_2 = False 
            
        else:
            corcheas= False
        
        if (semicorcheas == True) :
            period_time_corchea = (current_time - start) % (1.0/(4*tick_freq))
            if (period_time_corchea < (1.0/(4*tick_freq))*1/4-0.01) and not ticking_4:
                pygame.draw.circle(screen, red, (180,30), 8)
                subprocess.call(cmd2, shell=True)
                ticking_4 = True
            if (period_time_corchea >= (1.0/(4*tick_freq))*1/4-0.01) and ticking_4:
                pygame.draw.circle(screen, white, (180,30), 8)
                ticking_4 = False 
            
        else:
            semicorcheas= False
        
        
        
        if (tresillos == True) :
            period_time2 = (current_time - start) % (1.0/(3*tick_freq))
            if (period_time2 < (1.0/(3*tick_freq))*1/3-0.01) and not ticking2:
                pygame.draw.circle(screen, red, (180,30), 8)
                subprocess.call(cmd2, shell=True)
                ticking2 = True
            if (period_time2 >= (1.0/(3*tick_freq))*1/3-0.01) and ticking2:
                pygame.draw.circle(screen, white, (180,30), 8)
                ticking2 = False 
            
        else:
            tresillos= False
            
        if (quintillos == True) :
            period_time3 = (current_time - start) % (1.0/(5*tick_freq))
            if (period_time3 < (1.0/(5*tick_freq))*1/5-0.01) and not ticking3:
                pygame.draw.circle(screen, red, (180,30), 8)
                subprocess.call(cmd2, shell=True)
                ticking3 = True
            if (period_time3 >= (1.0/(5*tick_freq))*1/5-0.01) and ticking3:
                pygame.draw.circle(screen, white, (180,30), 8)
                ticking3 = False 
            
        else:
            quintillos = False
            
        
        if (tipocompas == 1) :
            period_time4 = (current_time - start) % (4.0/tick_freq)#tiempo dentro del periodo tiene que ser menor que 0.1
            
            if (period_time4 < (1.0/tick_freq)*1/4-0.01) and not ticking5:
                pygame.draw.circle(screen, green, (130,30), 10)
                subprocess.call(cmd3, shell=True)
                ticking5 = True
            if (period_time4 >= (1.0/tick_freq)*1/4-0.01) and ticking5:
                pygame.draw.circle(screen, white, (130,30), 10)
                
                ticking5 = False
        if (tipocompas == 2) :
            period_time5 = (current_time - start) % (3.0/tick_freq)#tiempo dentro del periodo tiene que ser menor que 0.1
            
            if (period_time5 < (1.0/tick_freq)*1/3-0.01) and not ticking6:
                pygame.draw.circle(screen, green, (130,30), 10)
                subprocess.call(cmd3, shell=True)
                ticking6 = True
            if (period_time5 >= (1.0/tick_freq)*1/3-0.01) and ticking6:
                pygame.draw.circle(screen, white, (130,30), 10)
                
                ticking6 = False            

        if (tipocompas == 3) :
            period_time6 = (current_time - start) % (6.0/tick_freq)#tiempo dentro del periodo tiene que ser menor que 0.1
            
            if (period_time6 < (1.0/tick_freq)*1/6-0.01) and not ticking7:
                pygame.draw.circle(screen, green, (130,30), 10)
                subprocess.call(cmd3, shell=True)
                ticking7 = True
            if (period_time6 >= (1.0/tick_freq)*1/6-0.01) and ticking7:
                pygame.draw.circle(screen, white, (130,30), 10)
                
                ticking7 = False
                
        if (tipocompas == 4) :
            period_time7 = (current_time - start) % (2.0/tick_freq)#tiempo dentro del periodo tiene que ser menor que 0.1
            
            if (period_time7 < (1.0/tick_freq)*1/2-0.01) and not ticking8:
                pygame.draw.circle(screen, green, (130,30), 10)
                subprocess.call(cmd3, shell=True)
                ticking8 = True
            if (period_time7 >= (1.0/tick_freq)*1/2-0.01) and ticking8:
                pygame.draw.circle(screen, white, (130,30), 10)
                
                ticking8 = False
                
                
        if (tipocompas == 5) :
            period_time8 = (current_time - start) % (9.0/tick_freq)#tiempo dentro del periodo tiene que ser menor que 0.1
            
            if (period_time8 < (1.0/tick_freq)*1/9-0.01) and not ticking9:
                pygame.draw.circle(screen, green, (130,30), 10)
                subprocess.call(cmd3, shell=True)
                ticking9 = True
            if (period_time8 >= (1.0/tick_freq)*1/9-0.01) and ticking9:
                pygame.draw.circle(screen, white, (130,30), 10)
                
                ticking9 = False
                
        if (tipocompas == 6) :
            period_time9 = (current_time - start) % (12.0/tick_freq)#tiempo dentro del periodo tiene que ser menor que 0.1
            
            if (period_time9 < (1.0/tick_freq)*1/12-0.01) and not ticking10:
                pygame.draw.circle(screen, green, (130,30), 10)
                subprocess.call(cmd3, shell=True)
                ticking10 = True
            if (period_time9 >= (1.0/tick_freq)*1/12-0.01) and ticking10:
                pygame.draw.circle(screen, white, (130,30), 10)
                
                ticking10 = False    
            

    
    return True
    

def update_bpm(screen, bpm):
    bpm_rect = pygame.Rect(0,0,60,20)
    bpm_rect.center = (280,30)
    pygame.draw.rect(screen,white,bpm_rect)

    text_surface = button_font.render(str(bpm) + " BPM", True, black)
    bpm_button = text_surface.get_rect(center=(280,30))
    screen.blit(text_surface, bpm_button)

    pygame.display.flip()
