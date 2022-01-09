#!/usr/bin/env python3
# 
# Playing with various animations on a strip of NeoPixels.
# Based off of strandtest.py

import time
import rpi_ws281x as ws
import argparse


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def reverseColorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels(), -1, -1):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return ws.Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return ws.Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return ws.Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)


def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear display on exit')
    parser.add_argument('-n', '--numpixels', dest='led_count', type=int, default=50, help='number of LED pixels')
    parser.add_argument('-p', '--pin', dest='led_pin', type=int, default=18, help='GPIO pin connected to the pixels (18 uses PWM!, 10 uses SPI /dev/spidev0.0')
    parser.add_argument('-f', '--freq', dest='led_freq_hz', type=int, default=800000, help='LED signal frequency in hertz (usually 800khz)')
    parser.add_argument('--dma', dest='led_dma', type=int, default=10, help='DMA channel to use for generating signal (try 10)')
    parser.add_argument('-b', '--bright', dest='led_brightness', type=int, default=20, help='set to 0 for darkest and 255 for brightest')
    parser.add_argument('-i', dest='led_invert', action='store_true', help='invert the signal (when using NPN transistor level shift)')
    parser.add_argument('--channel', dest='led_channel', type=int, default=0, help='set to "1" for GPIOs 13, 19, 41, 45 or 53, otherwise use "0"')
    parser.add_argument('--type', dest='led_type', default='RBG', choices={'GRB', 'RGB', 'RBG', 'GBR', 'BRG', 'BGR'}, help='order of colors the strip uses')
    args = parser.parse_args()

    # Convert led_type to object
    # TODO: Need more elegant way to manage "type". This doesn't handle any 'W' strips. 
    #       Although I probably won't ever change it again now that I know what this strip is.
    if args.led_type == 'GRB':
        strip_type = ws.WS2811_STRIP_GRB
    elif args.led_type == 'GBR':
        strip_type = ws.WS2811_STRIP_GBR
    elif args.led_type == 'RBG':
        strip_type = ws.WS2811_STRIP_RBG
    elif args.led_type == 'RGB':
        strip_type = ws.WS2811_STRIP_RGB
    elif args.led_type == 'BRG':
        strip_type = ws.WS2811_STRIP_BRG
    elif args.led_type == 'BGR':
        strip_type = ws.WS2811_STRIP_BGR

    # Create NeoPixel object with appropriate configuration.
    strip = ws.PixelStrip(args.led_count, args.led_pin, args.led_freq_hz, args.led_dma, args.led_invert, args.led_brightness, args.led_channel, strip_type)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            colorWipe(strip, ws.Color(255, 0, 0), 10)  # Red wipe
            reverseColorWipe(strip, ws.Color(0, 0, 0), 10)  # Blank reverse wipe
    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, ws.Color(0,0,0), 10)