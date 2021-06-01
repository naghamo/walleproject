import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D21, 24)

while True:
    r=int(input('Enter red value: '))
    g=int(input('Enter green value: '))
    b=int(input('Enter blue value: '))
    pixels.fill((r,g,b))
    pixels.show()
    time.sleep(0.05)