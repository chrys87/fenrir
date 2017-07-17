import time
from fcntl import ioctl
from array import array
from struct import unpack_from
from struct import unpack
from struct import pack
import errno
import sys
charmap = {}
hichar = None
def updateCharMap(screen):
    global hichar
    ttyno = '4' 
    tty = open('/dev/tty' + screen, 'rb')
    GIO_UNIMAP = 0x4B66
    VT_GETHIFONTMASK = 0x560D
    himask = array("H", (0,))
    ioctl(tty, VT_GETHIFONTMASK, himask)
    hichar, = unpack_from("@H", himask)
    sz = 512
    line = ''
    while True:
        try:
            unipairs = array("H", [0]*(2*sz))
            unimapdesc = array("B", pack("@HP", sz, unipairs.buffer_info()[0]))
            ioctl(tty.fileno(), GIO_UNIMAP, unimapdesc)
            break
        except IOError as e:
            if e.errno != errno.ENOMEM:
                raise
            sz *= 2
    tty.close()
    ncodes, = unpack_from("@H", unimapdesc)
    utable = unpack_from("@%dH" % (2*ncodes), unipairs)
    for u, b in zip(utable[::2], utable[1::2]):
        if charmap.get(b) is None:
            charmap[b] = chr(u)


def autoDecodeVCSA(allData, rows, cols):
    allText = []
    allAttrib = []
    for y in range(rows):
        lineText = ''
        lineAttrib = []
        i = 0
        for x in range(cols):
            data = allData[i: i + 2]
            i += 2            
            if data == b' \x07':
                #attr = 7
                #ink = 7
                #paper = 0
                #ch = ' '
                lineAttrib.append(7)             
                lineText += ' '
                continue
            (sh,) = unpack("=H", data)
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
        allText.append(lineText)
        allAttrib.append(lineAttrib)
    return allText, allAttrib

def m(screen):
    s = time.time()
    updateCharMap(str(screen))        
    print(time.time() -s )    
    vcsa = open('/dev/vcsa' + str(screen), 'rb')
    head = vcsa.read(4)
    rows = int(head[0])
    cols = int(head[1])
    text, attrib = autoDecodeVCSA(vcsa.read(), rows, cols)
    print(time.time() -s )
    
