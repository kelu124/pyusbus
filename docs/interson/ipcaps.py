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

def readPCAP_Interson(filename):
    packets = rdpcap(filename)
    Config = [] 
    ix = 0
    for k in packets:
        ix += 1
        t = k.time
        k = k[Raw].load
        EP = -1
        if k[8] == 0x53: # URB submit
            if k[9] == 0x02: # URB submit
                TYPE = "URB_CONTROL"
            elif k[9] == 0x03: # BULK
                TYPE = "BULK"
            EP = k[10] # EP
            if EP == 0:
                SENS ="OUT"
            else:
                SENS = "IN"
            if TYPE == "BULK":
                sizeRequested = k[33]*256+k[32] 
                Config.append({'ID': ix,"t":t,"Sens":SENS,"TYPE":TYPE,"EP":k[10],"sizeRequested":sizeRequested})
            else:
                bmRequestType = k[40]
                bmRequest = k[41]
                bmValue  =  256*k[43]+k[42] 
                bmIndex  = k[44]+256*k[45]  
                bmLength =  k[46]+256*k[47]  
                if bmLength:
                    PL = k[64:] 
                else:
                    PL = ""
                Config.append({'ID': ix,"t":t,"Sens":SENS,"TYPE":TYPE,"EP":k[10],"bmRequestType":bmRequestType,
                            "bmRequest":bmRequest,"bmValue":bmValue,"bmIndex":bmIndex,"bmLength":bmLength,
                            "PL":PL
                        })
             
    return pd.DataFrame(Config) 

def readPayload_Convex(df,packetid):
    PL = df.iloc[packetid].payload
    return np.array( struct.unpack( '>'+str(len(PL)//1)+'B', PL ) )

def savePCAP(df,filename):
    df["probe"] = "interson"
    df["source"] = filename
    ref = float(df.loc[0,"t"]) 
    if not ref == 0:
        ref = float(df.loc[0,"t"])
        df["t"] = df.t.apply(lambda x: round(float(x) - ref, 3))
    df.PL = df.PL.fillna(b'')
    df = df.fillna(-1)
    for k in ["EP","bmRequestType","bmRequest","bmValue","bmIndex","bmLength"]:
        df[k] = df[k].astype(int)

    df["sig"] =  df.EP.astype(str)+ "."+df.bmRequestType.astype(str)+ "."+df.bmRequest.astype(str)+ "." + \
        df.bmValue.astype(str)+ "."+df.bmIndex.astype(str)+ "."+df.bmLength.astype(str)
    df.to_parquet(filename+".parquet")
    return filename+ ' saved'