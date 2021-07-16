# TimeLapse
Python Script to run a TimeLapse Camera on a Raspberry Pi with PiCamera

## Installation
* Install the newest version of Raspbian on your SD-Card using for example [link to Raspbian Imager] (https://www.raspberrypi.org/software/)
* After succesful installation, a new Drive called "boot" should appear in your file manager. 
* Create a new file on this drive called "ssh" (be sure to remove the extension .txt)
* Copy the file "wpa_supplicant.conf" located in install_files to the boot drive and insert your WLAN SSID and password in the respective fields.

* Now, insert the micro SD card into your Pi and boot it up. After the successful boot open a terminal (in an ssh client that can enable X11 forwarding)

´git clone https://github.com/Chris-P-B4con/TimeLapse.git´
´cd TimeLapse´
´bash install_files/install_dependencies.sh´

Follow the instructions in the terminal, this could take a few minutes.