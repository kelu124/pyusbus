sudo echo "SUBSYSTEM==\"usb\", ATTR{idVendor}==\"04B4\", ATTR{idProduct}==\"8613\", MODE=\"666\"">/etc/udev/rules.d/99-healson.rules 
sudo echo "SUBSYSTEM==\"usb\", ATTR{idVendor}==\"04B4\", ATTR{idProduct}==\"0x00f1\", MODE=\"666\"">/etc/udev/rules.d/99-bmv.rules

sudo echo "SUBSYSTEM==\"usb\", ATTR{idVendor}==\"04B4\", ATTR{idProduct}==\"1003\", MODE=\"666\"">/etc/udev/rules.d/99-doppler.rules 
sudo udevadm control --reload-rules
sudo udevadm control --reload
sudo udevadm trigger 
