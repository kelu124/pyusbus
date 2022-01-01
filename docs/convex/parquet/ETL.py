import os
import pcapy as p
from scapy.all import * 

import pandas as pd
import glob
import struct
import numpy as np


def readPCAP_Convex(filename):
    packets = rdpcap(filename)
    Config = []

    start = 0
    for k in packets:
        t = k.time
        k = k[Raw].load

        start += 1

        if not k[16]:
            #print("ID:",start,k[16],k[21],k[32:36],len(k),k[22]) 
            if k[22] == 0x02 and k[21] == 128:
                L1 = struct.unpack( 'i', k[23:27] )[0]
                wV = struct.unpack( 'h', k[30:32] )[0]
                wI = struct.unpack( 'h', k[32:34] )[0]   
                wL = struct.unpack( 'h', k[34:36] )[0]  
                Config.append({"t":t,'ID': start,"Sens":k[16],"EP":k[21],"Type":k[22],"Length":L1,"bmReqTyp":k[28],
                               "Req":k[29],"wV":wV,"wI":wI,"wL":wL,
                               "TypeP":128
                              })
            elif k[22] == 0x02 and k[21] == 129:
                L1 = struct.unpack( 'i', k[23:27] )[0]
                wV = struct.unpack( 'h', k[30:32] )[0]
                wI = struct.unpack( 'h', k[32:34] )[0]   
                wL = struct.unpack( 'h', k[34:36] )[0]  
                Config.append({"t":t,'ID': start,"Sens":k[16],"EP":k[21],"Type":k[22],"Length":L1,"bmReqTyp":k[28],
                               "Req":k[29],"wV":wV,"wI":wI,"wL":wL,
                               "TypeP":129
                              })
            elif len(k) >= 539 and k[21] == 1:
                L1 = struct.unpack( 'i', k[23:27] )[0]
                Config.append({"t":t,'ID': start,"Sens":k[16],"EP":k[21],"Type":k[22],"Length512":L1 ,
                               "TypeP":512,"payload":k[27:]
                              })    
            elif (k[22] == 0xfe) or (k[22] == 0x7e):
                pass

            else:
                Config.append({"t":t,'ID': start,"Sens":k[16],"EP":k[21],"Type":k[22],"TypeP":"Unknown"})
        else:
            if len(k)>512:
                #print(start,len(k[27:]))
                if len(k[27:]) == 512:
                       Config.append({"t":t,'ID': start,"Sens":k[16],"EP":k[21],"Type":k[22],"Length":512,
                               "TypeP":"Rec_512","payload":k[27:]})
                if len(k[27:]) == 65508:
                       Config.append({"t":t,'ID': start,"Sens":k[16],"EP":k[21],"Type":k[22],"Length":65508,
                               "TypeP":"Rec_65508","Data":k[27:]})
            else:
                Config.append({"t":t,'ID': start,"Sens":k[16],"EP":k[21],"Type":k[22],"TypeP":"Unknown2"})
    return pd.DataFrame(Config) 

def readPayload_Convex(df,packetid):
    PL = df.iloc[packetid].payload
    return np.array( struct.unpack( '>'+str(len(PL)//1)+'B', PL ) )

def savePCAP(df,filename):
    df[df.columns[:-1]].astype({'TypeP': str}).to_parquet(filename+".parquet")
    #print(len(df),"packets.")
    return filename+ ' saved'

def processAll():
    for f in glob.glob('./*.pcapng'):
        df = readPCAP_Convex(f)
        print("File:",f,"- size:",len(df),"packets.")
        res = savePCAP(df,f)
    return "Done"
