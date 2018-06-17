#!/bin/bash
#Basic install script for Fenrir.
read -p "This will install Fenrir. Press ctrl+C to cancel, or enter to continue." continue

# Fenrir main application
install -m755 -d /opt/fenrirscreenreader
cp -af src/* /opt/fenrirscreenreader

ln -fs /opt/fenrirscreenreader/fenrir-daemon /usr/bin/fenrir-daemon
ln -fs /opt/fenrirscreenreader/fenrir /usr/bin/fenrir
# tools
install -m755 -d /usr/share/fenrirscreenreader/tools
cp -af tools/* /usr/share/fenrirscreenreader/tools

# scripts
install -m755 -d /usr/share/fenrirscreenreader/scripts
cp -af "config/scripts/wlan__-__key_y.sh" /usr/share/fenrirscreenreader/scripts/

# keyboard
install -m644 -D "config/keyboard/desktop.conf" /etc/fenrirscreenreader/keyboard/desktop.conf
install -m644 -D "config/keyboard/laptop.conf" /etc/fenrirscreenreader/keyboard/laptop.conf

# punctuation
install -m755 -d /etc/fenrirscreenreader/punctuation 
cp -af config/punctuation/* /etc/fenrirscreenreader/punctuation 

# sound
install -d /usr/share/sounds/fenrirscreenreader
cp -af config/sound/default /usr/share/sounds/fenrirscreenreader/default
cp -af config/sound/template /usr/share/sounds/fenrirscreenreader/template

# config
if [ -f "/etc/fenrirscreenreader/settings/settings.conf" ]; then
    echo "Do you want to overwrite your current global settings? (y/n)"
    read yn
    if [ $yn = "Y" -o $yn = "y" ]; then
      mv /etc/fenrirscreenreader/settings/settings.conf /etc/fenrirscreenreader/settings/settings.conf.bak
      echo "Your old settings.conf has been backed up to settings.conf.bak."
      install -m644 -D "config/settings/settings.conf" /etc/fenrirscreenreader/settings/settings.conf
    else
      install -m644 -D "config/settings/settings.conf" /etc/fenrirscreenreader/settings/settings.conf.current    
    fi
else
    install -m644 -D "config/settings/settings.conf" /etc/fenrirscreenreader/settings/settings.conf    
fi    


# end message
cat << EOF
Installation complete.
install path:/opt/fenrirscreenreader
settings path:/etc/fenrirscreenreader

To test Fenrir
sudo systemctl start fenrir
To have Fenrir start on system boot:
sudo systemctl enable fenrir

Pulseaudio users may want to run
/usr/share/fenrirscreenreader/tools/configure_pulse.sh
once from their user account, then once from the root.
EOF
