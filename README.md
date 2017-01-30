# Fenrir
An TTY screenreader for Linux.
In theorie its not limited to linux. but i currently only provide drivers for that because I do not have an ohter system here. If you want to help or write drivers to make it work on other systems, just let me know. 
This software is licensed under the LGPL v3 .

# requirements (core)
- linux (currently only screen and input drivers available for that)
- python3 >= 3.3
- screen, input, speech, sound or braille drivers see "Features, Drivers, Extras".

# Features, Drivers, Extras
# Input Drivers:
- "evdevDriver" input driver for linux evdev
  - python-evdev 
  - loaded uinput kernel module
  - ReadWrite permission 
    - /dev/input
    - /dev/uinput

# Screen Drivers:
- "vcsaDriver" screen driver for linux VCSA devices
  - Read permission to the following files:
    - /sys/devices/virtual/tty/tty0/active
    - /dev/vcsa[1-64]

# Speech Drivers:
- "espeakDriver" speech driver for espeak:
  - python-espeak
- "speechdDriver" speech driver for speech-dispatcher:
  - speech-dispatcher
  - python-speechd
- "dummyDriver" speech driver for debugging

# Braille Drivers:
- "brlttyDriver" braille driver (WIP):
  - brltty (configured and running)
  - python-brlapi
- "dummyDriver" braille driver for debugging

# Sound Drivers:
- "genericDriver" sound driver for sound as subprocess:
  - sox
- "gstreamerDriver" sound driver for gstreamer
  - gstreamer 1.x
  - GLib
- "dummyDriver" sound driver for debugging

# Extra:
- spellchecker
  - python-pyenchant
  - aspell-YourLanguageCode (example aspell-en for us english)
- unix daemon:
  - python-daemonize

# installation
- Archlinux: PKGBUILD in AUR
- install.sh (there is currently no uninstall)
- run from git:
You can just run the following as root:
cd src/fenrir-package/
sudo ./fenrir
Settings "settings.conf" is located in the "config" directory.
Take care that the used drivers in the config matching your installed drivers. 
By default it uses:
- sound driver: genericDriver (via sox, could configured in settings.conf)
- speech driver: speechdDriver
- braille driver: brlttyDriver (WIP)
- input driver: evdevDriver
