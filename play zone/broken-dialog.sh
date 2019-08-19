#!/bin/bash
# Script Functions
# Useful stuff for getting keypresses, or doing repetitive taks
#
# Copyright 2018, F123 Consulting, <information@f123.org>
# Copyright 2018, Storm Dragon, <storm_dragon@linux-a11y.org>
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

# Get the coluns and lines of the "screen"
cols=$(tput cols)
lines=$(tput lines)
# Settings to improve accessibility of dialog.
export DIALOGOPTS='--insecure --no-lines --visit-items'

menulist() {
    # Args: minimum group 2, multiples of 2, "tag" "choice"
    # returns: selected tag
    local menuList
    ifs="$IFS"
    #IFS=$'\n'
    dialog --backtitle "$(gettext "Use the up and down arrow keys to find the option you want, then press enter to select it.")" \
        --clear \
        --visit-items \
	--menu "$(gettext "Please select one")" 0 0 0 $@ --stdout
    #IFS="$ifs"
}

x="$(menulist "apple" "apple" "banana" "banana" "orange" "orange" "strawberry" "strawberry" "watermellon" "watermellon" "pineapple" "pineapple")"

echo "$x"

exit 0
