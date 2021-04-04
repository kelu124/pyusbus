[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/G2G81MT0G)


# pyusbus Readme

## Objective

The objective for this lib is be able to get images from USB probes easily, under python, in a user-friendly API, getting images in 3 lines of code.

```python
import pyusbus as usbProbe
probe = usbProbe.HealsonUP20() 
frames = probe.getImages(n=50) # should give you a loop of 50 frames
```

## Result

![](/experiments/images/first.gif)

## Installation

You can use the `build.sh` and `install.sh` scripts to prepare your module. Hopefully soon to come under pip.

# General setup
 
Need to work on the documentation here.

## Ubuntu adjustements

```
sudo usermod -a -G uucp $USER
sudo usermod -a -G dialout $USER
sudo echo "SUBSYSTEM==\"usb\", ATTR{idVendor}==\"04B4\", ATTR{idProduct}==\"8613\", MODE=\"666\"">/etc/udev/rules.d/99-healson.rules 
```

# Contents

* the `experiments` folder contains .. experiments.
  * [Initial Jupyter notebook](/experiments/20210325-InitialTest.ipynb)
* the `pyusbus` folder contains the python API.


# Changelog


* v0.0.1: Inital release
  * Initial config. Works for Healson UP20 probe.

# Todo

* Add the module under pip
* Improve documentation
* Explore content of [arrays](/pyusbus/config_arrays.py)
* Get some images on a phantom


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


