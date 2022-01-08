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

def readPCAP_Healson(filename):
    # sorted(df.EP.unique()) == [0, 1, 128, 129, 130]
    packets = rdpcap(filename)
    Config = []
    j = 0
    start = 0
    for k in packets:
        start += 1
        
        t = k.time
        k = k[Raw].load 
        # Checking packet, 0x53 == going out, 0x43: received
        if k[8] == 0x53:
            #print(j, "Sens:",hex(k[8]),"Type:",hex(k[9]),"EP:",hex(k[10]))
            # check if payload sent to probe
            if k[8] == 0x53 and k[9] == 0x03 and k[10] ==2:
                #print(j,"BULK OUT. Payload:",k[64:][:3])
                Config.append({"t":t,'ID': start,"RequestType:":k[40],\
                    "EP":k[10],"data":k[64:][:3]})
            elif k[8] == 0x53 and k[9] == 0x03 and k[10] ==0x86:
                L = struct.unpack( 'i', k[32:36] )[0]
                #print(j,"BULK IN. Requested length:",L)
                Config.append({"t":t,'ID': start,"RequestType:":k[40],\
                    "EP":k[10],"Length":L})
            elif k[8] == 0x53 and k[9] == 0x02 and k[10] ==0x80:
                L = struct.unpack( 'i', k[32:36] )[0]
                Config.append({"t":t,'ID': start,"RequestType:":k[40],\
                    "bRequest":k[41],"value":k[42],"EP":k[10],"Length":L})
            ## Urb
            elif k[8] == 0x53 and k[9] == 0x02 and k[10] ==0:
                LENGTH = struct.unpack( 'H', k[46:48] )[0]
                IDX = struct.unpack( 'H', k[43:45] )[0]
                
                #print(j,"CTR OUT RequestType:",k[40],"bRequest",k[41],"value",k[42],"index",IDX,"length",LENGTH)
                Config.append({"t":t,'ID': start,"RequestType:":k[40],\
                    "bRequest":k[41],"value":k[42],"index":IDX,"length":LENGTH, "EP":k[10]})
            else:
                Config.append({"t":t,'ID': start,"EP:":k[10]})
 
    return pd.DataFrame(Config) 

def readPayload_Convex(df,packetid):
    PL = df.iloc[packetid].payload
    return np.array( struct.unpack( '>'+str(len(PL)//1)+'B', PL ) )

def savePCAP(df,filename):
    df.to_parquet(filename+".parquet")
    #print(len(df),"packets.")
    return filename+ ' saved'