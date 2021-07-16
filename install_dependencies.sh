
echo "Installing Dependencies..."
pip install pathlib
sudo apt-get -qq install -y git python-picamera
sudo apt-get -qq install -y screen

echo "Getting source code..."
cd ~
git clone https://github.com/Chris-P-B4con/TimeLapse.git

echo "Configuring automatic script run on startup"
cd TimeLapse
sudo mv TimeLapse.startup /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable timelapse

echo "Configuring RPi Power consumption"
sudo echo "over_voltage=4" >> /boot/config.txt
sudo echo "force_turbo=1" >> /boot/config.txt