#!/bin/bash
#Basic uninstall script for fenrir.
cat << EOF
Fenrir is going to remove.
All scripts and settings will be lost.
EOF

# ask
read -p "This will remove fenrir and settings. Press ctrl+c to cancel, or enter to continue." continue

# do it
unlink /usr/bin/fenrir
unlink /usr/bin/fenrir-daemon
rm -r /opt/fenrir
rm -r /usr/share/fenrir
rm -r /etc/fenrir
rm -r /usr/share/sounds/fenrir
rm /usr/lib/systemd/system/fenrir.service

# success message
cat << EOF
Fenrir has been successfully removed from your system.
EOF
