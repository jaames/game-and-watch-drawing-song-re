Poking around reverse-engineering the hidden "Mario Drawing Song" from the Game & Watch: Super Mario Bros console, to see how closely it matches the original Flipnote version. 

The end goal is seeing if it's possible to swap in our own Flipnote .ppms

Additions: 
- **patch_flash_gif.py** - Extracts source GIF from a decrypted flash dump. Most of the header blocks have been stripped, so this tries to patch it up into a valid GIF. Not 100% working, but close
- **viewframebuffer.py** - Extracts the framebuffer from a given memory dump, tweaked from viewmem.py to use the correct color format, image dimensions and offset
- **2bpp.py** - Extracts the packed 2-bit 256*192 frame bitmap at 0xF2124 in memory. This is the source image that gets converted into rgb565(?) for the framebuffer.
- **decode_audio.py** - Extracts the audio from a decrypted flash dump, decodes it, nearest-neighbour interpolates it to 48KHz to match real hardware, and saves it as a WAV file.
