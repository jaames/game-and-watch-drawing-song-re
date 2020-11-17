Poking around reverse-engineering the hidden "Mario Drawing Song" from the Game & Watch: Super Mario Bros console, to see how closely it matches the original Flipnote version. 

The end goal is seeing if it's possible to swap in our own Flipnote .ppms

Additions: 
- **viewframebuffer.py** - Extracts the framebuffer from a given memory dump, tweaked from viewmem.py to use the correct color format, image dimensions and offset
- **2bpp.py** - Extracts the packed 2-bit 256*192 frame bitmap at 0xF2124 in memory. This is the source image that gets converted into rgb565(?) for the framebuffer. It's likely streamed in from flash storage since I don't see any other frames in memory, so until that's been fully decrpyted this is as far as I've managed to get.