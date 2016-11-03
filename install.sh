#!/bin/bash
#Basic install script for fenrir.
read -p "This will install fenrir. Press ctrl+c to cancil, or enter to continue." continue
install -m755 -d /opt/fenrir
 install -m755 -d /usr/share/fenrir/scripts
 install -m644 -D "config/keyboard/desktop.conf" /etc/fenrir/keyboard/desktop.conf
 install -m644 -D "config/keyboard/desktop.conf" /etc/fenrir/keyboard/desktop.conf
 install -m644 -D "config/punctuation/default.conf" /etc/fenrir/punctuation/default.conf
 install -m644 -D "config/settings/settings.conf" /etc/fenrir/settings/settings.conf
 install -d /usr/share/sounds/fenrir
  install -m644 -D "autostart/systemd/fenrir.service" /usr/lib/systemd/system/fenrir.service
  cp -a src/fenrir/* /opt/fenrir
  cp -a config/scripts/* /usr/share/fenrir/scripts
  cp -a config/sound/* /usr/share/sounds/fenrir
ln -s /opt/fenrir/fenrir-daemon /usr/bin/fenrir
cat << EOF
To have fenrir start at boot:
sudo systemctl enable fenrir
Pulseaudio users may want to run
/usr/share/fenrir/tools/configure-pulseaudio
once as their user account and once as root.
EOF
