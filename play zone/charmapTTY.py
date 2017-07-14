import time
from fcntl import ioctl
from array import array
import struct
import errno
import sys
charmap = {}
def updateCharMap(screen):
    ttyno = '4' 
    tty = open('/dev/tty' + screen, 'rb')
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
    for u, b in zip(utable[::2], utable[1::2]):
        if charmap.get(b) is None:
            charmap[b] = chr(u)


def autoDecodeVCSA(allData):
    allText = []
    allAttrib = []
    for y in range(rows):
        lineText = ''
        lineAttrib = []
        i = 0
        for x in range(cols):
            data = allData[i: i + 2]
            if data == b' \x07':
                #attr = 7
                #ink = 7
                #paper = 0
                #ch = ' '
                lineAttrib.append(7)             
                lineText += ' '
                continue
            (sh,) = struct.unpack("=H", data)
            attr = (sh >> 8) & 0xFF
            ch = sh & 0xFF
            if hichar == 0x100:
                attr >>= 1
            lineAttrib.append(attr)             
            ink = attr & 0x0F
            paper = (attr>>4) & 0x0F
            #if (ink != 7) or (paper != 0):
            #    print(ink,paper)
            if sh & hichar:
                ch |= 0x100
            try:
                lineText += charmap[ch]            
            except:
                lineText += chr('?')
            i += 2
        allText.append(lineText)
        allAttrib.append(lineAttrib)
    return allText, allAttrib

def m():
    s = time.time()
    updateCharMap('4')        
    print(time.time() -s )    
    vcsa = open('/dev/vcsa' + '4', 'rb')
    head = vcsa.read(4)
    rows = int(head[0])
    cols = int(head[1])
    text, attrib = autoDecodeVCSA(vcsa.read())
    print(time.time() -s )
    
