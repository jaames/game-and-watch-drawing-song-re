#!/usr/bin/env python3

from PIL import Image, ImageColor
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('rom', nargs=1, type=argparse.FileType('rb'))
parser.add_argument('--offset', '-l', type=int, default=4)
args = parser.parse_args()


args.rom[0].seek(args.offset)
im = Image.new('RGB', (256, 192)) 

palette = [
  (0, 0, 0),
  (255, 255, 255),
  (255, 0, 0), # probably wrong
  (0, 0, 255), # probably wrong
]

for y in range(0, 192):
  for x in range(0, 256, 4):
    byte = ord(args.rom[0].read(1))
    for pix in range(0, 4):
      color = byte >> (pix * 2) & 0x3
      im.putpixel( (x + pix, y), palette[color] ) 
            
im.show()
