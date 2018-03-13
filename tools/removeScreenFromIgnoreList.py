#!/bin/python
import os

def removeScreenFromIgnoreList(ignoreFileName = '/tmp/fenrirSuspend', screen = '1', useCurrentScreen = True):
    if useCurrentScreen:
        tty = open('/sys/devices/virtual/tty/tty0/active','r')
        screen = str(tty.read()[3:-1])
    ignoreScreens = []
    ignoreScreensStr = ''
    if ignoreFileName != '':
        if os.access(ignoreFileName, os.R_OK):
            with open(ignoreFileName, 'r') as fp:
                try:
                    ignoreScreens = fp.read().split(',')#.replace('\n','').split(',')
                except Exception as e:
                   print(e)

        if screen in ignoreScreens:
            ignoreScreens.remove(screen)
        ignoreScreensStr = ','.join(ignoreScreens)
           
        with open(ignoreFileName, 'w') as fp:
            fp.write(ignoreScreensStr)                
                
if __name__ == "__main__":
    removeScreenFromIgnoreList()
