#!/bin/bash
#Basic install script for fenrir.
read -p "This will install fenrir. Press ctrl+c to cancil, or enter to continue." continue

# fenrir main application
install -m755 -d /opt/fenrir
cp -a src/fenrir/* /opt/fenrir
install -m644 -D "autostart/systemd/fenrir.service" /usr/lib/systemd/system/fenrir.service
ln -s /opt/fenrir/fenrir-daemon /usr/bin/fenrir

# tools
install -m755 -d /usr/share/fenrir/tools
cp -a tools/* /usr/share/fenrir/tools

# scripts
install -m755 -d /usr/share/fenrir/scripts
cp -a "config/scripts/wlan__-__key_y.sh" /usr/share/fenrir/scripts/


install -m755 -d /etc/fenrir/punctuation 
cp -a config/punctuation/* /etc/fenrir/punctuation 

# sound
install -d /usr/share/sounds/fenrir
cp -a config/sound/default /usr/share/sounds/fenrir/default
cp -a config/sound/default-wav /usr/share/sounds/fenrir/default-wav
cp -a config/sound/template /usr/share/sounds/fenrir/template

# config
if [ -f "/etc/fenrir/keyboard/desktop.conf" ]; then
    echo "Do you want overwrite the desktop keyboard layout? (y/n)"
    read yn
    if [ $yn = "Y" -o $yn = "y"];
    then
        install -m644 -D "config/keyboard/desktop.conf" /etc/fenrir/keyboard/desktop.conf
    fi
fi

if [ -f "/etc/fenrir/keyboard/laptop.conf" ]; then
    echo "Do you want overwrite the laptop keyboard layout? (y/n)"
    read yn
    if [ $yn = "Y" -o $yn = "y"];
    then
        install -m644 -D "config/keyboard/laptop.conf" /etc/fenrir/keyboard/laptop.conf
    fi
fi
if [ -f "config/settings/settings.conf" ]; then
    echo "Do you want overwrite your current settings? (y/n)"
    read yn
    if [ $yn = "Y" -o $yn = "y"];
    then
      install -m644 -D "config/settings/settings.conf" /etc/fenrir/settings/settings.conf
    fi
fi


# end message
cat << EOF
To test fenrir
sudo systemctl start fenrir
To have fenrir start at boot:
sudo systemctl enable fenrir
Pulseaudio users may want to run
/usr/share/fenrir/tools/configure-pulseaudio
once as their user account and once as root.
EOF
