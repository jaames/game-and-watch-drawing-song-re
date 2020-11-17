Poking around reverse-engineering the hidden "Mario Drawing Song" from the Game & Watch: Super Mario Bros console, to see how closely it matches the original Flipnote version.

Additions: 
- **viewframebuffer.py** - Extracts the framebuffer from a given ram dump, tweaked from viewmem.py to use the correct color format, image dimensions and offset
- **2bpp.py** - Extracts an image one of the 2-bit frame bitmaps that seem to be scattered throughout the RAM. Known offsets: 991524