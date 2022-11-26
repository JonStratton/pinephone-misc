#!/bin/sh

run()
{
# If firefox is already running, new launches will just spawn off of running instance, and not run with proxychains.
if [ `ps -ef | grep 'firefox-esr' | grep -v 'grep' | wc -l` -ge 1 ]; then
   echo "Killing instance of running firefox"
   killall firefox-esr
fi

# Start tor and then run firefox with proxychains
sudo systemctl start tor
proxychains firefox-esr
sudo systemctl stop tor
}

install()
{
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tor proxychains4
sudo systemctl disable tor

# new group and sudo access to start and stop tor
sudo sh -c '( echo "Cmnd_Alias TORSTARTSTOP = /usr/bin/systemctl start tor, /usr/bin/systemctl stop tor
%tor-startstop ALL=NOPASSWD: TORSTARTSTOP" > /etc/sudoers.d/tor-startstop-sudoers )'
sudo groupadd tor-startstop
sudo usermod -a -G tor-startstop $USER

# Install self into bin
sudo cp $0 /usr/local/bin/

# GUI Launcher
sudo sh -c '( echo "[Desktop Entry]
Type=Application
Encoding=UTF-8
Name=Tor(ish) Browser
Comment=Tor(ish) Browser
Exec=/usr/local/bin/torish-browser.sh
Terminal=false
Categories=Tags;Describing;Application" > /usr/share/applications/torish-browser.desktop )'
}

uninstall()
{
sudo rm /usr/share/applications/torish-browser.desktop
sudo rm /usr/local/bin/torish-browser.sh
sudo groupdel tor-startstop
sudo rm /etc/sudoers.d/tor-startstop-sudoers
}

if [ $1 -a $1 = 'install' ]; then
   install
elif [ $1 -a $1 = 'uninstall' ]; then
   uninstall
else
   run
fi
