from sys import argv

def read_image_block(gif):
  data = bytes()
  while True:
    block_head = gif.read(1)
    if block_head == b'\x00': 
      break
    data += block_head + gif.read(ord(block_head))
  return data

with open(argv[1], 'rb') as flash, open(argv[2], 'wb') as out_gif:
  flash.seek(0x12D44)
  out_gif.write(flash.read(25))
  min_size = flash.read(1)
  out_gif.write(bytes([
    # netscape ext
    0x21, 0xFF, 0x0B, 0x4E, 0x45, 0x54, 0x53, 0x43, 0x41, 0x50, 0x45, 0x32, 0x2E, 0x30, 0x03, 0x01, 0x00, 0x00, 0x00
  ]))
  i = 0
  while True:
    block = read_image_block(flash)
    is_new_frame = i < 21
    use_local_color_table = i > 0
    out_gif.write(bytes([
      # gfx ctrl ext
      0x21, 0xF9, 0x04, 0x00 if is_new_frame else 0x01, 0x08, 0x00, 0x00, 0x00, 
      # image desc
      0x2C, 0x00, 0x00, 0x00 , 0x00, 0x00, 0x01, 0xC0, 0x00, 0x81 if use_local_color_table else 0x00
    ]))
    if use_local_color_table:
      out_gif.write(bytes([
        # local color table
        0xff, 0xff, 0xff,
        0x00, 0x00, 0x00,
        0x00, 0x00, 0xff,
        0xff, 0x00, 0x00,
      ]))
    i += 1
    out_gif.write(min_size)
    out_gif.write(block)
    out_gif.write(bytes(1))
    if len(block) == 0:
      break
    