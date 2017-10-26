#!/usr/bin/python

import time
import random

from constellation.ground import ground_base
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

#    def __init__(self):
#        self.leds = {}
#        self.COLORS = {led: random.choice(self.BASE_COLORS) for led in range(len(self.leds))}

    def set_letter(self, letter, brightness, update=False):
        self.set_led_brightness(LETTERS[letter], brightness)
        if update:
            self.update()

    def set_all_letters(self, brightness):
        for letter in LETTERS.iterkeys():
            self.set_letter(letter, brightness)
        self.update()

    def set_all_leds(self, brightness):
        for led in self.leds.itervalues():
            self.set_led_brightness(led, brightness)
        self.update()

    def update(self):
        pass

    def set_led_brightness(self, led, brightness):
        red = self.COLORS[led][0] * brightness
        green = self.COLORS[led][1] * brightness
        blue = self.COLORS[led][2] * brightness
        self.set_led(led, red, green, blue)

    def set_led(self, led, red, green, blue):
        pass


class WalleWrapper(LedNetwork):
    """
    Wrapper around WallE library for controlling a string of LEDs
    """
    def __init__(self):
        super(WalleWrapper, self).__init__()
        self.network = walle.WallE(0, 0)
        self.network.array.clear()
        self.network.array.autoupdate = False
        self.leds = {idx: walle.PrettyLed(led) for idx, led in enumerate(self.network.array.leds)}
        self.COLORS = {idx: random.choice(self.BASE_COLORS) for idx in range(len(self.leds))}
#        self.leds = {letter: all_leds[index] for letter, index in LETTERS.iteritems()}
        print self.leds.keys()
        print self.COLORS.keys()

    def update(self):
        self.network.array.update()

    def set_led(self, led, red, green, blue):
        self.leds[led].red = red
        self.leds[led].green = green
        self.leds[led].blue = blue


class ConstellationWrapper(LedNetwork):
    """
    Wrapper around constellation ground library for controlling wirelss LEDs
    """
    def __init__(self):
        self.network = ground_base.GroundBase()
        self.network.parse_args()
        self.leds = {idx: idx for idx in range(self.network.NUM_NODES)}
        self.COLORS = {idx: random.choice(self.BASE_COLORS) for idx in range(len(self.leds))}
        self.led_vals = {}
        print self.leds
        print self.COLORS.keys()

    def update(self):
        self.network.set_nodes(self.led_vals)
        self.led_vals = {}
   
    def set_led(self, led, red, green, blue):
        red = int(red * 255)
        green = int(green * 255)
        blue = int(blue * 255)
        self.led_vals[led] = (red, green, blue, 255)


class Alphabet(object):
    """
    Stranger Things' Joyce Byers' Chrismas Lights Alphabet
    """

    def __init__(self):
        self.letters = WalleWrapper()
        self.extras = ConstellationWrapper()
        self.normal()

    def text(self, message):
        self.off()
        time.sleep(1)

        cleaned = [char.lower() for char in message]
        for char in cleaned:
            self.flicker_letter(char)
            self.letters.set_letter(char, OFF, update=True)
            time.sleep(INTER_LETTER_DELAY)

    def normal(self, extras=True):
        self.letters.set_all_letters(DIM)
        if extras:
            self.extras.set_all_leds(DIM)

    def full(self, extras=True):
        self.letters.set_all_letters(FULL)
        if extras:
            self.extras.set_all_leds(FULL)

    def off(self, extras=True):
        self.letters.set_all_letters(OFF)
        if extras:
            self.extras.set_all_leds(OFF)

    def message(self, text):
        self.flicker(20)
        self.fade(MOSTLY, FULL, 1)
        time.sleep(2)
        self.fade(FULL, OFF, 0.5)
        time.sleep(0.5)
        self.text(text)
        time.sleep(3)
        self.fade(OFF, DIM, 1)

    def flicker(self, cycles=20):
        for flash in range(cycles):
            brightness = random.random() / 10. + 0.9
            self.off()
            time.sleep(random.random() / 10)
            self.letters.set_all_letters(brightness)
            self.extras.set_all_leds(brightness)
            time.sleep(random.random() / 10)

    def fade(self, frm=0., to=1., duration=3):
        step = 1 if to > frm else -1
        to = int(to * 100)
        frm = int(frm * 100)
        delay = 1. * duration / abs(to - frm)
        for brightness in range(frm, to, step):
            self.letters.set_all_letters(brightness / 100.)
            self.extras.set_all_leds(brightness / 100.)
            time.sleep(delay)
        
    def flicker_letter(self, letter, cycles=5):
        for flash in range(cycles):
            brightness = random.random() / 10. + 0.9
            self.letters.set_letter(letter, OFF, update=True)
            time.sleep(random.random() / 20)
            self.letters.set_letter(letter, brightness, update=True)
            time.sleep(random.random() / 20)
