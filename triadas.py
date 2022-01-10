import pygame # Import pygame graphics library
import RPi.GPIO as GPIO
from pygame.locals import *
import numpy as np
import time
from gui_functions import *
import pyaudio
import math
import itertools
#from itertools import zip
#from itertools import izip
from tone_player import Note
from metodosparatunertriadas import *
# import metodosparatunertriadas
from tuner import *
# from main_menu import main_init
frequency=440
# note="A"
# frequency0 = 4403454 # initial note frequency
# frequency2= 777#554.37
# note0 = "A77" # initial note
# note2= "C77#"
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
# 
def triadas_init(screen):
    global frequency
    global frequency0 
    global frequency2
    global frequency3
    global frequency4
    global frequency5
    global frequency6
#     global frec
    global note
    global note0
    global note2
    global note3
    global note4
    global note5
    global note6
    
    global note_ind
    global note_ind0
    global note_ind2
    global note_ind3#funciona graxcias a que le puse global creo
    global note_ind4
    global note_ind5
    global note_ind6
    
    root= False
    third = False
    terceramenor= False
    quintaperfecta=False
    quintadisminuida=False
    quintaaumentada=False
    retorno = False
    tercera= False
    screen.fill(white)
    root_button = show_botton(screen, "1", (40,40), (30,30), white, button_font)
    third_button = show_botton(screen, "3", (40,80), (30,30), white, button_font)
    thirdminor_button = show_botton(screen, "3m", (40,120), (30,30), white, button_font)
    fifth_perfect_button = show_botton(screen, "5", (190,40), (30,30), white, button_font)
    fifth_diminished_button = show_botton(screen, "5d", (190,80), (30,30), white, button_font)
    fifth_augmented_button = show_botton(screen, "5a", (190,120), (30,30), white, button_font)

    stop_button= show_botton(screen, "Stop Note", (40,210), (70,40), white, button_font)
    plus_button = show_botton(screen, "+", (220,210), (30,30), white, button_font)
    back2_button = show_botton(screen, "Back", (280,210), (50,50), white, button_font)
    
    text_surface = button_font.render("Frequency", True, black)
    freq_button = text_surface.get_rect(center=(160,210))
    screen.blit(text_surface, freq_button)
    
    minus_button = show_botton(screen, "-", (100,210), (30,30), white, button_font)
    
#     text_surface = button_font.render(note0, True, black)
#     note_button = text_surface.get_rect(center=(80,30))
#     screen.blit(text_surface, note_button)
# 
#     text_surface = button_font.render(str(frequency0) + " Hz", True, black)
#     hertz_button = text_surface.get_rect(center=(130,30))
#     screen.blit(text_surface, hertz_button)
#     
#     
#     text_surface = button_font.render(note2, True, black)
#     note_button = text_surface.get_rect(center=(80,50))
#     screen.blit(text_surface, note_button)
# 
#     text_surface = button_font.render(str(frequency2) + " Hz", True, black)
#     hertz_button = text_surface.get_rect(center=(120,50))
#     screen.blit(text_surface, hertz_button)
#     pygame.display.flip()       # display workspace on screen
    
#     navi = main_init(screen)    # Check for button presses
    while True:
        for action in pygame.event.get():
            if (action.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                
                if click_in_button(back2_button, pos) :
                    # Return to main menu
                    print ("Back2")
#                      screen.fill(white)
#                     navi==2
                    #tuner_init(screen)
#                     return True
                    screen.fill(white)
                    frequency0=440
                    
                    note_ind0=39 #no hace falta porque esto depende de la frecuencia
                    
                    frequency2=554.37
                    note_ind2=35
#                     
                    frequency3=523.25
                    note_ind3=36
                     
                    frequency4=659.26
                    note_ind4=31
                    
                    frequency5=622.25#diminished
                    note_ind5=32
#                     
                    frequency6=698.46
                    note_ind6=30
                    
                    
                    
#                     frequency2= 554.37
#                     note = "A" # initial note
#                     note2= "C#"
                    update_freq(screen, frequency)#creo q no sirve porq utiliza frecuency, no frecuency0
                    listen_button = show_botton(screen, "Start Listening", (160, 110), (120,40), white, button_font)
                    play_button = show_botton(screen, "Play Note", (160,160), (80,40), white, button_font)
                    triada_button = show_botton(screen, "Triada", (40,40), (50,30), white, button_font)
                    plus_button = show_botton(screen, "+", (220,210), (30,30), white, button_font)
                    back_button = show_botton(screen, "Back", (280,210), (50,50), white, button_font)
                    minus_button = show_botton(screen, "-", (100,210), (30,30), white, button_font)
                    text_surface = button_font.render("Frequency", True, black)
                    freq_button = text_surface.get_rect(center=(160,210))
                    screen.blit(text_surface, freq_button)
#                     text_surface = button_font.render(note, True, black)
#                     note_button = text_surface.get_rect(center=(120,30))
#                     screen.blit(text_surface, note_button)
# 
#                     text_surface = button_font.render(str(frequency) + " Hz", True, black)
#                     hertz_button = text_surface.get_rect(center=(200,30))
#                     screen.blit(text_surface, hertz_button)
#                     update_freq(screen, frequency)
#                     update_freq2(screen, frequency2)
                    pygame.display.flip()
#                     update_freq2(screen, frequency2)
#                     while True:
#                         for action in pygame.event.get():
#                             if (action.type is MOUSEBUTTONUP):
#                                 pos = pygame.mouse.get_pos()    
#                                 if click_in_button(listen_button, pos):
#                                     print ("Listening")
#                                     start_listening(screen)
#                                     update_freq0(screen,frequency0)
#                                 if click_in_button(play_button, pos):
#                                 # Play the specified note
#                                     print ("Play note")
#                                     play_note0(screen, frequency0)
#                                 
#                                 if click_in_button(back_button, pos):
#                                     # Return to main menu
#                                     print ("Back")
#                                     frequency= 440
#                                     frequency2= 554.37
#                                     return True
#                                     return True
#                                 else:
#                                     return False
#                    
                    
                    return True
                    
                if click_in_button(root_button, pos):
                    print("root note")
                    print(frequency0)
                    root=True
                    
                    update_freq0(screen, frequency0)
                    play_note0(screen, frequency0)                    
                if click_in_button(minus_button, pos):
                    print ("-")
                    note_ind0 = min(note_ind0+1,len(note_thrsh)-1)
                    frequency0 = note_freqs[note_ind0]
                    
                    note_ind2 = min(note_ind2+1,len(note_thrsh)-5)
                    frequency2 = note_freqs[note_ind2]
                    
                    note_ind3 = min(note_ind3+1,len(note_thrsh)-4)
                    frequency3 = note_freqs[note_ind3]
                    
                    note_ind4 = min(note_ind4+1,len(note_thrsh)-8)
                    frequency4 = note_freqs[note_ind4]
                    
                    note_ind5 = min(note_ind5+1,len(note_thrsh)-7)
                    frequency5 = note_freqs[note_ind5]
                    
                    note_ind6 = min(note_ind6+1,len(note_thrsh)-9)
                    frequency6 = note_freqs[note_ind6]
                    if (root==True):
#                         note_ind0 = min(note_ind0+1,len(note_thrsh)-1)
#                         frequency0 = note_freqs[note_ind0]
                        update_freq0(screen, frequency0)
                    
#                     El que más limita es la tónica en este caso
                    if (tercera==True):

#                         note_ind2 = min(note_ind2+1,len(note_thrsh)-5)
#                         frequency2 = note_freqs[note_ind2]
                        update_freq2(screen, frequency2)
                    if (terceramenor==True):
                        
#                         note_ind3 = min(note_ind3+1,len(note_thrsh)-4)
#                         frequency3 = note_freqs[note_ind3]
                        update_freq3(screen, frequency3)
                    if (quintaperfecta==True):
                    
#                         note_ind4 = min(note_ind4+1,len(note_thrsh)-8)
#                         frequency4 = note_freqs[note_ind4]
                        update_freq4(screen, frequency4)
                    if (quintadisminuida==True):                    
#                         note_ind5 = min(note_ind5+1,len(note_thrsh)-7)
#                         frequency5 = note_freqs[note_ind5]
                        update_freq5(screen, frequency5)
                    if (quintaaumentada==True):                    
#                         note_ind6 = min(note_ind6+1,len(note_thrsh)-9)
#                         frequency6 = note_freqs[note_ind6]
                        update_freq6(screen, frequency6)


#                     # Decrease the frequency of the note to play
#                     print ("-")
#                     note_ind0 = min(note_ind0+1,len(note_thrsh)-1)
#                     frequency0 = note_freqs[note_ind0]
#                     update_freq0(screen, frequency0)
#                     if(tercera== True):
#                         note_ind2 = min(note_ind2+1,len(note_thrsh)-5)# para que el tope sea 4 semitonos por encima de la tónica
#                         frequency2 = note_freqs[note_ind2]
#                         update_freq2(screen, frequency2)
#                     
#                     if(terceramenor== True):
#                         note_ind3 = min(note_ind3+1,len(note_thrsh)-4)# para que el tope sea 3 semitonos por encima de la tónica
#                         frequency3 = note_freqs[note_ind3]
#                         update_freq3(screen, frequency3)
#                     if(quintaperfecta==True):
#                         note_ind4 = min(note_ind4+1,len(note_thrsh)-8)# para que el tope sea 7 semitonos por encima de la tónica
#                         frequency4 = note_freqs[note_ind4]
#                         update_freq4(screen, frequency4)
#                         if(tercera== True):
#                             note_ind2 = min(note_ind2+1,len(note_thrsh)-5)# para que el tope sea 4 semitonos por encima de la tónica
#                             frequency2 = note_freqs[note_ind2]
#                             update_freq2(screen, frequency2)
#                     
#                         if(terceramenor== True):
#                             note_ind3 = min(note_ind3+1,len(note_thrsh)-4)# para que el tope sea 3 semitonos por encima de la tónica
#                             frequency3 = note_freqs[note_ind3]
#                             update_freq3(screen, frequency3)
#                         
#                         
#                     if(quintadisminuida==True):
#                         note_ind5 = min(note_ind5+1,len(note_thrsh)-7)# para que el tope sea 6 semitonos por encima de la tónica
#                         frequency5 = note_freqs[note_ind5]
#                         update_freq5(screen, frequency5)
#                         if(tercera== True):
#                             note_ind2 = min(note_ind2+1,len(note_thrsh)-5)# para que el tope sea 4 semitonos por encima de la tónica
#                             frequency2 = note_freqs[note_ind2]
#                             update_freq2(screen, frequency2)
#                     
#                         if(terceramenor== True):
#                             note_ind3 = min(note_ind3+1,len(note_thrsh)-4)# para que el tope sea 3 semitonos por encima de la tónica
#                             frequency3 = note_freqs[note_ind3]
#                             update_freq3(screen, frequency3)
#                     if(quintaaumentada==True):
#                         note_ind6 = min(note_ind6+1,len(note_thrsh)-9)# para que el tope sea 8 semitonos por encima de la tónica
#                         frequency6 = note_freqs[note_ind6]
#                         update_freq6(screen, frequency6)
#                         if(tercera== True):
#                             note_ind2 = min(note_ind2+1,len(note_thrsh)-5)# para que el tope sea 4 semitonos por encima de la tónica
#                             frequency2 = note_freqs[note_ind2]
#                             update_freq2(screen, frequency2)
#                     
#                         if(terceramenor== True):
#                             note_ind3 = min(note_ind3+1,len(note_thrsh)-4)# para que el tope sea 3 semitonos por encima de la tónica
#                             frequency3 = note_freqs[note_ind3]
#                             update_freq3(screen, frequency3)
                        
                    
                if click_in_button(plus_button, pos):
                    # Increase the frequency of the note to play
                    print ("+")
#                   tomando el caso más restrictivo que es la 5 aumentada los valores máximos de las notas quedarían así
#                   tomando el valor mas restrictivo de la tercera
                    note_ind0 = max(note_ind0-1,8)# para que aumente el root 1 semitono y que cuando llegue al  semitono se pare y asi la 5taaumentada pueda ser la primera frecuencia del lista
                    frequency0 = note_freqs[note_ind0]
                    
                    note_ind2 = max(note_ind2-1,4)# para que aumente la terecra 1 semitono y que llegue al 4 semitono como maximo pues se lleva 4 semitonos con la 5a aumentada
                    frequency2 = note_freqs[note_ind2]
                    
                    note_ind3 = max(note_ind3-1,5)# para que aumente el tercera menor1 semitono y que cuando llegue al 9 semitono se pare y asi la 5taaumentada pueda ser la primera frecuencia del lista
                    frequency3 = note_freqs[note_ind3]
                    
                    note_ind4 = max(note_ind4-1,1)# para que aumente el quinta justa 1 semitono y que cuando llegue al 9 semitono se pare y asi la 5taaumentada pueda ser la primera frecuencia del lista
                    frequency4 = note_freqs[note_ind4]
                    
                    note_ind5 = max(note_ind5-1,2)# para que aumente el quinta disminuida 1 semitono y que cuando llegue al 9 semitono se pare y asi la 5taaumentada pueda ser la primera frecuencia del lista
                    frequency5 = note_freqs[note_ind5]
                    
                    note_ind6 = max(note_ind6-1,0)# para que aumente el quinta aumentada 1 semitono y que cuando llegue al 0 semitono como másximo pues se lleva 0 semitonoscon la 5taaumentada,que es la primera frecuencia de la lista
                    frequency6 = note_freqs[note_ind6]
                    if (root==True):
#                         note_ind0 = max(note_ind0-1,8)# para que aumente el root 1 semitono y que cuando llegue al 9 semitono se pare y asi la 5taaumentada pueda ser la primera frecuencia del lista
#                         frequency0 = note_freqs[note_ind0]
                        update_freq0(screen, frequency0)
#                     la tercera respecto de la aumentada está a -4semitonos
                    if (tercera==True):
#                         note_ind2 = max(note_ind2-1,4)# para que aumente la terecra 1 semitono y que llegue al 4 semitono como maximo pues se lleva 4 semitonos con la 5a aumentada
#                         frequency2 = note_freqs[note_ind2]
                        update_freq2(screen, frequency2)
#                   la tercera menor respecto de la aumentada está a -5semitonos
                    if (terceramenor==True):
#                         note_ind3 = max(note_ind3-1,5)# para que aumente el root 1 semitono y que cuando llegue al 9 semitono se pare y asi la 5taaumentada pueda ser la primera frecuencia del lista
#                         frequency3 = note_freqs[note_ind3]
                        update_freq3(screen, frequency3)
#                   la quinta justa respecto de la aumentada está a -1semitonos
                    if (quintaperfecta==True):           
#                         note_ind4 = max(note_ind4-1,1)# para que aumente el root 1 semitono y que cuando llegue al 9 semitono se pare y asi la 5taaumentada pueda ser la primera frecuencia del lista
#                         frequency4 = note_freqs[note_ind4]
                        update_freq4(screen, frequency4)                
#                   la 5disminuida respecto de la aumentada está a -2semitonos
                    if (quintadisminuida==True):                    
#                         note_ind5 = max(note_ind5-1,2)# para que aumente el root 1 semitono y que cuando llegue al 9 semitono se pare y asi la 5taaumentada pueda ser la primera frecuencia del lista
#                         frequency5 = note_freqs[note_ind5]
                        update_freq5(screen, frequency5)                     
#                   la 5aumentada respecto de la aumentada está a -0semitonos
                    if (quintaaumentada==True):                    
#                         note_ind6 = max(note_ind6-1,0)# para que aumente el root 1 semitono y que cuando llegue al 9 semitono se pare y asi la 5taaumentada pueda ser la primera frecuencia del lista
#                         frequency6 = note_freqs[note_ind6]
                        update_freq6(screen, frequency6)                     
                     
                     
#                     note_ind0 = max(note_ind0-1,0)# para que aumente el root 1 semitono o si no puede más devuelva la 1era posición del array
#                     frequency0 = note_freqs[note_ind0]
#                     update_freq0(screen, frequency0)
#                     if(tercera== True):
#                         note_ind0 = max(note_ind0-1,4)# para que el tope sea 4 semitonos por debajo de la tónica(estando la tónica en posicion 0)
#                         frequency0 = note_freqs[note_ind0]
#                         update_freq0(screen, frequency0)
#                         note_ind2 = max(note_ind2-1,0)
#                         frequency2 = note_freqs[note_ind2]
#                         update_freq2(screen, frequency2)
#                         
#                     if(terceramenor== True):
#                         note_ind0 = max(note_ind0-1,3)# para que el tope sea 3 semitonos por debajo de la tónica(estando la tónica en posicion 0)
#                         frequency0 = note_freqs[note_ind0]
#                         update_freq0(screen, frequency0)
#                         note_ind3 = max(note_ind3-1,0)
#                         frequency3 = note_freqs[note_ind3]
#                         update_freq3(screen, frequency3)
#                         
#                     if(quintaperfecta== True):
#                         note_ind0 = max(note_ind0-1,7)# para que el tope de la tónica sea 7 semitonos por debajo de la quinta(estando la quinta en posicion 0)
#                         frequency0 = note_freqs[note_ind0]
#                         update_freq0(screen, frequency0)
#                         
#                         note_ind4 = max(note_ind4-1,0)
#                         frequency4 = note_freqs[note_ind4]
#                         update_freq4(screen, frequency4)
#                         if(terceramenor== True):
#                             note_ind3 = max(note_ind3-1,4)#para que el tope de la 3menor sea 4 semitonos por debajo de la quinta
#                             frequency3 = note_freqs[note_ind3]
#                             update_freq3(screen, frequency3)
#                         if(tercera== True):                        
#                             note_ind2 = max(note_ind2-1,3)#para que el tope de la 3 sea 3 semitonos por debajo de la quinta
#                             frequency2 = note_freqs[note_ind2]
#                             update_freq2(screen, frequency2)
#                     if(quintadisminuida== True):
#                         note_ind0 = max(note_ind0-1,6)# para que el tope de la tónica sea 6 semitonos por debajo de la quintadisminuida(estando la quintadisminuida en posicion 0)
#                         frequency0 = note_freqs[note_ind0]
#                         update_freq0(screen, frequency0)
#                         
#                         note_ind5 = max(note_ind5-1,0)
#                         frequency5 = note_freqs[note_ind5]
#                         update_freq5(screen, frequency5)
#                         if(terceramenor== True):
#                             note_ind3 = max(note_ind3-1,3)#para que el tope de la 3menor sea 4 semitonos por debajo de la quinta
#                             frequency3 = note_freqs[note_ind3]
#                             update_freq3(screen, frequency3)
#                         if(tercera== True):  #caso que nunca va a pasar para formar acorde porque no existe pero si que se puede pulsar si se tiene curiosidad                      
#                             note_ind2 = max(note_ind2-1,2)#para que el tope de la 3 sea 3 semitonos por debajo de la quinta
#                             frequency2 = note_freqs[note_ind2]
#                             update_freq2(screen, frequency2)       
#                     if(quintaaumentada== True):
#                         note_ind0 = max(note_ind0-1,8)# para que el tope de la tónica sea 6 semitonos por debajo de la quintadisminuida(estando la quintadisminuida en posicion 0)
#                         frequency0 = note_freqs[note_ind0]
#                         update_freq0(screen, frequency0)
#                         
#                         note_ind6 = max(note_ind6-1,0)
#                         frequency6 = note_freqs[note_ind6]
#                         update_freq6(screen, frequency6)
#                         if(terceramenor== True):
#                             note_ind3 = max(note_ind3-1,5)#para que el tope de la 3menor sea 4 semitonos por debajo de la quinta
#                             frequency3 = note_freqs[note_ind3]
#                             update_freq3(screen, frequency3)
#                         if(tercera== True):  #caso que nunca va a pasar para formar acorde porque no existe pero si que se puede pulsar si se tiene curiosidad                      
#                             note_ind2 = max(note_ind2-1,4)#para que el tope de la 3 sea 3 semitonos por debajo de la quinta
#                             frequency2 = note_freqs[note_ind2]
#                             update_freq2(screen, frequency2)
                
                            
                    
                    
                if click_in_button(third_button, pos):
                     # Increase the frequency of the note to play
#                     tercera= True
                    print ("Third")
                    
                    note_ind2 = max(note_ind0-4,0)#sumo 4 semitonos=2 tonos
                    frequency2 = note_freqs[note_ind2]
                    print (frequency2)
                    update_freq2(screen, frequency2)
                    play_note0(screen, frequency2)
                    tercera= True
                        
                if click_in_button(thirdminor_button,pos):
                    print ("Minor Third")
#                     terceramenor= True
                    note_ind3 = max(note_ind0-3,0)#sumo 3 semitonos=1+1/2 tonos
                    frequency3 = note_freqs[note_ind3]
                    print (frequency3)
                    update_freq3(screen, frequency3)
                    play_note0(screen, frequency3)
                    terceramenor= True
                if click_in_button(fifth_perfect_button, pos):
                     # Increase the frequency of the note to play
#                     quintaperfecta= True
                    print ("Perfect Fifth")

                    
                    note_ind4 = max(note_ind0-7,0)#sumo 7 semitonos=2+1+1/2 tonos
                    frequency4 = note_freqs[note_ind4]
                    print (frequency4)
                    update_freq4(screen, frequency4)
                    play_note0(screen, frequency4)
                    quintaperfecta= True
                if click_in_button(fifth_diminished_button, pos):
                     # Increase the frequency of the note to play
#                     quintadisminuida= True
                    print ("Diminished Fifth")
                                     
                    note_ind5 = max(note_ind0-6,0)#sumo 6 semitonos=3 tonos
                    frequency5 = note_freqs[note_ind5]
                    print (frequency5)
                    update_freq5(screen, frequency5)
                    play_note0(screen, frequency5)
                    quintadisminuida= True
                if click_in_button(fifth_augmented_button, pos):
                     # Increase the frequency of the note to play
#                     quintaaumentada = True
                    print ("Augmented Fifth")
                    

                    note_ind6 = max(note_ind0-8,0)#sumo 8 semitonos=2 tonos
                    frequency6 = note_freqs[note_ind6]
                    print (frequency6)
                    update_freq6(screen, frequency6)
                    play_note0(screen, frequency6)
                    quintaaumentada = True
        
# def update_freq(screen, freq):
#     freq_rect = pygame.Rect(200,30,80,20)
#     freq_rect.center = (200,30)
#     pygame.draw.rect(screen,white,freq_rect)
# 
#     text_surface = button_font.render("%4.0f Hz" % freq, True, black)
#     freq_button = text_surface.get_rect(center=(200,30))
#     screen.blit(text_surface, freq_button)
# 
#     index = get_note(freq)
#     note0 = notes_list[index % len(notes_list)]
#     note_rect = pygame.Rect(0,0,40,20)
#     note_rect.center = (120,30)
#     pygame.draw.rect(screen,white,note_rect)
# 
#     note_surface = button_font.render(note0, True, black)
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
# def update_freq0(screen, freq):
#     freq_rect = pygame.Rect(200,30,80,20)
#     freq_rect.center = (130,30)
#     pygame.draw.rect(screen,white,freq_rect)
# 
#     text_surface = button_font.render("%4.0f Hz" % freq, True, black)
#     freq_button = text_surface.get_rect(center=(130,30))
#     screen.blit(text_surface, freq_button)
# 
#     index = get_note(freq)
#     note0 = notes_list[index % len(notes_list)]
#     note_rect = pygame.Rect(0,0,40,20)
#     note_rect.center = (80,30)
#     pygame.draw.rect(screen,white,note_rect)
# 
#     note_surface = button_font.render(note0, True, black)
#     note_button = note_surface.get_rect(center=(80,30))
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
#     tune_rect.center = (80, 50)
#     pygame.draw.rect(screen,white,tune_rect)
#     sharp_surface = button_font.render(tune_symbol, True, black)
#     sharp_text = sharp_surface.get_rect(center=(80,50))
#     screen.blit(sharp_surface, sharp_text)
# 
#     pygame.display.flip()
# def update_freq2(screen, freq):
#     freq_rect = pygame.Rect(200,30,80,20)
#     freq_rect.center = (130,70)
#     pygame.draw.rect(screen,white,freq_rect)
# 
#     text_surface = button_font.render("%4.0f Hz" % freq, True, black)
#     freq_button = text_surface.get_rect(center=(130,70))
#     screen.blit(text_surface, freq_button)
# 
#     index = get_note(freq)
#     note2 = notes_list[index % len(notes_list)]
#     note_rect = pygame.Rect(0,0,40,20)
#     note_rect.center = (80,70)#cambio de 120 a 100
#     pygame.draw.rect(screen,white,note_rect)
# 
#     note_surface = button_font.render(note2, True, black)
#     note_button = note_surface.get_rect(center=(80,70))#cambio de 120 a 100
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
#     tune_rect.center = (80, 90)#cambio de 120 a 100
#     pygame.draw.rect(screen,white,tune_rect)
#     sharp_surface = button_font.render(tune_symbol, True, black)
#     sharp_text = sharp_surface.get_rect(center=(80,90))#cambio de 120 a 100
#     screen.blit(sharp_surface, sharp_text)
# 
#     pygame.display.flip()
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

# def play_note0(screen, freq):
#     play_button = show_botton(screen, "Stop Note", (40,210), (70,40), white, button_font)
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
#     
#     tone.stop()
#     
# #     play_button =show_botton(screen, "Start Note", (160,160), (80,40), white, button_font)

# determine what note is being received
# the frequency must be greater than 0
# def get_note(freq):
#     for i in range(len(note_thrsh)):
#         if freq > note_thrsh[i]:
#             return i
#     return "Not valid"




