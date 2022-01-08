##


## Two phases:

1. gets programmed first
2. Can be used afterwards

## Exposed

config 0
Interfaces 1
0
  CONFIGURATION 1: 100 mA ==================================
   bLength              :    0x9 (9 bytes)
   bDescriptorType      :    0x2 Configuration
   wTotalLength         :   0xab (171 bytes)
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
     bNumEndpoints      :    0x0
     bInterfaceClass    :   0xff Vendor Specific
     bInterfaceSubClass :   0xff
     bInterfaceProtocol :   0xff
     iInterface         :    0x0 
    INTERFACE 0, 1: Vendor Specific ========================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x0
     bAlternateSetting  :    0x1
     bNumEndpoints      :    0x6
     bInterfaceClass    :   0xff Vendor Specific
     bInterfaceSubClass :   0xff
     bInterfaceProtocol :   0xff
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
      ENDPOINT 0x4: Bulk OUT ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x4 OUT
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
      ENDPOINT 0x86: Bulk IN ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x86 IN
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
      ENDPOINT 0x88: Bulk IN ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x88 IN
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
    INTERFACE 0, 2: Vendor Specific ========================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x0
     bAlternateSetting  :    0x2
     bNumEndpoints      :    0x6
     bInterfaceClass    :   0xff Vendor Specific
     bInterfaceSubClass :   0xff
     bInterfaceProtocol :   0xff
     iInterface         :    0x0 
      ENDPOINT 0x1: Interrupt OUT ==========================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x1 OUT
       bmAttributes     :    0x3 Interrupt
       wMaxPacketSize   :   0x40 (64 bytes)
       bInterval        :    0x1
      ENDPOINT 0x81: Interrupt IN ==========================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x81 IN
       bmAttributes     :    0x3 Interrupt
       wMaxPacketSize   :   0x40 (64 bytes)
       bInterval        :    0x1
      ENDPOINT 0x2: Interrupt OUT ==========================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x2 OUT
       bmAttributes     :    0x3 Interrupt
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x1
      ENDPOINT 0x4: Bulk OUT ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x4 OUT
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
      ENDPOINT 0x86: Interrupt IN ==========================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x86 IN
       bmAttributes     :    0x3 Interrupt
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x1
      ENDPOINT 0x88: Bulk IN ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x88 IN
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
    INTERFACE 0, 3: Vendor Specific ========================
     bLength            :    0x9 (9 bytes)
     bDescriptorType    :    0x4 Interface
     bInterfaceNumber   :    0x0
     bAlternateSetting  :    0x3
     bNumEndpoints      :    0x6
     bInterfaceClass    :   0xff Vendor Specific
     bInterfaceSubClass :   0xff
     bInterfaceProtocol :   0xff
     iInterface         :    0x0 
      ENDPOINT 0x1: Interrupt OUT ==========================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x1 OUT
       bmAttributes     :    0x3 Interrupt
       wMaxPacketSize   :   0x40 (64 bytes)
       bInterval        :    0x1
      ENDPOINT 0x81: Interrupt IN ==========================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x81 IN
       bmAttributes     :    0x3 Interrupt
       wMaxPacketSize   :   0x40 (64 bytes)
       bInterval        :    0x1
      ENDPOINT 0x2: Isochronous OUT ========================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x2 OUT
       bmAttributes     :    0x1 Isochronous
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x1
      ENDPOINT 0x4: Bulk OUT ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :    0x4 OUT
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
      ENDPOINT 0x86: Isochronous IN ========================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x86 IN
       bmAttributes     :    0x1 Isochronous
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x1
      ENDPOINT 0x88: Bulk IN ===============================
       bLength          :    0x7 (7 bytes)
       bDescriptorType  :    0x5 Endpoint
       bEndpointAddress :   0x88 IN
       bmAttributes     :    0x2 Bulk
       wMaxPacketSize   :  0x200 (512 bytes)
       bInterval        :    0x0
