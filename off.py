"""Reset pixels to "off"."""

import board
import neopixel


PIXEL_PIN = board.D18
NUM_PIXELS = 50
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS)

for i in range(NUM_PIXELS):
    pixels[i] = (0, 0, 0)
pixels.show()
