#!/bin/bash
#Basic install script for Fenrir.
read -p "This will install Fenrir. Press ctrl+C to cancel, or enter to continue." continue

# Fenrir main application
install -m755 -d /opt/fenrir
cp -af src/fenrir/* /opt/fenrir
install -m644 -D "autostart/systemd/fenrir.service" /usr/lib/systemd/system/fenrir.service
ln -fs /opt/fenrir/fenrir-daemon /usr/bin/fenrir-daemon
ln -fs /opt/fenrir/fenrir /usr/bin/fenrir
# tools
install -m755 -d /usr/share/fenrir/tools
cp -af tools/* /usr/share/fenrir/tools

# scripts
install -m755 -d /usr/share/fenrir/scripts
cp -af "config/scripts/wlan__-__key_y.sh" /usr/share/fenrir/scripts/

# keyboard
install -m644 -D "config/keyboard/desktop.conf" /etc/fenrir/keyboard/desktop.conf
install -m644 -D "config/keyboard/laptop.conf" /etc/fenrir/keyboard/laptop.conf

# punctuation
install -m755 -d /etc/fenrir/punctuation 
cp -af config/punctuation/* /etc/fenrir/punctuation 

# sound
install -d /usr/share/sounds/fenrir
cp -af config/sound/default /usr/share/sounds/fenrir/default
cp -af config/sound/default-wav /usr/share/sounds/fenrir/default-wav
cp -af config/sound/template /usr/share/sounds/fenrir/template

# config
if [ -f "/etc/fenrir/settings/settings.conf" ]; then
    echo "Do you want to overwrite your current global settings? (y/n)"
    read yn
    if [ $yn = "Y" -o $yn = "y" ]; then
      mv /etc/fenrir/settings/settings.conf /etc/fenrir/settings/settings.conf.bak
      echo "Your old settings.conf has been backed up to settings.conf.bak."
      install -m644 -D "config/settings/settings.conf" /etc/fenrir/settings/settings.conf
    else
      install -m644 -D "config/settings/settings.conf" /etc/fenrir/settings/settings.conf.current    
    fi
else
    install -m644 -D "config/settings/settings.conf" /etc/fenrir/settings/settings.conf    
fi    


# end message
cat << EOF
Installation complete.
install path:/opt/fenrir
settings path:/etc/fenrir

To test Fenrir
sudo systemctl start fenrir
To have Fenrir start on system boot:
sudo systemctl enable fenrir

Pulseaudio users may want to run
/usr/share/fenrir/tools/configure_pulse.sh
once from their user account, then once from the root.
EOF
