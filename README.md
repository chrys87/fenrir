# fenrir
An TTY screenreader for Linux. Its an early alpha version. you can test it. it is not recommented for productive use. if you want to help just let me know. 

# requirements
- linux
- python3
- python-espeak
- python-evdev
- loaded uinput kernelmodule
Read permission to the following files:
/sys/devices/virtual/tty/tty0/active
/dev/vcsa[1-64]
ReadWrite permission 
/dev/input
/dev/uinput

# optional 
- sox [using for soundicons via sox]
- speech-dispatcher, python3-speechd [for use the speech-dispatcher]
- brltty, python-brlapi [for using braille] # not implemented yet
- gstreamer [using for soundicons via gsteramer] # not working yet

# installation
Currently there is no setupscript (sorry). But you can just run src/fenrir-package/fenrir.py as root or setup the needed permissions




