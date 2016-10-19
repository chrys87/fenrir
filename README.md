# fenrir (Alfa)
An TTY screenreader for Linux.
Its an early alpha version. You can test it. It is not recommended for production use. If you want to help just let me know.

# requirements
- linux
- python3
- python-espeak
- python-evdev
- loaded uinput kernel module
Read permission to the following files:
/sys/devices/virtual/tty/tty0/active
/dev/vcsa[1-64]
ReadWrite permission 
/dev/input
/dev/uinput

# optional 
- sox [its used by default in the generic sound driver for playing sound-icons]
- speech-dispatcher, python3-speechd [to use the speech-dispatcher driver]
- brltty, python-brlapi [using braille] # (not implemented yet)
- gstreamer [soundicons via gstreamer] # not working yet
- python-pyenchant [spell check functionality]
- python-daemonize [use fenrir as background service on Unix like systems]

# installation
Currently there is no setupscript (sorry). But you can just run as root or setup needed permission
cd src/fenrir-package/
sudo ./fenrir.py
Settings are located in the config directory.
