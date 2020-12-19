import OPRFSetup
import Crypto.Random
from Crypto.Util.number import getPrime
from sympy import isprime
import random
from decimal import Decimal
xid=15
z=6456346347568137456456456346347568137456456456346347568137456456456346347568137456456456346347568321
while 1:
    q=getPrime(100,randfunc=Crypto.Random.get_random_bytes)
    p=(2*q)+1
    if isprime(p):
        break

while 1:
    g=random.randint(2,p-2)
    a=(g**2)%p
    b=(g**q)%p
    if a!=1 and b==1:
        break
inverse_z=1
while 1:
    
    if ((inverse_z*z)%q)==1:
        break
    else:
        inverse_z=inverse_z+1

print(inverse_z)
y=xid*(inverse_z)
print(y)
print(y*z)
gkx=4




print("이문제")
xtag=(pow(g,(gkx*xid)))%p
print(xtag**(1/xid))
# print(round(pow(xtag,(1/gkx))))
# print(int(round(pow(xtag,(1/gkx)),5)))
print(pow(g,gkx))

xtoken=(pow(g,(z*gkx)))%p
print(xtoken)
print(xtag)
print(((xtoken**(inverse_z))**xid)%p)
print((xtoken**(xid*(inverse_z)))%p)

## 방법은 두개뿐 인데 y를 해결하거나
## xtag도 잘라서 넣고 찾는것도 잘라서 찾으면....