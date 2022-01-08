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


def readPCAP_Doppler(filename): 
    packets = rdpcap(filename)
    Config = [] 
 
    j = 0
    for k in packets: 
        
        t = k.time 
        k = k[Raw].load
        j = j+1
        if k[0x10] == 1:
            L = len(k[0x1B:])
            #print(j,"Bulk in","EP:",k[6],"-Type",k[7],L,"bytes")
            if L > 20000:
                Config.append({'ID': j,"t":t,"TYPE":"B","Payload":k[0x1B:],"Length":L})            
            elif L > 400:
                Config.append({'ID': j,"t":t,"TYPE":"DOPPLER","Payload":k[0x1B:],"Length":L})
            else:
                Config.append({'ID': j,"t":t,"TYPE":"OTHER","Payload":k[0x1B:],"Length":L})
            #print(k[0x1B:])
        elif k[0x15] == 2:
            L = len(k[0x1B:])
            if L>500:
                # This is written as URB_BULK, on ENDPOINT #2
                Config.append({'ID': j,"t":t,"TYPE":"OUT_PROG","Payload":k[0x1B:],"Length":L})   
        else:
            #print(j,k[0x14],k[0x15])
            if k[0x15] == 128:
                #print( k[30:32])
                wVal    = struct.unpack( 'H', k[30:32] )[0]
                wIndex  = struct.unpack( 'H', k[32:34] )[0]
                wLength = struct.unpack( 'H', k[34:36] )[0]
                Config.append({'ID': j,"t":t,"TYPE":"URBCTRL","bReqType":k[28],"bReq":k[29],\
                            "wVal":wVal,"wIndex":wIndex,"wLength":wLength
                            }) 
                
            else:
                Config.append({'ID': j,"t":t,"TYPE":"UNKNWN"}) 
        #print(j, "Sens:",hex(k[8]),"Type:",hex(k[9]),"EP:",hex(k[10])) 
        #print(j,hex(k[6]),hex(k[0x15]),k) 
    df = pd.DataFrame(Config)
    ref = float(df.loc[0,"t"])
    df.source = "DOPPLER"
    if not ref == 0:
        ref = float(df.loc[0,"t"])
        df["t"] = df.t.apply(lambda x: round(float(x) - ref, 3))
    df = df[df.Length<65500]
    return df


def readPayload_Convex(df,packetid):
    PL = df.iloc[packetid].payload
    return np.array( struct.unpack( '>'+str(len(PL)//1)+'B', PL ) )

def savePCAP(df,filename):
    df.to_parquet(filename.replace(" ","_")+".parquet")
    #print(len(df),"packets.")
    return filename+ ' saved'