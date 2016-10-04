#!/bin/python

import time

from sound.gstreamer import sound

s = sound()
s.playSoundFile('/home/chrys/Projekte/fenrir/fenrir/src/fenrir-package/1ChangeTTY.opus')
time.sleep(10)
