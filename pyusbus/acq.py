#USB
import usb.core
import usb.util
from fx2 import FX2Config,FX2Device
# Figures
import numpy as np
# Utilities
import json
import base64
import struct
import time 
import matplotlib.pyplot as plt
import cv2

from pyusbus.confUP20L import healson_config
from pyusbus.confCONV  import cvx
from pyusbus.confInterson import lP, lV, initIntReq, initIntVal

def findProbe():
    if usb.core.find(idVendor=0x04B4, idProduct=0x8613):
        return "UP20"
    if usb.core.find(idVendor=0x04B4, idProduct=0x00f1):
        return "CONVEX"
    if usb.core.find(idVendor=0x1921, idProduct=0x0001):
        return "Interson, not programmed"
    if usb.core.find(idVendor=0x1921, idProduct=0xf001):
        # 0xf001 seems to indicate serial, analogdevices?
        # gnICE+
        # https://wiki.analog.com/_media/resources/technical-guides/adispi_rev_1p0_customer.pdf
        return "Interson, programmed"
    return "No Device"

def arr2img(arr,x,y): # UP20L : (440, 500)
    bw = cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
    img = cv2.resize(bw, dsize=(440, 500), interpolation=cv2.INTER_CUBIC)
    return img


class Interson:
    # https://github.com/KitwareMedical/IntersonManager/blob/master/IntersonManager.cpp
    # Interesting doc on the registers
    def __init__(self):
        """Configure the FTDI interface. 
        """ 
        if    usb.core.find(idVendor=0x1921, idProduct=0x0001):
            self.progIt()
            time.sleep(5)

        self.dev = usb.core.find(idVendor=0x1921, idProduct=0xf001)
        if not self.dev: 
            print("No Device")
        else:
            for config in self.dev:  
                # The device was getting "Err 16 busy" on my ubuntu
                for i in range(config.bNumInterfaces):
                    if self.dev.is_kernel_driver_active(i):
                        self.dev.detach_kernel_driver(i) 
            self.dev.reset()

            try:
                self.dev.set_configuration()
            except:
                print("Already connected")
            self.EP = []
        
            for cfg in self.dev:
                for iface in cfg:
                    for ep in iface:
                        ep_dir = usb.util.endpoint_direction(ep.bEndpointAddress)
                        ep_type = usb.util.endpoint_type(ep.bmAttributes)
                        self.EP.append(ep)
                        #print(ep)
    
            try:
                self.dev.ctrl_transfer(bmRequestType=64,bRequest=187, wValue =0x0000)
                print("Working")
            except:
                print("Not working")

    def StartRun(self): # initIntReq, initIntVal
        for k in range(len(initIntReq)):
            bmR = int(initIntReq[k])
            wV = int(initIntVal[k])
            self.dev.ctrl_transfer(bmRequestType= 64,bRequest= bmR, wValue= wV, 
                                 wIndex= 0 , data_or_wLength=  "\x00\x00") 
        print("Starting..")
        return 1

    def startMotor(self):
        self.dev.ctrl_transfer(bmRequestType= 64,bRequest= 213, wValue= 0, wIndex= 0 , data_or_wLength=  "\x00\x00") # démarre le moteur
    def startAcq(self):
        self.dev.ctrl_transfer(bmRequestType= 64,bRequest= 208, wValue= 0, wIndex= 0 , data_or_wLength=  "\x00\x00") # démarre le moteur
    def stopMotor(self):
        self.dev.ctrl_transfer(bmRequestType= 64,bRequest= 214, wValue= 0, wIndex= 0 , data_or_wLength=  "\x00\x00") # démarre le moteur
    def stopAcq(self):
        self.dev.ctrl_transfer(bmRequestType= 64,bRequest= 209, wValue= 0, wIndex= 0 , data_or_wLength=  "\x00\x00") # démarre le moteur
    def fastMotor(self):
        # @todo discover what it does??
        self.dev.ctrl_transfer(bmRequestType= 64,bRequest= 187, wValue= 0, wIndex= 0 , data_or_wLength=  "\x00\x00") # démarre le moteur


    def getRawImages(self,n=1):
        dataOdd = []
        dataEven = []
        timings = []
        i = 0
        while i < n*12*20480//4096 : # @todo not so glamorous hardcoded values
            dataOdd.append(self.EP[1].read(4096))
            dataEven.append(self.EP[0].read(4096)) 
            timings.append(time.time())
            i += 1
        self.data = [dataOdd,dataEven]
        self.timings = [dataOdd,dataEven]
        return self.data


    def getImages(self,n=1):
        self.startMotor() 
        self.startAcq()
        self.getUSBImages(n)
        self.stopAcq()
        self.stopMotor()
        return 1

    def getUSBImages(self,n=1):
        # Using a single channel
        rawData = []
        timings = []
        i = 0
        while i < n*12*20480//4096 : 
            rawData.append(self.EP[1].read(4096)) 
            timings.append(time.time())
            i += 1
        self.rawData = rawData
        self.timings = timings
        return self.rawData      

    def progIt(self):
        dev = usb.core.find(idVendor=0x1921, idProduct=0x0001)
        if not dev: print("No Device")

        for config in dev:  
            # The device was getting "Err 16 busy" on my ubuntu
            for i in range(config.bNumInterfaces):
                if dev.is_kernel_driver_active(i):
                    dev.detach_kernel_driver(i)
                #print(i)
        dev.reset()

        try:
            dev.set_configuration()
        except:
            print("Already connected")

        for k in range(len(lV)): 
            dev.ctrl_transfer(bmRequestType= 64,bRequest= 160, wValue= lV[k], 
                                  wIndex= 0 , data_or_wLength=  lP[k])


####
#### Starting the Healson linear probe
####

class UP20:

    def __init__(self):
        """Configure the FTDI interface. 
        """ 
        self.config = healson_config 
        self.payloads = {}
        for k in self.config.keys():
            self.payloads[k] = base64.b64decode(self.config[k][1:-1] + "========" )

        self.ARRAY = b'\x00'
        for k in range(64):
            self.ARRAY += b'\x00' 
            

        dev = usb.core.find(idVendor=0x04B4, idProduct=0x8613)
        if not dev: print("No Device") 
        c = 1
        for config in dev:
            #print('config', c)
            #print('Interfaces', config.bNumInterfaces)
            # The device was getting "Err 16 busy" on my ubuntu
            for i in range(config.bNumInterfaces):
                if dev.is_kernel_driver_active(i):
                    dev.detach_kernel_driver(i)
                #print(i)
            c+=1 
        dev.reset()
        try:
            dev.set_configuration()
        except:
            print("Already connected")

        self.conf = FX2Config()
        self.device = FX2Device() 
        self.InitOn() 
        self.InitSeries10() 
        self.InitArrays()
        self.InitRegisters()
        #print("Probe should be ready")

    def BulkOut(self,payload):
        # 
        return self.device.bulk_write(0x02, payload,timeout=None)

    def BulkIn(self,Length):
        # Receive from Bulk
        return self.device.bulk_read(0x86,Length)
                
    def ControlIn(self):
        return self.device.control_read(0x40, 184, 0, 0, 32,timeout=None)

    def ControlOut(self,request,value,index,length):
        return self.device.control_write( 0x40, request, value, index,self.ARRAY[:length],timeout=None )

    ## Inits

    def InitOneA(self,TwoBytes): #178 1 to 179 2
        self.ControlOut(178,1,0,16)
        self.BulkOut(TwoBytes)
        self.ControlOut(179,2,0,16)
        return self.BulkIn(512)

    def Read512(self):
        self.ControlOut(179,1,0,16)
        return struct.unpack( '<512B', self.BulkIn(512) )

    def BulkOutTwo(self,Two):
        self.ControlOut(178,1,0,16)
        self.BulkOut(Two)

    def BulkOutTwo512(self,Two):
        self.ControlOut(178,1,0,16)
        self.BulkOut(Two)
        return self.Read512() 

    def BulkOutFour(self,Four):
        self.ControlOut(178,2,0,16)
        self.BulkOut(Four)
        
    def BulkOutLarge(self,Large):
        self.ControlOut(178,2,0,16)
        if len(Large)<=4096:
            self.BulkOut(Large)
        else:
            NPackets = len(Large)//4096 
            for k in range(NPackets+1):
                if len(Large[4096*k:]) >= 4096:
                    #print(k,len(Large[4096*k:4096*(k+1)]))
                    self.BulkOut(Large[4096*k:4096*(k+1)])
                else:
                    if len(Large[4096*k:]):
                        #print(k,len(Large[4096*k:]))
                        self.BulkOut(Large[4096*k:])
            
    def readWrite(self,command):
        # Used to write something somewhere, and check if the reply is identical 
        self.BulkOutTwo(command) 
        return self.BulkOutTwo512(b'\xff'+command[0:1])

    def Init1004(self,FourBytes):
        self.BulkOutTwo(b'\x10\x04')
        self.BulkOutFour(FourBytes)
        return 1

    ## Init facility
        
    def InitOn(self):                # 
        self.ControlIn()             # Checks name of the probe
        self.InitOneA(b'\x10\x0e')   # 
        self.ControlOut(179,2,0,16)
        self.ControlIn()             # Checks name of the probe
        self.BulkOutTwo(b'\xff\x06') # 113 to 119
        
    def InitSeries10(self):               
        # What would we have here ?
        # 10x04
        for k in [b'\x01\x00\x00\x0f',
                  b' \x00\x03\x0f'   ,
                  b'\x00\x00\x03\x0f',
                  b'\xe3\x00\x16\x0f', 
                  b'\xff\x00\x14\x0f',
                  b'\xc5\x80B\x0f'   ,
                  b'\x0c\x82F\x0f'    ]:
            self.Init1004(k)
        
    def InitArrays(self):                    # Pas de 2, 3, 11
        
        # Array setup ?                        # Array 0, 960B
        self.BulkOutTwo(b'\x10\x00')         # Command n255
        self.BulkOutLarge(self.payloads["259"])   # 960-element array. 6*160. Delays ?
        
        self.BulkOutTwo(b'\x10\x05')         # Array 5, 16k pts - 128*64, ('<'+str(L//2)+'h' )
        self.BulkOutLarge(self.payloads["279"])   # Interesting ?
        
        self.BulkOutTwo(b'\x10\x06')         # Array 6, 16k pts, assez ressemblant au packet passé
        self.BulkOutLarge(self.payloads["293"])   # 
        
        self.BulkOutTwo(b'\x10\x03')         # Array 3, 256 elements
        self.BulkOutLarge(self.payloads["307"])   # filter, or gate -- '>'+str(L//8)+'Q'
        
        self.BulkOutTwo(b'\x10\x0c')         # Array 12, 16384 - doubling sequence, full of 0es
        self.BulkOutLarge(self.payloads["315"])   # --> Seems like the only good vals are until [:2*80*64] (10240)
        
        self.BulkOutTwo(b'\x10\n')           # Array 10, 512 -- seems to contain SINCs.
        self.BulkOutLarge(self.payloads["329"])   # 

        self.BulkOutTwo(b'\x10\t')           # Array 9 - largest, 43904 (128*343, 10976*4, 2744*16). Why 343 ?
        self.BulkOutLarge(self.payloads["337"])   # 337 to 357

        # ATGC
        self.BulkOutTwo(b'\x10\x07')         # Array 7, 256
        self.BulkOutLarge(self.payloads["365"])   # Values match the ATGC values

        # DTGC
        self.BulkOutTwo(b'\x10\x08')         # Array 8, 512 elements --> set also via the TGC when programming
        self.BulkOutLarge(self.payloads["373"])   # Values match the dTGC values, up to a facteur 16
        
        
    def InitRegisters(self) :

        # Should guess what we have here
        self.readWrite(b'\x1b\x00') 
        
        self.readWrite(b'#\xe0') 
        self.readWrite(b'$\x01') 
        self.readWrite(b'%\xdf') 
        self.readWrite(b'&\x01')
        
        # These 3 should be for the depth, see 05.Depth/00.ProcessPCAPs.ipynb
        # for each depth change, the TGC values should be updated
        self.readWrite(b' \x04')    # 20
        # Normalement update de 1008 à ce moment (why?) -- 
        self.readWrite(b'+\xe9')    # 2b
        self.readWrite(b',\t')      # 2c
        # Next ?
        self.readWrite(b'\x1a\x06') 
        # Focus zone:
        self.readWrite(b'\x17\x01') # second parameter could be 0, 1, 2...

        # Next ?
        self.readWrite(b"'\x19")
        self.readWrite(b'(\x00')
        self.readWrite(b')|')  
        self.readWrite(b'*\x01')   
        self.readWrite(b'\x18\x01') 
        self.readWrite(b'@\x0b') 
        
        self.readWrite(b'A\x01') 
        
        self.readWrite(b'\x12\x01') 
        self.readWrite(b'\xfe\xaa')  
            
        self.ControlOut(182,0,0,16) ## 182, packet ID 515
        
    # Image acquisition

    def freeze(self):
        self.readWrite(b'\x11\x01') 

    def unfreeze(self):
        self.readWrite(b'\x11\x00')
        self.ControlOut(179,0,0,16) # Seems to start: without it, no acqs


    def getImages(self,n=1):
        IMG = self.DLImgs(n)
        NPts =np.shape(IMG)[0]*np.shape(IMG)[1]
        IMG = np.array( IMG, dtype=np.int )
        IMG = IMG.reshape((NPts//160, 160))
        images = []
        for k in range(n):
            images.append(IMG[512*k:512*(k+1)] )
        self.loop = images
        return images

    def saveImage(self,n=0):
        plt.figure(figsize=(8,8))
        plt.imshow(np.sqrt(np.abs(self.loop[n])),cmap=plt.cm.bone,extent=[0,44.4,50,0],aspect=1)  
        plt.title("UP20L: Image "+str(n))
        plt.savefig("up20l_"+str(n)+".jpg")
        return n

    def DLImgs(self,n=1):
        IMG = []
        timings = []
        self.unfreeze()
        k = 0
        while k < n*40:
            tple = struct.unpack( '<2048H', self.device.bulk_read(0x86,4096) ) 
            my_array = np.array( tple, dtype=np.int )
            IMG.append(my_array)
            timings.append(time.time()) # timings
            k += 1

        #self.freeze()
        self.timings = timings
        return IMG


    ## Facility 
    def checkAddress(self,address): 
        return self.checkAddressFull(address)[1:2]
    def checkAddressFull(self,address): 
        return [x for x in self.BulkOutTwo512(b'\xff'+address)]


### Going to the CONVEX



class Convex:

    def __init__(self):
        """
        Configure the USB interface 
        """ 

        self.nL = 80   #np lines per frame
        self.nP = 3900 #nb pts per line
        self.payloads = None
        self.payloads = cvx.copy()
        for k in self.payloads.keys():
            print(self.payloads[k][1:-1])
            self.payloads[k] = base64.b64decode(self.payloads[k][1:-1] + "========")          

        dev = usb.core.find(idVendor=0x04B4, idProduct=0x00f1)
        if not dev: print("No Device")

        c = 0
        for config in dev: 
            # The device was getting "Err 16 busy" on my ubuntu
            for i in range(config.bNumInterfaces):
                if dev.is_kernel_driver_active(i):
                    dev.detach_kernel_driver(i)
                print(i)
            c+=1 
        dev.reset()
        try:
            dev.set_configuration()
        except:
            print("Already connected") 
        

        cfg = dev.get_active_configuration()
        intf = cfg[(0,0)]

        self.EPOUT = usb.util.find_descriptor(
            intf,
            # match the first OUT endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)

        assert self.EPOUT is not None 


        cfg = dev.get_active_configuration()
        intf = cfg[(0,0)]

        self.EPIN = usb.util.find_descriptor(
            intf,
            # match the first OUT endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)

        assert self.EPIN is not None        
        self.dev = dev
        # Starting the configuration
        self.dev.ctrl_transfer(bmRequestType=0xc3,bRequest=176, wValue=0, wIndex= 0, data_or_wLength=  8)
        self.dev.ctrl_transfer(bmRequestType=0xc3,bRequest=187, wValue=3, wIndex= 0, data_or_wLength= 32)
        self.dev.ctrl_transfer(bmRequestType=0xc3,bRequest=187, wValue=3, wIndex=32, data_or_wLength= 32)
        self.dev.ctrl_transfer(bmRequestType=0xc3,bRequest=187, wValue=3, wIndex=64, data_or_wLength=  8)
        for k in self.payloads.keys():
            self.EPOUT.write(self.payloads[k]) 
        self.dev.ctrl_transfer(bmRequestType=0xc3,bRequest=187, wValue=3)
        # Aaaand it should be configured


    def getImages(self,n=1):
        nReads = self.nL*self.nP*(n+1)
        i = 0
        data = []
        timings = []
        while i < 2*nReads//4096: # 2 because we're reading 2bytes words
            data.append(self.EPIN.read(4096))
            i += 1
            timings.append(time.time())
        nData = data.copy()
        for k in range(len(data)):
            PL = bytes(bytearray(data[k]))
            nData[k] = np.array( struct.unpack( '<'+str(len(PL)//2)+'h', PL ) )
        nData = np.array(nData)
        allData = np.concatenate(nData, axis=None)
        self.raw = allData
        self.timings = timings
        return self.createLoop()
    

    def createLoop(self):
        lenImg = self.nL*self.nP
        newLine = [x[0] for x in np.argwhere(self.raw == np.amax(self.raw))]
        cntFrame = []
        cntNewFrame = []
        for x in newLine:
            if self.raw[x-1] == 0:
                cntFrame.append(self.raw[x+2]) # compteur de frame
                cntNewFrame.append(x)
                #print(x,self.raw[x+2])
        cntImg = []
        cntnPt = []
        for k in range(len(cntFrame)-1):
            if cntFrame[k] != cntFrame[k+1]:
                cntImg.append(cntFrame[k]) 
                cntnPt.append(cntNewFrame[k])
                print(cntFrame[k],cntNewFrame[k])
        self.cntImg = cntImg
        self.cntnPt = cntnPt
        self.newLine = newLine
        self.loop = []
        i = self.cntnPt[0]
        while i < len(self.raw) - lenImg:
            self.loop.append(self.raw[i:i+lenImg].reshape((self.nL, self.nP)))
            i += lenImg
        return self.loop

if __name__ == "__main__": 
    device = UP20()
    print("Connected to UP20.\nInit...")
    device.InitOn()
    print("Initialize series")
    device.InitSeries10()
    print("Preping arrays")
    device.InitArrays()
    print("Preping registers")
    device.InitRegisters()
