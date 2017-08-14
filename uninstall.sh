#!/bin/bash
#Basic uninstall script for Fenrir.
cat << EOF
Fenrir is going to remove.
All scripts and settings will be lost.
EOF

# ask
read -p "This will remove Fenrir and its settings from your system,, press ctrl+C to cancel, or enter to continue." continue

# do it
unlink /usr/bin/fenrir
unlink /usr/bin/fenrir-daemon
rm -rf /opt/fenrir
rm -rf /usr/share/fenrir
rm -rf /etc/fenrir
rm -rf /usr/share/sounds/fenrir
rm -f /usr/lib/systemd/system/fenrir.service

# success message
cat << EOF
Fenrir has been successfully removed from your system.
EOF
