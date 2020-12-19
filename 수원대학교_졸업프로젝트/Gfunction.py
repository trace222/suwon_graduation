import random
import OPRFSetup


class G:
    def __init__(self):
        self.k=128
        self.l=128
        self.K=[]
        self.p=0
        self.g=0
        self.q=0

        self.xi=""

        
    def OPRFKeyGen(self):

        i=0
        while i<self.l:
            ki=random.getrandbits(128)
            self.K.append(ki)
            i=i+1

        return self.K
    
    def OPRFKeyGen2(self,K):
        self.K=K
        return self.K

    def setpg(self):

        OPRFSet=OPRFSetup.OPRFSetup()
        OPRFSetup.OPRFSetup.qset(OPRFSet)
        self.p,self.g=OPRFSetup.OPRFSetup.gpset(OPRFSet)
        self.q=OPRFSetup.OPRFSetup.getq(OPRFSet)
        
    def getq(self):
        return self.q
    def setpg2(self,p,g):
        self.p=p
        self.g=g
    
    def getpg(self):
        return self.p, self.g

    def setxi(self,xi):
        xi=xi.encode('utf-8')
        xi=list(map(bin,xi))
        i=0
        while i<len(xi):
            xi[i]=xi[i].lstrip("0b")

            xi[i]=xi[i].rjust(8,'0')
            i=i+1
        
        self.xi="".join(xi)

        self.xi=self.xi[::-1]
        


    def gety(self):
        i=0
        OPRFSet2=OPRFSetup.OPRFSetup()
        y=self.g
       
        while i<len(self.xi):
            if self.xi[i]=="1":
                y=OPRFSetup.OPRFSetup.left_to_right_binary(OPRFSet2,y,self.K[i],self.p)
            i=i+1
        return y

