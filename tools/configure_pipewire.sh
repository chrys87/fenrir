#!/bin/bash

# This script configures pipewire to work both in the graphical environment and in the console with root apps.

if [[ $(whoami) != "root" ]]; then
# Get the current user's XDG_HOME
xdgPath="${XDG_CONFIG_HOME:-$HOME/.config}"
mkdir -p "$xdgPath/pipewire/pipewire-pulse.conf.d"
mkdir -p "$xdgPath/wireplumber/main.lua.d"
# Warn user if we are going to overwrite an existing 10-console_audio.conf
if [ -f "$xdgPath/pipewire/pipewire-pulse.conf.d/10-console_audio.conf" ]; then
    read -p "This will replace the current file located at $xdgPath/pipewire/pipewire-pulse.conf.d/10-console_audio.conf, press enter to continue or control+c to abort. " continue
fi
echo 'context.modules = [
{ name = libpipewire-module-protocol-pulse
        args = {
server.address = [
                    "unix:/tmp/pulse.sock"
]
        }
}
]
context.exec = [
    { path = "pactl"        args = "load-module module-switch-on-connect" }
]' > $xdgPath/pipewire/pipewire-pulse.conf.d/10-console_audio.conf

# Warn user if we are going to overwrite an existing 50-do-not-suspend.lua
if [ -f "$xdgPath/wireplumber/main.lua.d/50-do-not-suspend.lua" ]; then
    read -p "This will replace the current file located at $xdgPath/wireplumber/main.lua.d/50-do-not-suspend.lua, press enter to continue or control+c to abort. " continue
fi
echo 'alsa_monitor.rules = {
  {
    matches = {
      {
                { "device.name", "matches", "alsa_card.*" },
      },
    },
   apply_properties = {
["session.suspend-timeout-seconds"] = 0
    },
  },
  {
    matches = {
      {        
        { "node.name", "matches", "alsa_input.*" },
      },
      {
        { "node.name", "matches", "alsa_output.*" },
      },
    },
    apply_properties = {
      ["session.suspend-timeout-seconds"] = 0
    },
  },
}' > $xdgPath/wireplumber/main.lua.d/50-do-not-suspend.lua

echo "If you have not yet done so, please run this script as root to write the client.conf file."
else
# This section does the root part:
xdgPath="/root/.config"
mkdir -p "$xdgPath/pulse"

# Warn user if we are going to overwrite an existing default.pa
if [ -f "$xdgPath/pulse/default.pa" ]; then
    read -p "This will replace the current file located at $xdgPath/pulse/default.pa, press enter to continue or control+c to abort. " continue
fi

cat << EOF > "$xdgPath/pulse/client.conf"
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
echo "If you have not yet done so, run this script as your normal user to write the user configs"
fi

# If there were no errors tell user to restart, else warn them errors happened.
if [ $? -eq 0 ]; then
echo "Configuration created successfully, please restart both Pipewire-pulseaudio and Wireplumber or your system, for changes to take affect."
else
echo "Errors were encountered whilst writing the configuration, please correct them manually."
fi
exit 0
