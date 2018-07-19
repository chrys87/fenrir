#!/usr/bin/python

from cairo import *
from fcntl import ioctl
from array import array
import struct
import errno
import sys

GIO_UNIMAP = 0x4B66
VT_GETHIFONTMASK = 0x560D

if len(sys.argv) != 3:
    print "Usage: %s <tty-number> <output-png>" % sys.argv[0]
    exit()

ttyno = int(sys.argv[1])
png = sys.argv[2]

tty = open('/dev/tty%d' % ttyno, 'rb')
himask = array("H", (0,))
ioctl(tty, VT_GETHIFONTMASK, himask)
hichar, = struct.unpack_from("@H", himask)

sz = 512
while True:
    try:
        unipairs = array("H", [0]*(2*sz))
        unimapdesc = array("B", struct.pack("@HP", sz, unipairs.buffer_info()[0]))
        ioctl(tty.fileno(), GIO_UNIMAP, unimapdesc)
        break
    except IOError as e:
        if e.errno != errno.ENOMEM:
            raise
        sz *= 2
tty.close()

ncodes, = struct.unpack_from("@H", unimapdesc)
utable = struct.unpack_from("@%dH" % (2*ncodes), unipairs)

charmap = {}
for u, b in zip(utable[::2], utable[1::2]):
    if charmap.get(b) is None:
        charmap[b] = unichr(u)

vcs = open('/dev/vcsa%d' % ttyno, 'rb')

head = vcs.read(4)
rows = ord(head[0])
cols = ord(head[1])
caretX = ord(head[2])
caretY = ord(head[3])

surf = ImageSurface(FORMAT_RGB24, cols * 8, rows * 16)

cr = Context(surf)
cr.set_source_rgb(1,1,1)
cr.set_font_face(ToyFontFace("Mono", FONT_SLANT_NORMAL, FONT_WEIGHT_NORMAL));
m = Matrix()
m.scale(10.0, 12.0)
cr.set_font_matrix(m)

def CairoColor(b, a):
    return (b if a & 4 else 0, b if a & 2 else 0, b if a & 1 else 0)

for y in range(rows):
    for x in range(cols):
        data = vcs.read(2)
        (sh,) = struct.unpack("=H", data)
        attr = (sh >> 8) & 0xFF
        ch = sh & 0xFF
        if hichar == 0x100:
            attr >>= 1

        ink = attr & 0x0F
        paper = (attr>>4) & 0x0F
        b = 1.0 if attr & 0x80 else 0.75
        if sh & hichar:
            ch |= 0x100

        cr.set_source_rgb(*CairoColor(b, paper))
        cr.rectangle(x*8, y*16, 8, 16)
        cr.fill()

        cr.set_source_rgb(*CairoColor(b, ink))
        cr.move_to(x*8, 12 + y*16)
        cr.show_text(charmap.get(ch, u'?'))
        cr.stroke()
vcs.close()

surf.write_to_png(png)

