#!/bin/bash

# This script configures pipewire to work both in the graphical environment and in the console with root apps.

if [[ $(whoami) != "root" ]]; then
# Get the current user's XDG_HOME
xdgPath="${XDG_CONFIG_HOME:-$HOME/.config}"
mkdir -p "$xdgPath/pipewire"
mkdir -p "$xdgPath/wireplumber/main.lua.d"
mkdir -p "$xdgPath/wireplumber/bluetooth.lua.d"

#create the file that tells the pipewire-pulse server to use a second socket located at /tmp/pulse.sock
# Warn user if we are going to overwrite an existing pipewire-pulse.conf
if [ -f "$xdgPath/pipewire/pipewire-pulse.conf" ]; then
    read -p "This will replace the current file located at $xdgPath/pipewire/pipewire-pulse.conf, press enter to continue or control+c to abort. " continue
fi
cat << "EOF" > "$xdgPath/pipewire/pipewire-pulse.conf"
# PulseAudio config file for PipeWire version "0.3.49" #
#
# Copy and edit this file in /etc/pipewire for system-wide changes
# or in ~/.config/pipewire for local changes.
#
# It is also possible to place a file with an updated section in
# /etc/pipewire/pipewire-pulse.conf.d/ for system-wide changes or in
# ~/.config/pipewire/pipewire-pulse.conf.d/ for local changes.
#

context.properties = {
    ## Configure properties in the system.
    #mem.warn-mlock  = false
    #mem.allow-mlock = true
    #mem.mlock-all   = false
    #log.level       = 2

    #default.clock.quantum-limit = 8192
}

context.spa-libs = {
    audio.convert.* = audioconvert/libspa-audioconvert
    support.*       = support/libspa-support
}

context.modules = [
    { name = libpipewire-module-rt
        args = {
            nice.level   = -11
            #rt.prio      = 88
            #rt.time.soft = -1
            #rt.time.hard = -1
        }
        flags = [ ifexists nofail ]
    }
    { name = libpipewire-module-protocol-native }
    { name = libpipewire-module-client-node }
    { name = libpipewire-module-adapter }
    { name = libpipewire-module-metadata }

    { name = libpipewire-module-protocol-pulse
        args = {
	    # contents of pulse.properties can also be placed here
	    # to have config per server.
        }
    }
]

# Extra modules can be loaded here. Setup in default.pa can be moved here
context.exec = [
    { path = "pactl"        args = "load-module module-always-sink" }
    { path = "pactl"        args = "load-module module-switch-on-connect" }
    #{ path = "/usr/bin/sh"  args = "~/.config/pipewire/default.pw" }
]

stream.properties = {
    #node.latency          = 1024/48000
    #node.autoconnect      = true
    #resample.quality      = 4
    #channelmix.normalize  = false
    #channelmix.mix-lfe    = false
    #channelmix.upmix      = true
    #channelmix.upmix-method = simple  # none, psd
    #channelmix.lfe-cutoff = 120
    #channelmix.fc-cutoff  = 6000
    #channelmix.rear-delay = 12.0
    #channelmix.stereo-widen = 0.1
    #channelmix.hilbert-taps = 0
}

pulse.properties = {
    # the addresses this server listens on
    server.address = [
        "unix:native"
        "unix:/tmp/pulse.sock"              # absolute paths may be used
        #"tcp:4713"                         # IPv4 and IPv6 on all addresses
        #"tcp:[::]:9999"                    # IPv6 on all addresses
        #"tcp:127.0.0.1:8888"               # IPv4 on a single address
        #
        #{ address = "tcp:4713"             # address
        #  max-clients = 64                 # maximum number of clients
        #  listen-backlog = 32              # backlog in the server listen queue
        #  client.access = "restricted"     # permissions for clients
        #}
    ]
    #pulse.min.req          = 256/48000     # 5ms
    #pulse.default.req      = 960/48000     # 20 milliseconds
    #pulse.min.frag         = 256/48000     # 5ms
    #pulse.default.frag     = 96000/48000   # 2 seconds
    #pulse.default.tlength  = 96000/48000   # 2 seconds
    #pulse.min.quantum      = 256/48000     # 5ms
    #pulse.default.format   = F32
    #pulse.default.position = [ FL FR ]
    # These overrides are only applied when running in a vm.
    vm.overrides = {
        pulse.min.quantum = 1024/48000      # 22ms
    }
}

# client/stream specific properties
pulse.rules = [
    {
        matches = [
            {
                # all keys must match the value. ~ starts regex.
                #client.name                = "Firefox"
                #application.process.binary = "teams"
                #application.name           = "~speech-dispatcher.*"
            }
        ]
        actions = {
            update-props = {
                #node.latency = 512/48000
            }
            # Possible quirks:"
            #    force-s16-info                 forces sink and source info as S16 format
            #    remove-capture-dont-move       removes the capture DONT_MOVE flag
            #quirks = [ ]
        }
    }
    {
        # skype does not want to use devices that don't have an S16 sample format.
        matches = [
             { application.process.binary = "teams" }
             { application.process.binary = "skypeforlinux" }
        ]
        actions = { quirks = [ force-s16-info ] }
    }
    {
        # firefox marks the capture streams as don't move and then they
        # can't be moved with pavucontrol or other tools.
        matches = [ { application.process.binary = "firefox" } ]
        actions = { quirks = [ remove-capture-dont-move ] }
    }
    {
        # speech dispatcher asks for too small latency and then underruns.
        matches = [ { application.name = "~speech-dispatcher*" } ]
        actions = {
            update-props = {
                pulse.min.req          = 1024/48000     # 21ms
                pulse.min.quantum      = 1024/48000     # 21ms
            }
        }
    }
]
EOF

#Creates the file that tells pipewire not to suspend any sinks for all devices. This makes sure audio doesn't die after switching to the console.
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
      ["api.alsa.use-acp"] = true,
      ["api.acp.auto-profile"] = false,
      ["api.acp.auto-port"] = false,
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

#Creates the file that disables the logind module for wireplumber which causes bluetooth to disconnect when switching tty
# Warn user if we are going to overwrite an existing 30-bluez-monitor.lua
if [ -f "$xdgPath/wireplumber/bluetooth.lua.d/30-bluez-monitor.lua" ]; then
    read -p "This will replace the current file located at $xdgPath/wireplumber/bluetooth.lua.d/30-bluez-monitor.lua, press enter to continue or control+c to abort. " continue
fi
echo 'bluez_monitor = {}
bluez_monitor.properties = {}
bluez_monitor.rules = {}

function bluez_monitor.enable()
  load_monitor("bluez", {
    properties = bluez_monitor.properties,
    rules = bluez_monitor.rules,
  })

end' > $xdgPath/wireplumber/bluetooth.lua.d/30-bluez-monitor.lua

echo "Please ensure that your user is added to the audio group."
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
