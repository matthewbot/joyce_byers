#!/usr/bin/python

import time
import random

import ground
import walle

# Brightness constants
FULL = 1.
MOSTLY = 0.8
DIM = 0.4
OFF = 0.

# Time constants
LETTER_ON_DELAY = 1.
INTER_LETTER_DELAY = 0.5


LETTERS = {
        ['a'] = 1,
        ['b'] = 1,
        ['c'] = 1,
        ['d'] = 1,
        ['e'] = 1,
        ['f'] = 1,
        ['g'] = 1,
        ['h'] = 1,
        ['i'] = 1,
        ['j'] = 1,
        ['k'] = 1,
        ['l'] = 1,
        ['m'] = 1,
        ['n'] = 1,
        ['o'] = 1,
        ['p'] = 1,
        ['q'] = 1,
        ['r'] = 1,
        ['s'] = 1,
        ['t'] = 1,
        ['u'] = 1,
        ['v'] = 1,
        ['w'] = 1,
        ['x'] = 1,
        ['y'] = 1,
        ['z'] = 1,
       } 

class LedNetwork(object):
    """
    Base class for wrapping up LED arrays
    """
    COLORS = {letter: (0, 0, 0) for letter in LETTERS}

    def __init__(self):
        self.leds = {letter: None for letter in LETTERS}

    def set_letter(self, letter, brightness):
        red = self.COLORS[letter][0] * brightness
        green = self.COLORS[letter][1] * brightness
        blue = self.COLORS[letter][2] * brightness
        self._set_letter(self.leds[letter], red, green, blue)
        
    def set_all(self, brightness):
        for letter in self.leds.iterkeys():
            self.set_letter(letter, brightness)
        self.update()


class WalleWrapper(LedNetwork):
    """
    Wrapper around WallE library for controlling a string of LEDs
    """
    BASE_COLORS = [
              (1., 0., 0.),
              (0., 1., 0.),
              (0., 0., 1.),
              (1., 1., 0.),
             ]
    COLORS = {letter: random.choice(BASE_COLORS) for letter in LETTERS.iterkeys()}

    def __init__(self):
        self.network = walle.WallE(0,0)
        self.network.array.clear()
        self.network.array.autoupdate = False
        all_leds = [string.PrettyLed(led) for led in w.array.leds]
        self.leds = {letter: all_leds[index] for letter, index in LETTERS.iteriems()}

    def update(self):
        self.network.array.update()

    def _set_letter(self, led, red, green, blue):
        led.red = reg
        led.green = green
        led.blue = blue
        led.update()


class ConstellationWrapper(LedNetwork):
    """
    Wrapper around constellation ground library for controlling wirelss LEDs
    """
    BASE_COLORS = [
              (1., 0., 0.),
              (0., 1., 0.),
              (0., 0., 1.),
              (1., 1., 0.),
             ]
    COLORS = {letter: random.choice(BASE_COLORS) for letter in LETTERS.iterkeys()}
    def __init__(self):
        network = ground.GroundBase()
        network.parse_args()


class Alphabet(object):
    """
    Stranger Things' Joyce Byers' Chrismas Lights Alphabet
    """

    def __init__(self, wired=True):
        self._wired = wired
        if wired:
            self.leds = WalleWrapper()
        else:
            self.leds = ConstellationWrapper()
        self.normal()

    def text(self, message):
        self.off()
        
        cleaned = [char.lower() for char in message]
        for char in cleaned:
            self.leds.set_letter(char, MOSTLY)
            time.sleep(LETTER_ON_DELAY)
            self.leds.set_letter(char, OFF)
            time.sleep(INTER_LETTER_DELAY)

    def normal(self):
        self.leds.set_all(DIM)

    def full(self):
        self.leds.set_all(FULL)

    def off(self):
        self.leds.set_all(OFF)

    def message(self, text):
        self.text(text)
        self.normal()


