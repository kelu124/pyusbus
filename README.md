[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/G2G81MT0G)


# pyusbus Readme



# General setup
 
## Ubuntu goodies

```
sudo usermod -a -G uucp $USER
sudo usermod -a -G dialout $USER
sudo echo "SUBSYSTEM==\"usb\", ATTR{idVendor}==\"04B4\", ATTR{idProduct}==\"8613\", MODE=\"666\"">/etc/udev/rules.d/99-healson.rules 
```

# Contents

* Experiments contains .. experiments
* Module contains python API.


# Changelog


* v0.0.1: Inital release
  * Initial config.

# License

```
    pyusbus is a python API to access usb ultrasound probes
    Copyright (C) 2021 Luc Jonveaux

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
```


