#!/bin/bash

 # Make sure this script is ran as root
if [[ "$(whoami)" != "root" ]]; then
    echo "Please run $0 with oot privileges."
    exit 1
fi

# This script checks for, and creates if needed, the fenrirscreenreader user.

# Find out which group to use for uinput
uinput="$(stat -c '%G' /dev/uinput | grep -v root)"
if ! [[ "$uinput" =~ ^[a-zA-Z]+$ ]]; then
    groupadd -r uinput
    chown root:uinput /dev/uinput
fi

# find out which group to use for /dev/input.
input="$(stat -c '%G' /dev/input/* | grep -v root | head -1)"
if ! [[ "$input" =~ ^[a-zA-Z]+$ ]]; then
    # Create the input group
    groupadd --system input
    echo 'KERNEL=="event*", NAME="input/%k", MODE="660", GROUP="input"' >> /etc/udev/rules.d/99-input.rules
    input="input"
fi

# find out which group to use for /dev/tty.
tty="$(stat -c '%G' /dev/tty | grep -v root)"
if ! [[ "$tty" =~ ^[a-zA-Z]+$ ]]; then
    # Create the tty group
    groupadd --system tty
    echo 'KERNEL=="event*", NAME="tty/%k", MODE="660", GROUP="tty"' >> /etc/udev/rules.d/99-tty.rules
    tty="tty"
fi

# Add fenrirscreenreader
id fenrirscreenreader &> /dev/null || \
    useradd -m -d /var/fenrirscreenreader -r -G $input,$tty,$uinput -s /bin/nologin -U fenrirscreenreader

#configure directory structure.
mkdir -p /var/log/fenrirscreenreader /etc/fenrirscreenreader

# Set directory ownership
chown -R fenrirscreenreader:fenrirscreenreader /var/log/fenrirscreenreader
chmod -R 755 /var/log/fenrirscreenreader
chown -R root:fenrirscreenreader /etc/fenrirscreenreader

# Fix permissions on tty#s
for i in /dev/tty[0-9]* ; do
    chmod 660 "$i"
done

sudo -Hu fenrirscreenreader mkdir ~/.config/{pipewire,pulse}
echo "Remember to run the configuration script for the sound server you are using as the fenrirscreenreader user."
echo "For example, to configure pipewire, run the following:"
echo 'sudo -Hu fenrirscreenreader /usr/share/fenrirscreenreader/tools/configure_pipewire.sh'

exit 0
