#!/bin/python3
#attrib:
#http://rampex.ihep.su/Linux/linux_howto/html/tutorials/mini/Colour-ls-6.html
#0 = black, 1 = blue, 2 = green, 3 = cyan, 4 = red, 5 = purple, 6 = brown/yellow, 7 = white. 
from fcntl import ioctl
from array import array
import struct
import errno
import sys

ttyno = 4 
tty = open('/dev/tty%d' % ttyno, 'rb')
vcs = open('/dev/vcsa%d' % ttyno, 'rb')

head = vcs.read(4)
rows = int(head[0])
cols = int(head[1])


GIO_UNIMAP = 0x4B66
VT_GETHIFONTMASK = 0x560D
himask = array("H", (0,))
ioctl(tty, VT_GETHIFONTMASK, himask)
hichar, = struct.unpack_from("@H", himask)

sz = 512
line = ''
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
        charmap[b] = u

allText = []
allAttrib = []
for y in range(rows):
    lineText = ''
    lineAttrib = []
    for x in range(cols):
        data = vcs.read(2)
        (sh,) = struct.unpack("=H", data)
        attr = (sh >> 8) & 0xFF
        ch = sh & 0xFF
        if hichar == 0x100:
            attr >>= 1
        lineAttrib.append(attr)             
        ink = attr & 0x0F
        paper = (attr>>4) & 0x0F
        if (ink != 7) or (paper != 0):
            print(ink,paper)
        if sh & hichar:
            ch |= 0x100
        lineText += chr(charmap.get(ch, u'?'))
    allText.append(lineText)
    allAttrib.append(lineAttrib)

print(allText)
print(allAttrib)
