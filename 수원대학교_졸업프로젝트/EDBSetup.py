import os
import security
import hashlib
import hmac
import string
import random
import Gfunction
import OPRFSetup
from Crypto.Util.number import getPrime
import Crypto.Random
class EYset:
    def __init__(self,encrypdata,ydata):
        self.encryptdata=encrypdata
        self.ydata=ydata

    def getEdata(self):
        return self.encryptdata
    
    def getYdata(self):
        return self.ydata

class EDB:

    def __init__(self):
        self.path_dir='C:/졸작/졸작/filelist'
        self.file_list=os.listdir(self.path_dir)
        
        self.t1=0
        self.key=""
        self.w=[]
        self.W2=[]
        self.D=[]
        self.T=[]
        self.State=[]
        self.Xset=[]
        self.GKd=Gfunction.G()
        self.GKx=Gfunction.G()
        self.GKz=Gfunction.G()
        self.OPRFSet=OPRFSetup.OPRFSetup()
        self.keyd=Gfunction.G.OPRFKeyGen(self.GKd)
        Gfunction.G.setpg(self.GKd)
        self.p, self.g= Gfunction.G.getpg(self.GKd)
        self.q=Gfunction.G.getq(self.GKd)
        self.keyx=Gfunction.G.OPRFKeyGen(self.GKx)
        Gfunction.G.setpg2(self.GKx,self.p, self.g)
        self.keyz=Gfunction.G.OPRFKeyGen(self.GKz)
        Gfunction.G.setpg2(self.GKz,self.p, self.g)

    def choice_key(self):
        key_length=10
        string_rand=string.ascii_letters
        for i in range(key_length):
            self.key = self.key + random.choice(string_rand)

        return self.key


    # 파일 리스트 폴더 받아서 각 파일마다 w[i] 키워드 추출 w[i][j]
    # def make_w(self):
    #     i=0
    #     while i < len(self.file_list):
            
    #         f=open(self.path_dir+'/'+self.file_list[i],'r')
    #         lines=f.readlines()
        
    #         self.w.append([])
        
    #         self.w[i].append(self.file_list[i])
    
    #         for line in lines:
    #             self.w[i].append(line.rstrip())
    #             self.W2.append(line.rstrip())
               
    #         i=i+1

    def make_w(self):
        i=0
        f=open(self.path_dir+'/'+"input.txt",'r')
        lines=f.readlines()
        while i < len(lines):
            line0=lines[i].split(':')
            line2=line0[1].split(",")
            self.w.append([])
        
            self.w[i].append(line0[0])
    
            for line in line2:
                self.w[i].append(line.rstrip())
                self.W2.append(line.rstrip())
               
            i=i+1
        f.close()
    def make_Ws(self):
        # 키워드 중복 제거해서 배열에 대입
        i=0
        j=1
        Wsize=len(self.W2)
        while i<Wsize:
            while j<Wsize:
                
                if self.W2[i]==self.W2[j]:
                    self.W2.remove(self.W2[i])
                    j=i+1
                    Wsize=len(self.W2)
                j=j+1
                
            i=i+1
            j=i+1

    

    
    

    # 딕셔너리 하는게 낫겠다
    def make_D(self):
        i=0
        while i<len(self.W2):

            self.D.append([])
            self.D[i].append(self.W2[i])
            
            for files in self.w:
                if self.W2[i] in files :
                    self.D[i].append(files[0])
            i=i+1



    
    def Extended_Euclid(self,r1, r2):
        r=0
        q=0
        s=0
        s1=1
        s2=0
        t=0
        self.t1=0
        t2=1
        tmp = r1

        while(r2):
    
            q = int(r1/r2)
            r = r1%r2
            s = s1 - q*s2
            t = self.t1 - q*t2

            r1 = r2
            r2 = r
            s1 = s2
            s2 = s
            self.t1 = t2
            t2 = t



        if(r1 == 1):
            if(self.t1 < 0):
                self.t1 += tmp
            
        else:
            self.t1=0


    def make_T(self):
        i=0
        while i<len(self.D):
            self.T.append([])
            self.T[i].append(self.W2[i])
            key = hmac.new((self.key).encode('utf-8'), self.W2[i].encode('utf-8'), hashlib.sha1).hexdigest()
            
            ctr=1
            while ctr < len(self.D[i]):
                
                AES2=security.AESCipher(key)
                encryptdata=security.AESCipher.encrypt(AES2,self.D[i][ctr])

                Gfunction.G.setxi(self.GKd,self.D[i][ctr])
                Gfunction.G.setxi(self.GKz,self.W2[i]+str(ctr))

                Gfunction.G.setxi(self.GKx,self.W2[i])
                xid=Gfunction.G.gety(self.GKd)
                z=Gfunction.G.gety(self.GKz)


                invers=0
                
                EDB.Extended_Euclid(self,z,self.q)
                if((z*invers)%self.q !=1):
                    EDB.Extended_Euclid(self,self.q,z)
                invers=self.t1
                if(invers):

                    if(self.W2[i]=="Ratchet"):
                        print(invers)
                else:
                    print("역원이 존재하지 않습니다. \n")    
                   

                
                y=(xid*invers)%self.q
            

                eysets=EYset(encryptdata,y)
                self.T[i].append(eysets)
                gy=Gfunction.G.gety(self.GKx)

                q=gy*xid
                xtag=OPRFSetup.OPRFSetup.left_to_right_binary(self.OPRFSet,self.g,q,self.p)
                ctr=ctr+1

                self.Xset.append(xtag)

            self.State.append([])
            self.State[i].append(self.W2[i])
            self.State[i].append(ctr)
            i=i+1
           
        
        return self.T
            



    def getXset(self):
        return self.Xset

    def getState(self):
        return self.State
    def getkeyzxpg(self):
        return self.keyz, self.keyx, self.p, self.g


# A=EDB()
# A.choice_key()
# A.make_w()
# A.make_Ws()
# A.make_D()
# T=A.make_T()

