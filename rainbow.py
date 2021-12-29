"""Make a RAINBOW!"""
# Based in part off of Adafruit's code in the tutorial at this URL: https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage

import time
import board
import neopixel
import signal
import sys


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
PIXEL_PIN = board.D18

# The number of NeoPixels
NUM_PIXELS = 50

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(0,255,1):
        for i in range(NUM_PIXELS):
            pixel_index = (i * 256 // NUM_PIXELS) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


def signal_handler(sig, frame):
    """Clear out LEDs when a signal is received"""
    print("\nSignal received ({})".format(sig))
    print("Clearing LEDs")
    for i in range(NUM_PIXELS):
        pixels[i] = (0, 0, 0)
    pixels.show()
    sys.exit(0)


# Gracefully handle a SIGINT (since this code never exits on its own)
signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    pixels = neopixel.NeoPixel(
        PIXEL_PIN, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER
    )

    while True:
        rainbow_cycle(0.0001)  # rainbow cycle with 1ms delay per step
