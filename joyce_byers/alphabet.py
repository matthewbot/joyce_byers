#!/usr/bin/python

import time
import random

#import ground
import joyce_byers.walle as walle

# Brightness constants
FULL = 1.
MOSTLY = 0.8
DIM = 0.4
OFF = 0.

# Time constants
LETTER_ON_DELAY = 1.
INTER_LETTER_DELAY = 0.5


LETTERS = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8,
    'i': 9,
    'j': 10,
    'k': 11,
    'l': 12,
    'm': 13,
    'n': 14,
    'o': 15,
    'p': 16,
    'q': 17,
    'r': 18,
    's': 19,
    't': 20,
    'u': 21,
    'v': 22,
    'w': 23,
    'x': 24,
    'y': 25,
    'z': 26,
}

class LedNetwork(object):
    """
    Base class for wrapping up LED arrays
    """
    BASE_COLORS = [
        (1., 0., 0.),
        (0., 1., 0.),
        (0., 0., 1.),
        (1., 1., 0.),
    ]

    def __init__(self):
        self.leds = {letter: None for letter in LETTERS}
        self.COLORS = {letter: random.choice(self.BASE_COLORS) for letter in LETTERS.iterkeys()}

    def set_letter(self, letter, brightness):
        red = self.COLORS[letter][0] * brightness
        green = self.COLORS[letter][1] * brightness
        blue = self.COLORS[letter][2] * brightness
        self.set_led(self.leds[letter], red, green, blue)
        self.update()

    def set_all(self, brightness):
        for letter in self.leds.iterkeys():
            self.set_letter(letter, brightness)
        self.update()

    def update(self):
        pass

    def set_led(self, led, red, green, blue):
        pass


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

    def __init__(self):
        super(WalleWrapper, self).__init__()
        self.network = walle.WallE(0, 0)
        self.network.array.clear()
        self.network.array.autoupdate = False
        all_leds = [walle.PrettyLed(led) for led in self.network.array.leds]
        self.leds = {letter: all_leds[index] for letter, index in LETTERS.iteritems()}

    def update(self):
        self.network.array.update()

    def set_led(self, led, red, green, blue):
        led.red = red
        led.green = green
        led.blue = blue


# class ConstellationWrapper(LedNetwork):
#     """
#     Wrapper around constellation ground library for controlling wirelss LEDs
#     """
#     BASE_COLORS = [
#               (255, 0., 0.),
#               (0., 255, 0.),
#               (0., 0., 255),
#               (255, 255, 0.),
#              ]
#     COLORS = {letter: random.choice(BASE_COLORS) for letter in LETTERS.iterkeys()}
#     def __init__(self):
#         network = ground.GroundBase()
#         network.parse_args()


class Alphabet(object):
    """
    Stranger Things' Joyce Byers' Chrismas Lights Alphabet
    """

    def __init__(self, wired=True):
        self._wired = wired
        if wired:
            self.leds = WalleWrapper()
#        else:
#            self.leds = ConstellationWrapper()
        self.normal()

    def text(self, message):
        self.off()
        time.sleep(1)

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

    def flicker(self):
        for flash in range(10):
            brightness = random.random()
            self.off()
            time.sleep(random.random())
            self.leds.set_all(brightness)
            time.sleep(random.random())
        self.normal()
