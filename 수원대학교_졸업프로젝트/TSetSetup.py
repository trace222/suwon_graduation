
import sys
import hmac
import base64
import hashlib
import random
import security
import json
import EDBSetup
from collections import namedtuple
# key='secret'
EDBS=EDBSetup.EDB()
key=EDBSetup.EDB.choice_key(EDBS)
EDBSetup.EDB.make_w(EDBS)
EDBSetup.EDB.make_Ws(EDBS)
EDBSetup.EDB.make_D(EDBS)

class TsetSet:
    def __init__(self):
        self.Tset=[['']*128 for i in range(128)]
        self.T=EDBSetup.EDB.make_T(EDBS)
        self.Xset=EDBSetup.EDB.getXset(EDBS)
        self.State=EDBSetup.EDB.getState(EDBS)
        self.value=namedtuple("tsetvalue","eval xval")
        self.TsetG=namedtuple("tset","label value")
        self.make_k=87112285931760246646623899502532662132608 #129bit 값
        self.FREE=[]
  

    def make_free(self):
        i=0
        while i<128:
            j=0
            self.FREE.append([])
            while j<128:
                self.FREE[i].append(j)
                j=j+1
            i=i+1    
        

    
    def make_tset(self):
        j=0
        for ws in self.T:
            w=ws[0]
            i=1
            
            stag = hmac.new(key.encode('utf-8'), w.encode('utf-8'), hashlib.sha1).hexdigest()

            while i<len(ws):
                cnt=0   
                j=0 
                stagF = hmac.new(chr(i).encode('utf-8'), stag.encode('utf-8'),hashlib.sha1).hexdigest()
   
                hashl=hashlib.sha256(stagF.encode('utf-8')).digest()
                b=hashl[26]&0b01111111
                L=int(hashl[0:10].hex(),16)
                K=int(hashl[10:27].hex(),16)&self.make_k

                while 1:
                    j=random.randrange(0,128)
                    if(self.FREE[i][j]==500):
                        cnt=cnt+1
                        continue
                    else:
                        self.FREE[b][j]=500
                        break

                if cnt==128:
                    print("나가리")
                    continue
                if i==(len(ws)-1):
                    beta='0'
                else:
                    beta='1'
            

                values=ws[i].getEdata()+beta

                
                num=0
                s=0
                checkzero=""
                str2=""
                while s<len(values):
                    str2=str2+"{0:>08s}".format(format(ord(values[s]),'b'))
                    s=s+1
                
 

                while checkzero !='1':
                    checkzero=str2[num]
                    num=num+1
                num=num-1
                str3=int(str2,2)^K
           
                evaldata=str(num)+str(str3)
                xval=ws[i].getYdata()


                
                value=self.value(evaldata,xval)
                b=int(b)
                self.Tset[b][j]=self.TsetG(L,value)

                i=i+1
        
        # print(self.Tset)
        return self.Tset, key

    def getXset(self):
        return self.Xset
        
    def getState(self):
        return self.State
    
    def getkeyzxpg(self):
        keyz, keyx, p, g= EDBSetup.EDB.getkeyzxpg(EDBS)
        return keyz, keyx, p, g
        
    


# A=TsetSet()
# TsetSet.make_free(A)
# tset,key=TsetSet.make_tset(A)

# # print(tset)
# jsoni=json.dumps(tset)
# print(jsoni)
# dict=json.loads(jsoni)
# print(dict)


# print(id)
# id =id+'1'
# print(id[64])
# w=T[0][0]
# i=1

# stag = hmac.new(key.encode('utf-8'), w.encode('utf-8'), hashlib.sha1).hexdigest()
# stagF = hmac.new(chr(i).encode('utf-8'), stag.encode('utf-8')).hexdigest()
# hashl=hashlib.sha256(stagF.encode('utf-8')).digest()
# b=hashl[27]>>1
# # L=hashl[0:]
