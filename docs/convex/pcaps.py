# -*- coding: utf-8 -*-
# 
from scapy.all import *
import pandas as pd
import struct
import numpy as np
import array
import json 
import pprint
import hashlib
import base64 

def tagDF(df,source):
    dictKeys = loadJson()

    ref = float(df.loc[0,"t"])
    df.source = source
    if not ref == 0:
        ref = float(df.loc[0,"t"])
        df["t"] = df.t.apply(lambda x: round(float(x) - ref, 3))
    df["verbose"] = np.nan
    df.loc[((df.bmReqTyp == 0xC3) & (df.Req == 176) & (df.wV == 0) & (df.wI == 0 )),"verbose"] = "SetupStep1"
    df.loc[((df.bmReqTyp == 0xC3) & (df.Req == 187) & (df.wV == 3) & (df.wI == 0 )),"verbose"] = "SetupStep2"
    df.loc[((df.bmReqTyp == 0xC3) & (df.Req == 187) & (df.wV == 3) & (df.wI == 32)),"verbose"] = "SetupStep3"
    df.loc[((df.bmReqTyp == 0xC3) & (df.Req == 187) & (df.wV == 3) & (df.wI == 64)),"verbose"] = "SetupStep4"
    df.TypeP = df.TypeP.astype(str)
    df["sig"] = np.nan
    df["basePL"] = np.nan
    df["source"] = source
    df.loc[~df.payload.isna(),"basePL"] =  df.loc[~df.payload.isna(),"payload"].apply(lambda x: str(base64.b64encode(x)))
    df.loc[~df.payload.isna(),"sig"] =  df.loc[~df.payload.isna(),"payload"].apply(lambda x: signPacket(x))
    #str(base64.b64encode(PL163))
    # #df.loc[~df.payload.isna(),"lst"] =  df.loc[~df.payload.isna(),"payload"].apply(lambda x: bin2array(x))
    for keyZ in dictKeys.keys():
        #print(keyZ, dictKeys[keyZ]["desc"])
        df.loc[df.sig == keyZ,"verbose"] = dictKeys[keyZ]["desc"]
    return df


def signPacket(binary):
    return hashlib.sha1(binary).hexdigest()[:6]


def loadJson(fileName='CONVEX.json'):
    with open(fileName, 'r') as f:
        dataTxt= f.read()
        data = json.loads(dataTxt) 
    return data
    
def updateJson(DF,dictKeys): 
    dictKeys = loadJson()
    DF = DF[~DF.sig.isna()].drop_duplicates(subset=["sig"],keep="first")
    DF["verbose"] = DF.apply(lambda x: "Packet "+str(x.ID)+ " "+x.source, axis=1)
 
    for i, row in DF.iterrows():
        #print(row.sig)
        if row.sig not in dictKeys.keys():
            dictKeys[row.sig] = {"source": row.source, "packet": row.ID, "desc": row.verbose, "payload":row.basePL[2:-1]}
    saveJson(dictKeys)
    return dictKeys

def saveJson(data,fileName='CONVEX.json'):
    pretty_print_json = pprint.pformat(data).replace("'",'"')
    with open(fileName, 'w') as f:
        f.write(pretty_print_json)  


def bin2array(binary,length=False):
    U = array.array("B")
    U.fromstring(binary)
    L = list(U[4:-4])
    L = np.trim_zeros(L, "b")
    if length:
        return len(L), L
    return L

def readPCAP_Convex(filename):
    # sorted(df.EP.unique()) == [0, 1, 128, 129, 130]
    packets = rdpcap(filename)
    Config = []

    start = 0
    for k in packets:

        
        t = k.time
        k = k[Raw].load
        assert k[21] in [0, 1, 128, 129, 130]
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