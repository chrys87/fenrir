#!/bin/bash

 # Make sure this script is ran as root
if [[ "$(whoami)" != "root" ]]; then
    echo "Please run $0 with oot privileges."
    exit 1
fi

write_pulse() {
sudo -u fenrirscreenreader cat << EOF > "/var/fenrirscreenreader/.config/pulse/client.conf"
# This file is part of PulseAudio.
#
# PulseAudio is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PulseAudio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PulseAudio; if not, see <http://www.gnu.org/licenses/>.

## Configuration file for PulseAudio clients. See pulse-client.conf(5) for
## more information. Default values are commented out.  Use either ; or # for
## commenting.

; default-sink =
; default-source =
default-server = unix:/tmp/pulse.sock 
; default-dbus-server =

autospawn = no
; autospawn = yes
; daemon-binary = /usr/bin/pulseaudio
; extra-arguments = --log-target=syslog

; cookie-file =

; enable-shm = yes
; shm-size-bytes = 0 # setting this 0 will use the system-default, usually 64 MiB

; auto-connect-localhost = no
; auto-connect-display = no
EOF
}

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
id fenrirscreenreader &> /dev/null || {
    useradd -m -d /var/fenrirscreenreader -r -G $input,$tty,$uinput -s /bin/nologin -U fenrirscreenreader;
    sleep 1;
    sudo -u fenrirscreenreader mkdir -p /var/fenrirscreenreader/.config/pulse;
    write_pulse;
}

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

exit 0
