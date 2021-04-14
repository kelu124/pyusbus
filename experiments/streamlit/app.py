import streamlit as st
from streamlit import caching

caching.clear_cache()

import struct
import pyusbus as usbProbe
import numpy as np
import time
import cv2
import scipy.misc

st.write("pyubus version:",usbProbe.__version__)


image_zone = st.empty()

probe = usbProbe.UP20()
probe.unfreeze()

while True: 
    IMG = []
    k = 0
    probe.unfreeze()
    while k < 40:
        tple = struct.unpack( '<2048H', probe.device.bulk_read(0x86,4096) ) 
        my_array = np.array( tple, dtype=np.int )
        IMG.append(my_array)
        k += 1
    NPts =np.shape(IMG)[0]*np.shape(IMG)[1]
    #st.write(np.shape(IMG)[0],np.shape(IMG)[1],NPts,len(IMG))
    IMG = np.array( IMG, dtype=np.int )
    IMG = np.array(254*IMG/np.max(IMG), dtype = np.uint8 )
    IMG = IMG.reshape((NPts//160, 160))
    rgb = cv2.cvtColor(IMG, cv2.COLOR_GRAY2BGR)
    res = cv2.resize(rgb, dsize=(440, 500), interpolation=cv2.INTER_CUBIC)
    image_zone.image(res)
    #probe.freeze()
