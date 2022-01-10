# tone_player.py
#
# Note class courtesy of hortonew: https://pythonexample.com/code/pygame-play-sound-sample/
#
# Run with the following command:
#   python pygame-play-tone.py

from array import array
from time import sleep

import pygame
from pygame.mixer import Sound, get_init, pre_init
try:
    #python2
    xrange
except NameError:
    #Python3, xrange is now named range
    xrange = range
class Note(Sound):
    def __init__(self, frequency, volume=.1):
        self.frequency = frequency
        Sound.__init__(self, buffer=self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for time in xrange(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples