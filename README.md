[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/G2G81MT0G)


# pyusbus Readme

## Objective

The objective for this lib is be able to get images from USB probes easily, under python, in a user-friendly API, getting images in 3 lines of code.

```python
import pyusbus as usbProbe
probe = usbProbe.UP20() 
frames = probe.getImages(n=10) # should give you a loop of 10 frames
```

## Result

First series on a vein phantom, second on my forearm. Still some work around image compression / dynamic range adjustments.
 
![](/experiments/streamlit/capture.gif)

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
  * [Initial Jupyter notebook](/experiments/20210325-UP20L_init.ipynb)
  * Init Convex

* the `pyusbus` folder contains the python API.


# Changelog

* v0.0.2:
  * Solved an issue with incomplete images with UP20
  * Adding a streamlit interface - to be improved.
  * (hopefully) solved a bug with base64.decode leading to incorrect padding. 
* v0.0.1: Inital release
  * Initial config. Works for UP20 probe, yielding enveloppe.
  * Also added a Convex probe, which yields RF signals.
  * Adding [Convex pictures of a phantom](/probes/CONV/)
  * saveImage added to UP20 with correct mm markers

# Todo

* __High priority__
  * Explore content of [arrays](/experiments/payloads/) for both UP20 and Convex
  * Add correct ratios for images
  * Create gifs from loops
* __Medium__
  * Improve documentation
  * Better get the APIs different options
  * Get to know the Convex configuration packets
  * Explore acquisitions timings (packets/lines/frames per sec)
* __Low__
  * Add the module under pip

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


