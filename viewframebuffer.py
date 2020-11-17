#!/usr/bin/env python3

from PIL import Image, ImageColor
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('rom', nargs=1, type=argparse.FileType('rb'))
args = parser.parse_args()

args.rom[0].seek(0x1A000)
im = Image.new('RGB', (320, 480))

for y in range(0, 480):
    for x in range(0, 320):
        try:
            # I only have a black and white image to reference here, but it's def 16bpp, so assuming rgb565 for now
            data = args.rom[0].read(2)
            pixel = data[0] | data[1] << 8
            r = (pixel       & 0x1f)
            g = (pixel >> 5  & 0x3f)
            b = (pixel >> 11 & 0x1f) 
            r = r << 3 | (r >> 2)
            g = g << 2 | (g >> 4)
            b = b << 3 | (b >> 2)
            im.putpixel( (x, y), (r, g, b) ) 
        except:
            im.putpixel( (x, y), (0,0,0) ) 
            
im.show()
