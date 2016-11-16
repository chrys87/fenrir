# fenrir (Alfa)
An TTY screenreader for Linux.
Its an early alpha version. You can test it. It is not recommended for production use. If you want to help just let me know.

# requirements (core)
- linux
- python3
- python-evdev
- loaded uinput kernel module
- Read permission to the following files:
  - /sys/devices/virtual/tty/tty0/active
  - /dev/vcsa[1-64]
- ReadWrite permission 
  - /dev/input
  - /dev/uinput
- speech, sound or braille drivers see "optional (features, drivers)".

# optional (features, drivers)
- "espeak" speech driver:
  - python-espeak
- "speechd" speech driver:
  - speech-dispatcher
  - python-speechd
- brltty braille driver (not implemented yet, WIP):
  - brltty (configured and running)
  - python-brlapi
- "generic" sound driver:
  - sox
- "gstreamer" sound driver
  - gstreamer 1.x
  - GLib
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
- sound driver: generic (via sox, could configured in settings.conf)
- speech driver: speechd
- braille driver: brltty (WIP)
