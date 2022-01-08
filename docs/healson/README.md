Tests
```
sudo modprobe usbmon
sudo setfacl -m u:$USER:r /dev/usbmon*
sudo mount -t debugfs none /sys/kernel/debug
more /dev/usbmon2
wireshark 
```

