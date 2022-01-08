
# Probes: Convex

## What

```
dev = usb.core.find(idVendor=0x04B4, idProduct=0x00f1)
self.nL = 80   #np lines per frame
self.nP = 3900 #nb pts per line
```

## Descriptor

```
config 0
Interfaces 1
0
  CONFIGURATION 1: 100 mA ==================================
   bLength              :    0x9 (9 bytes)
   bDescriptorType      :    0x2 Configuration
   wTotalLength         :   0x3c (60 bytes)
   bNumInterfaces       :    0x1
   bConfigurationValue  :    0x1
   iConfiguration       :    0x0 
   bmAttributes         :   0x80 Bus Powered
   bMaxPower            :   0x32 (100 mA)
    INTERFACE 0: Vendor Specific ===========================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x0
     bAlternateSetting  :    0x0
     bNumEndpoints      :    0x6
     bInterfaceClass    :   0xff Vendor Specific
     bInterfaceSubClass :    0x0
     bInterfaceProtocol :    0x0
     iInterface         :    0x0 
      ENDPOINT 0x1: Bulk OUT ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x1 OUT
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
      ENDPOINT 0x81: Bulk IN ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x81 IN
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
      ENDPOINT 0x2: Bulk OUT ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x2 OUT
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
      ENDPOINT 0x82: Bulk IN ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x82 IN
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
      ENDPOINT 0x3: Bulk OUT ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x3 OUT
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
      ENDPOINT 0x83: Bulk IN ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x83 IN
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
      ENDPOINT 0x1: Bulk OUT ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x1 OUT
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
 === EPIN ===
      ENDPOINT 0x81: Bulk IN ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x81 IN
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
 === EPOUT ===
      ENDPOINT 0x1: Bulk OUT ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x1 OUT
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
```

### Booting

```
['Init1',
 'Init2',
 'Init3',
 'Init4',
 'Init5',
 'Init6',
 'Seq1.3',
 'Seq1.4bis',
 'Seq1.5',
 'Seq1.6',
 'Seq1.7',
 'TGC-related-TBC',
 'PreInitBoot1',
 'PreInitBoot2',
 'Init2',
 'PreInitBoot3',
 'PreInitBoot4',
 'Seq1.1',
 'Seq1.2',
 'Seq1.3',
 'Seq1.4',
 'Seq1.5',
 'Seq1.6',
 'Seq1.7',
 'Seq1.1',
 'Seq1.2',
 'Seq1.3',
 'Seq1.4',
 'Seq1.5',
 'Seq1.6',
 'Seq1.7',
 'Seq1.1',
 'Seq1.2',
 'Seq1.3',
 'Seq1.4',
 'Seq1.5',
 'Seq1.6',
 'Seq1.7',
 'StopAcq-TBC']
```

### Changing depth

Sequences:

```
 'Depth1',
 'ConfirmDepth1.1',
 'Seq1.3',
 'ConfirmDepth1.2',
 'Seq1.5',
 'Seq1.6',
 'Seq1.7',

'Depth2',
 'ConfirmDepth1.1',
 'Seq1.3',
 'ConfirmDepth1.2',
 'Seq1.5',
 'Seq1.6',
 'Seq1.7',

'Depth3',
 'ConfirmDepth2.1',
 'Seq1.3',
 'ConfirmDepth2.2',
 'Seq1.5',
 'Seq1.6',
 'Seq1.7',


'Depth4',
 'ConfirmDepth1.3',
 'Seq1.3',
 'ConfirmDepth1.2',
 'Seq1.5',
 'Seq1.6',
 'Seq1.7',

'Depth5',
 'ConfirmDepth5.1',
 'Seq1.3',
 'ConfirmDepth5.2',
 'Seq1.5',
 'Seq1.6',
 'Seq1.7',
 ```


## All

####  ./onoff.pcapng.parquet 

['Init1', 'Init2', 'Init3', 'Init4', 'Init5', 'Init6', 'Seq1.3', 'Seq1.4bis', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'TGC-related-TBC-StartMaybe', 'PreInitBoot1', 'PreInitBoot2', 'Init2', 'PreInitBoot3', 'PreInitBoot4', 'Seq1.1', 'Seq1.2', 'Seq1.3', 'Seq1.4', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Seq1.1', 'Seq1.2', 'Seq1.3', 'Seq1.4', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Seq1.1', 'Seq1.2', 'Seq1.3', 'Seq1.4', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'StopAcq-TBC']

####  ./diff_tgc2.pcapng.parquet 

['TGC-related-TBC-StartMaybe', 'StopAcq-TBC']

####  ./diff_tgc.pcapng.parquet 

['TGC-related-TBC-StartMaybe', 'StopAcq-TBC']

####  ./diff_gains.pcapng.parquet 

['TGC-related-TBC-StartMaybe', 'StopAcq-TBC']

####  ./diff_depth.pcapng.parquet 

['TGC-related-TBC-StartMaybe', 'Depth1', 'ConfirmDepth1.1', 'Seq1.3', 'ConfirmDepth1.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth1', 'ConfirmDepth1.1', 'Seq1.3', 'ConfirmDepth1.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth2', 'ConfirmDepth1.1', 'Seq1.3', 'ConfirmDepth1.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth2', 'ConfirmDepth1.1', 'Seq1.3', 'ConfirmDepth1.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth3', 'ConfirmDepth2.1', 'Seq1.3', 'ConfirmDepth2.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth3', 'ConfirmDepth2.1', 'Seq1.3', 'ConfirmDepth2.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth4', 'ConfirmDepth1.3', 'Seq1.3', 'ConfirmDepth1.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth4', 'ConfirmDepth1.3', 'Seq1.3', 'ConfirmDepth1.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth2', 'ConfirmDepth1.1', 'Seq1.3', 'ConfirmDepth1.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth2', 'ConfirmDepth1.1', 'Seq1.3', 'ConfirmDepth1.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth1', 'ConfirmDepth1.1', 'Seq1.3', 'ConfirmDepth1.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth1', 'ConfirmDepth1.1', 'Seq1.3', 'ConfirmDepth1.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth0', 'ConfirmDepth1.1', 'Seq1.3', 'ConfirmDepth1.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth0', 'ConfirmDepth1.1', 'Seq1.3', 'ConfirmDepth1.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Seq1.1', 'Seq1.2', 'Seq1.3', 'Seq1.4', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Seq1.1', 'Seq1.2', 'Seq1.3', 'Seq1.4', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth5', 'ConfirmDepth5.1', 'Seq1.3', 'ConfirmDepth5.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'Depth5', 'ConfirmDepth5.1', 'Seq1.3', 'ConfirmDepth5.2', 'Seq1.5', 'Seq1.6', 'Seq1.7', 'StopAcq-TBC']
