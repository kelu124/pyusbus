sudo echo "SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"04b4\", ATTRS{idProduct}==\"8613\", MODE=\"0666\", GROUP=\"dialout\"">/etc/udev/rules.d/99-healson.rules 
sudo echo "SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"04b4\", ATTRS{idProduct}==\"00f1\", MODE=\"0666\", GROUP=\"dialout\"">/etc/udev/rules.d/99-bmv.rules
sudo echo "SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"04b4\", ATTRS{idProduct}==\"1003\", MODE=\"0666\", GROUP=\"dialout\"">/etc/udev/rules.d/99-doppler.rules 
sudo udevadm control --reload-rules
sudo udevadm control --reload
sudo udevadm trigger 
