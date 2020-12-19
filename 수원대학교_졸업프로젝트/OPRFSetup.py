import random
from Crypto.Util.number import getPrime
import Crypto.Random
from sympy import isprime


class OPRFSetup:
    def __init__(self):    

        self.q=88659814541496837864246379650307344803245082549267922038649472491123172200963704210847900328944210419799732651053417626574751001663415661497555541817763498175067892344237355903185900778348422538532175767569839727810726079534240548272841349705870821196709961499230988217183579949347300122560138658319005679571
        self.p=177319629082993675728492759300614689606490165098535844077298944982246344401927408421695800657888420839599465302106835253149502003326831322995111083635526996350135784688474711806371801556696845077064351535139679455621452159068481096545682699411741642393419922998461976434367159898694600245120277316638011359143
        self.g=0
    
    def qset(self):
        i=0
        j=0
        # self.p=2*self.q+1
        while 1:
           
            if isprime(self.p):
                j=j+1
                if(j==30):

                    break

            else:
                # self.q=getPrime(1023,randfunc=Crypto.Random.get_random_bytes)
                # self.q=88659814541496837864246379650307344803245082549267922038649472491123172200963704210847900328944210419799732651053417626574751001663415661497555541817763498175067892344237355903185900778348422538532175767569839727810726079534240548272841349705870821196709961499230988217183579949347300122560138658319005679571
                # self.p=(2*self.q)+1
                # self.p=177319629082993675728492759300614689606490165098535844077298944982246344401927408421695800657888420839599465302106835253149502003326831322995111083635526996350135784688474711806371801556696845077064351535139679455621452159068481096545682699411741642393419922998461976434367159898694600245120277316638011359143
                j=0    
            
            i=i+1
            

    def setqg(self,p,q):
        self.p=p
        self.q=q
    
    def getp(self):
        return self.p
    def left_to_right_binary(self,g,q,p):
        parray=format(q,'b')
        parray2=parray[::-1]
        twoarray=[]
        i=0
        while i<len(format(q,'b')):
                
            if i==0:
                a=2**i # 1
                b=(g**a)%p # = g
                
                twoarray.append(b)
            else:
                b=(twoarray[i-1]**2)%p
                twoarray.append(b)

            i=i+1
        i=0
        beta=1

        while i<len(parray2):
            
            if(parray2[i]=="1"):
                beta=beta*twoarray[i]
               
                beta=beta%p
            i=i+1
        return beta
            

            
    def getq(self):
        return self.q

    def gpset(self):


        while 1:
            self.g=random.randint(2,self.p-2)

            i=0
            beta=self.left_to_right_binary(self.g,self.q,self.p)
            alpa=(self.g**2)%self.p
            if alpa !=1 and beta ==1:
                print("alpa")
                print("beata")
                break
        return self.p, self.g

