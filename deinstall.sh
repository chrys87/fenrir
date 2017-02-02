#!/bin/bash
#Basic install script for fenrir.
cat << EOF
fenrir is going to remove.
every script and settings are lost.
EOF
read -p "This will remove fenrir and settings. Press ctrl+c to cancil, or enter to continue." continue
rm -r /opt/fenrir
rm -r /usr/share/fenrir
rm -r /etc/fenrir
rm -r /usr/share/sounds/fenrir

unlink /usr/bin/fenrir
cat << EOF
fenrir is removed
EOF
