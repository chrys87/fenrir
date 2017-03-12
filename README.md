# Fenrir
A TTY screenreader for Linux.
In theory it's not just limited to Linux. but i currently only provide drivers for that since I do not have another system here. If you want to help or write drivers to make it work on other systems, just let me know. 
This software is licensed under the LGPL v3 .

# Requirements (core)
- linux (currently only screen and input drivers available for that)
- python3 >= 3.3
-	python-configargparse
- screen, input, speech, sound or braille drivers see "Features, Drivers, Extras".

# Features, Drivers, Extras, Dependencys
# Input Drivers:
1. "evdevDriver" input driver for linux evdev
  - python-evdev >=0.6.3
- This is commonly referred to as python3-evdev by your distribution
  - loaded uinput kernel module
  - ReadWrite permission 
    - /dev/input
    - /dev/uinput

# Screen Drivers:
1. "vcsaDriver" screen driver for linux VCSA devices
  - python-dbus
  - Read permission to the following files and services:
    - /sys/devices/virtual/tty/tty0/active
    - /dev/vcsa[1-64]
    - read systemd DBUS

# Speech Drivers:
1. "espeakDriver" speech driver for espeak:
  - python-espeak
- "speechdDriver" speech driver for speech-dispatcher:
  - speech-dispatcher
  - python-speechd
2. "dummyDriver" speech driver for debugging

# Braille Drivers:
1. "brlttyDriver" braille driver (WIP):
  - brltty (configured and running)
  - python-brlapi
2. "dummyDriver" braille driver for debugging

# Sound Drivers:
1. "genericDriver" sound driver for sound as subprocess:
  - sox
2. "gstreamerDriver" sound driver for gstreamer
  - gstreamer >=1.0
  - GLib
3. "dummyDriver" sound driver for debugging

# Extra:
1. spellchecker
  - python-pyenchant
  - aspell-YourLanguageCode (example aspell-en for us english)
2. unix daemon (also needed for systemd):
  - python-daemonize
3. Modify system volume:
  - pyalsaaudio (needs libasound2's headers).

# installation
- Archlinux: PKGBUILD in AUR
- Manual: run install.sh and uninstall.sh as root
- you also can just run it from Git without installing:
You can just run the following as root:
if you are in Fenrir Git rootfolder:
cd src/fenrir/
sudo ./fenrir
Settings "settings.conf" is located in the "config" directory or after installation in /etc/fenrir/settings.
Take care that the used drivers in the config matching your installed drivers. 
By default it uses:
- sound driver: genericDriver (via sox, could configured in settings.conf)
- speech driver: speechdDriver
- braille driver: brlttyDriver (WIP)
- input driver: evdevDriver
