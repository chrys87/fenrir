#!/bin/sh
#output the ESSID and signal level
#needs iw (for iwconfig)
if [[ $(nmcli device wifi | wc -l ) -ge 2  ]]; then
    echo "Signal $(nmcli -f IN-USE,SIGNAL device wifi | grep "*" | tail -n1  | cut -f 2 -d '*') %"
    echo "Name $(nmcli -f IN-USE,SSID device wifi | grep "*" | tail -n1  | cut -f 2 -d '*') "
else
    echo "Leider keine Wlan verbindung $(whoami)"
fi
