
echo "Installing Dependencies..."
sudo apt-get -qq update && sudo apt-get -qq upgrade
pip install pathlib
sudo apt-get -qq install -y git python-picamera
sudo apt-get -qq install -y screen
sudo apt-get -qq install -y rclone

echo "Configuring automatic script run on startup"
cd TimeLapse
sudo mv TimeLapse.startup /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable timelapse

echo "Configuring RPi Power consumption"
sudo echo "over_voltage=4" >> /boot/config.txt
sudo echo "force_turbo=1" >> /boot/config.txt

echo "Enable the Raspberry PI camera. Afterwards exit raspi-config"
sudo raspi-config

echo "Configure rclone"
rclone config