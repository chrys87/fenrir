#!/bin/bash

# This script configures pulse to work both in the graphical invironment and in the console with root apps.

# Make sure we aren't started as root:
if [[ $(whoami) = "root" ]]; then
    echo "Please don't start this script with root priveleges, the script will call sudo when needed."
    exit 1
fi

# Get the current user's XDG_HOME
xdgPath="${XDG_CONFIG_HOME:-$HOME/.config}"

# Warn user if we are going to overwrite an existing default.pa
if [ -f "$xdgPath/pulse/default.pa" ]; then
    read -p "This will replace the current file located at $xdgPath/pulse/default.pa, press enter to continue or control+c to abort. " continue
fi
echo '.include /etc/pulse/default.pa
load-module module-native-protocol-unix auth-anonymous=1 socket=/tmp/pulse.sock' > $xdgPath/pulse/default.pa

# This section does the root part:
read -p "This next sections requires root priveleges.. If you don't have access to sudo, please control c to abort this script, if you can use sudo, press enter to continue. " continue


# Get root's 's XDG_HOME
xdgPath="$(sudo bash -c '${XDG_CONFIG_HOME:-$HOME/.config}')"

# Warn user if we are going to overwrite an existing default.pa
if [ -f "$xdgPath/pulse/default.pa" ]; then
    read -p "This will replace the current file located at $xdgPath/pulse/default.pa, press enter to continue or control+c to abort. " continue
fi

sudo cat << EOF > "$xdgPath/pulse/client.conf"
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

# If there were no errors tell user to restart, else warn them errors happened.
if [ $? -eq 0 ]; then
echo "Configuration created succeswsfully, restart pulse, or your system, for changes to take affect."
else
echo "Errors were encountered while writing the configuration. please correct them manually."
fi
exit 0
