#!/bin/bash

 # Make sure this script is ran as root
if [[ "$(whoami)" != "root" ]]; then
    echo "Please run $0 with oot privileges."
    exit 1
fi

# This script checks for, and creates if needed, the fenrirscreenreader user.

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
id fenrirscreenreader &> /dev/null || {
    useradd -m -d /var/fenrirscreenreader -r -G $input,$tty -s /bin/nologin -U fenrirscreenreader;
    sudo -u fenrirscreenreader mkdir -p /var/fenrirscreenreader/.config/pulse;
    sudo -u fenrirscreenreader echo -e '.include /etc/pulse/default.pa\nload-module module-switch-on-connect\nload-module module-native-protocol-unix auth-anonymous=1 socket=/tmp/pulse.sock' > /var/fenrirscreenreader/.config/pulse/default.pa;
}

#configure directory structure.
mkdir -p /var/log/fenrirscreenreader /etc/fenrirscreenreader

# Set directory ownership
chown -R fenrirscreenreader:fenrirscreenreader /var/log/fenrirscreenreader
chmod -R 755 /var/log/fenrirscreenreader
chown -R root:fenrirscreenreader /etc/fenrirscreenreader
