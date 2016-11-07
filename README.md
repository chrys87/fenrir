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
- aspell-<language> [your languagedata for spellchecker, english support "aspell-en"]
- python-daemonize [use fenrir as background service on Unix like systems]

# installation
- Archlinux: PKGBUILD in AUR
- install.sh (there is currently no uninstall)
- run from git:
You can just run the following as root:
cd src/fenrir-package/
sudo ./fenrir
Settings are located in the "config" directory.

