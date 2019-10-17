#!/bin/bash
# clilauncher.sh
# Description: Launches xterm with give application and fenrir.
#
# Copyright 2019, F123 Consulting, <information@f123.org>
# Copyright 2019, Storm Dragon, <storm_dragon@linux-a11y.org>
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3, or (at your option) any later
# version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this package; see the file COPYING.  If not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
#--code--
 
if [[ $# -lt 1 ]]; then
    echo "Usage: $0 program to launch args."
    exit 1
fi

# Make sure the program being launched exists
command -v "${1%% *}" &> /dev/null || exit 1

for i in /tmp/fenrirscreenreader-*.sock ; do
if [[ "$i" != "/tmp/fenrirscreenreader-deamon.sock" ]]; then
        echo -n "setting set screen#suspendingScreen=pty" | socat - UNIX-CLIENT:$i
    fi
done

#/usr/bin/urxvt -name "${1%% *}" -e fenrir -d -s /etc/fenrirscreenreader/settings/xterm.conf -o "general.shell=/usr/bin/${1%% *};remote#socketFile=/tmp/fenrirscreenreader-${1%% *}.sock"
/usr/bin/urxvt -name "${1%% *}" -e ../src/fenrir -d -s ./xterm.conf -o "general.shell=/usr/bin/${1%% *};remote#socketFile=/tmp/fenrirscreenreader-${1%% *}.sock"

