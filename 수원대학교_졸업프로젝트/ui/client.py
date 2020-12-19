from socket import *
import TSetSetup
import hmac
import sys
import security
import json
import Gfunction
import OPRFSetup
import hashlib
import time
class SearchClient:

    def __init__(self):
        self.keyword=[]
        self.stag=""
        self.port = 8080
        self.key=""
        self.encode_key=""
        self.decryptdata=[]
        self.IDs=[]
        self.Xset=[]
        self.State=[]
        self.keyz=""
        self.keyx=""
        self.p=0
        self.g=0
        self.ctr=0
        self.minword=""
        self.Ws=[]
        self.z=""
        self.xtoken=[]
        # self.clientSock = socket(AF_INET, SOCK_STREAM)
        # self.clientSock.connect(('127.0.0.1', self.port))
        self.tset=[]
        self.file_list=[]

        

    def getTset(self):
    

        TSETS=TSetSetup.TsetSet()
        TSetSetup.TsetSet.make_free(TSETS)
        tset, key=TSetSetup.TsetSet.make_tset(TSETS)
        self.Xset=TSetSetup.TsetSet.getXset(TSETS)
        self.State=TSetSetup.TsetSet.getState(TSETS)
        self.keyz, self.keyx, self.p, self.g = TSetSetup.TsetSet.getkeyzxpg(TSETS)
        return tset, key


        
    def input_keyword(self,keyword):
        i=0
        key_value=""

        while i<len(keyword):
            if keyword[i]=="\n":
                self.keyword.append(key_value)
                key_value=""
            else:
                key_value=key_value+keyword[i]
            i=i+1
        self.keyword.append(key_value)
    


    def gettoken(self,key):
        minkeyword=1000000
        minword=""
        print("키워드입력")
        # while 1:
        #     keyword=input('그만입력시 exit 입력 >>>')
        #     if keyword=="exit":
        #         break
        #     else:
        #         self.keyword.append(keyword)
                

        i=0

        while i<len(self.keyword):
            j=0
            cnt=0
            while j<len(self.State):
                    if self.keyword[i]==self.State[j][0]:
                        self.Ws.append(self.State[j])
                        cnt=cnt+1
                    j=j+1
            if(cnt==0):
                self.Ws.append([self.keyword[i],0])
            i=i+1

        i=0
        while i<len(self.Ws)-1:
            j=i+1

            while j<len(self.Ws):
                if self.Ws[i][1]>self.Ws[j][1]:
                    temp=self.Ws[i]
                    self.Ws[i]=self.Ws[j]
                    self.Ws[j]=temp

                j=j+1
            i=i+1

        self.stag = hmac.new(key.encode('utf-8'), self.Ws[0][0].encode('utf-8'), hashlib.sha1).hexdigest()

        

    


    
    def connectServer(self) :
        self.clientSock = socket(AF_INET, SOCK_STREAM)
        self.clientSock.connect(('127.0.0.1', self.port))
        print('접속 완료')

    def send_DBinfo(self,id,pw):
        self.clientSock.send(id.encode('utf-8'))
        self.clientSock.send(pw.encode('utf-8'))
        time.sleep(0.1)
        recv_data=self.clientSock.recv(1024).decode('utf-8')
        if recv_data =="OK":
            return True
        elif recv_data =="NO":
            return False
    def Initialize_DB(self):
        self.clientSock.send("error".encode('utf-8'))
        time.sleep(0.1)
    def MTU_send(self,data):
        i=0
        error_check_Data=""
        try:
            while 1:
                if(i+1460>len(data)):
                    sub_num=len(data)-i
                    self.clientSock.send(data[i:i+sub_num].encode('utf-8'))
                    error_check_Data=self.clientSock.recv(10).decode('utf-8')
                    break
                self.clientSock.send(data[i:i+1460].encode('utf-8'))
                time.sleep(0.01)
                i=i+1460
                error_check_Data=self.clientSock.recv(10).decode('utf-8')
                if(error_check_Data=="error"):
                    self.MTU_send(data)
                    return
                #self.clientSock.sendall(json.dumps(self.tset).encode('utf-8'))
            time.sleep(0.01)
            self.clientSock.send("exit".encode('utf-8'))
        except Exception:
            self.clientSock.send("error".encode('utf-8'))
            self.MTU_send(data)

    def set_TXset(self):
        self.tset, self.key=SearchClient.getTset(self)
    def send_TXset(self):

        time.sleep(0.1)
        # self.tset, self.key=SearchClient.getTset(self)
                

        k=0
        while k<len(self.tset):
            print(self.tset[k])
            k=k+1
        # data=json.dumps(self.tset)
        # with open("jsonfile", 'wb') as file:
        #     file.write(data.encode('utf-8'))
         # with open("jsonfile",'rb') as file:
        #     send_file=file.read()
        # self.clientSock.send(json.dumps(self.tset).encode('utf-8'))
        # time.sleep(0.1)
        # self.clientSock.send(json.dumps(self.Xset).encode('utf-8'))
        # time.sleep(0.1)
        data= json.dumps(self.tset)
        self.MTU_send(data)
        time.sleep(0.1)
        data2=json.dumps(self.Xset)
        self.MTU_send(data2)
        time.sleep(0.1)

    def startwork(self):
            SearchClient.gettoken(self,self.key)
            # print(self.ctr) 이거 +1 나오네 
            i=0
            GF=Gfunction.G()
            GF2=Gfunction.G()
            Gfunction.G.OPRFKeyGen2(GF,self.keyz)
            Gfunction.G.OPRFKeyGen2(GF2,self.keyx)
            Gfunction.G.setpg2(GF,self.p,self.g)
            Gfunction.G.setpg2(GF2,self.p,self.g)
            self.ctr=self.Ws[0][1]
            while i<self.ctr-1:  #  2

                Gfunction.G.setxi(GF,self.Ws[0][0]+str(i+1))
                self.z=Gfunction.G.gety(GF)
           
                j=1
                if len(self.Ws)>1:  #3
                    while j<len(self.Ws):
        
                        Gfunction.G.setxi(GF2,self.Ws[j][0])
                        # print("ws")
                        # print(self.Ws[j][0])
                        Wi=Gfunction.G.gety(GF2)
                        # print("Wi")
                        # print(Wi)
                        # print("self.z")
                        # print(self.z)
                        q=Wi*self.z
                        # q=Wi*25353495834053463456452535349583405346345645253534958340534634564525353495834053463456452535349583405346345645253534958340534634564525353495834053463456452535349583405346345645
                        OPRFs=OPRFSetup.OPRFSetup()
                        value=OPRFSetup.OPRFSetup.left_to_right_binary(OPRFs,self.g,q,self.p)

                        if j==1:
                            values=[]
                            values.append(value)
                            self.xtoken.append(values)
                        else:
                            self.xtoken[i].append(value)
                        j=j+1
                else:
                        
                    Gfunction.G.setxi(GF2,self.Ws[0][0])
                    Wi=Gfunction.G.gety(GF2)
                    q=Wi*self.z
                    # q=Wi*25353495834053463456452535349583405346345645253534958340534634564525353495834053463456452535349583405346345645253534958340534634564525353495834053463456452535349583405346345645
                    OPRFs=OPRFSetup.OPRFSetup()
                    value=OPRFSetup.OPRFSetup.left_to_right_binary(OPRFs,self.g,q,self.p)
                    values=[]
                    values.append(value)
                    self.xtoken.append(values)
                    # print("Wi")
                    # print(Wi)
                    # print("self.z")
                    # print(self.z)
                i=i+1
            print("아아아3")
            print(self.xtoken)
            self.clientSock.send(self.stag.encode('utf-8'))
            time.sleep(0.1)
            xtoken_data=json.dumps(self.xtoken)
            self.MTU_send(xtoken_data)
            # self.clientSock.send(json.dumps(self.xtoken).encode('utf-8'))
            time.sleep(0.1)
            self.clientSock.send((str(self.p)).encode('utf-8'))


            while True:
                idvalue=self.clientSock.recv(1024).decode('utf-8')
                if(idvalue=="exit"):
                    break
                self.IDs.append(idvalue)

    

    # def startwork(self):

    #     while 1:

    #         print('1번 Tset 전송 , 2번 검색 시작')
    #         num=""
    #         sys.stdout.flush()
    #         num=input('>>>')

    #         if num=='1':
    #             self.tset, self.key=SearchClient.getTset(self)
                
    #             print("self.tset")
    #             k=0
    #             while k<len(self.tset):
    #                 print(self.tset[k])
    #                 k=k+1
    #             # data=json.dumps(self.tset)
    #             # with open("jsonfile", 'wb') as file:
    #             #     file.write(data.encode('utf-8'))
    #             # with open("jsonfile",'rb') as file:
    #             #     send_file=file.read()
    #             self.clientSock.send(json.dumps(self.tset).encode('utf-8'))
    #             time.sleep(0.1)
    #             self.clientSock.send(json.dumps(self.Xset).encode('utf-8'))
    #             time.sleep(0.1)

    #         elif num=="2":
    #             SearchClient.gettoken(self,self.key)
    #             # print(self.ctr) 이거 +1 나오네 
    #             i=0
    #             GF=Gfunction.G()
    #             GF2=Gfunction.G()
    #             Gfunction.G.OPRFKeyGen2(GF,self.keyz)
    #             Gfunction.G.OPRFKeyGen2(GF2,self.keyx)
    #             Gfunction.G.setpg2(GF,self.p,self.g)
    #             Gfunction.G.setpg2(GF2,self.p,self.g)
    #             self.ctr=self.Ws[0][1]
    #             while i<self.ctr-1:  #  2

    #                 Gfunction.G.setxi(GF,self.Ws[0][0]+str(i+1))
    #                 self.z=Gfunction.G.gety(GF)
           
    #                 j=1
    #                 if len(self.Ws)>1:  #3
    #                     while j<len(self.Ws):
        
    #                         Gfunction.G.setxi(GF2,self.Ws[j][0])
    #                         # print("ws")
    #                         # print(self.Ws[j][0])
    #                         Wi=Gfunction.G.gety(GF2)
    #                         # print("Wi")
    #                         # print(Wi)
    #                         # print("self.z")
    #                         # print(self.z)
    #                         q=Wi*self.z
    #                         # q=Wi*25353495834053463456452535349583405346345645253534958340534634564525353495834053463456452535349583405346345645253534958340534634564525353495834053463456452535349583405346345645
    #                         OPRFs=OPRFSetup.OPRFSetup()
    #                         value=OPRFSetup.OPRFSetup.left_to_right_binary(OPRFs,self.g,q,self.p)

    #                         if j==1:
    #                             values=[]
    #                             values.append(value)
    #                             self.xtoken.append(values)
    #                         else:
    #                             self.xtoken[i].append(value)
    #                         j=j+1
    #                 else:
                        
    #                     Gfunction.G.setxi(GF2,self.Ws[0][0])
    #                     Wi=Gfunction.G.gety(GF2)
    #                     q=Wi*self.z
    #                     # q=Wi*25353495834053463456452535349583405346345645253534958340534634564525353495834053463456452535349583405346345645253534958340534634564525353495834053463456452535349583405346345645
    #                     OPRFs=OPRFSetup.OPRFSetup()
    #                     value=OPRFSetup.OPRFSetup.left_to_right_binary(OPRFs,self.g,q,self.p)
    #                     values=[]
    #                     values.append(value)
    #                     self.xtoken.append(values)
    #                     # print("Wi")
    #                     # print(Wi)
    #                     # print("self.z")
    #                     # print(self.z)
                        
    #                 i=i+1
    #             print("아아아3")
    #             print(self.xtoken)
    #             self.clientSock.send(self.stag.encode('utf-8'))
    #             time.sleep(0.1)
    #             self.clientSock.send(json.dumps(self.xtoken).encode('utf-8'))
    #             time.sleep(0.1)
    #             self.clientSock.send((str(self.p)).encode('utf-8'))


    #             while True:
    #                 idvalue=self.clientSock.recv(1024).decode('utf-8')
    #                 if(idvalue=="exit"):
    #                     break
    #                 self.IDs.append(idvalue)



    #         else:
    #             print('error or find')
    #             break
    

    def getIds(self):

        self.encode_key=hmac.new(self.key.encode('utf-8'), self.Ws[0][0].encode('utf-8'), hashlib.sha1).hexdigest()
        AES=security.AESCipher(self.encode_key)
        i=0
        while i<len(self.IDs):
           
            decryptdata=security.AESCipher.decrypt(AES,self.IDs[i])
            print(decryptdata.decode('utf-8'))
            self.decryptdata.append(decryptdata.decode('utf-8'))
            i=i+1

    def send_fileid(self):
        time.sleep(0.1)
        self.clientSock.send(json.dumps(self.decryptdata).encode('utf-8'))
    # def write_file(data, filename):
    #     with open(filename, 'wb') as file:
    #         file.write(data)
    def get_file(self):
        # file_list=json.loads(self.clientSock.recv(100000).decode('utf-8'))
        i=0
        name=[]

        self.file_list=[]
        while 1:
            file2=self.clientSock.recv(100000)
            if file2==("exit".encode('utf-8')):
                break
            self.file_list.append(file2)
        
        for files in self.file_list:
            name.append("downolad_file"+str(i))
            i=i+1
        return name

        
    def down_file(self):
        i=0
        key = hmac.new('MBiQyKxOkH'.encode('utf-8'), 'rVtNNIywrx'.encode('utf-8'), hashlib.sha1).hexdigest()
        AES=security.AESCipher(key)
        for files in self.file_list:
            decryptdata=security.AESCipher.decrypt(AES,files)
            name="./download_files/downolad_file"+str(i)
            with open(name, 'wb') as file:
                file.write(decryptdata)
            i=i+1
        return len(self.file_list)
    def loop_check(self):
        # print('1번 재검색 , 2번 종료')
        # num=""
        # sys.stdout.flush()
        # num=input('>>>')
        # if num !="1" and num !="2":
        #     print("잘못입력")
        #     num="2"
        time.sleep(0.1)
        self.clientSock.send("!#loop_check#%".encode('utf-8'))
        self.xtoken=[]
        self.IDs=[]
        self.decryptdata=[]
        # self.Xset=[]
        # self.State=[]
        self.keyword=[]
        self.Ws=[]
        # return num
    def loop_check2(self):
        time.sleep(0.1)
        self.clientSock.send("!#loop_check2#%".encode('utf-8'))
        




# Searches=SearchClient()
# SearchClient.connectServer(Searches)
# while 1:
#     SearchClient.startwork(Searches)
#     SearchClient.getIds(Searches)
#     SearchClient.send_fileid(Searches)
#     SearchClient.get_file(Searches)
#     if SearchClient.loop_check(Searches)=="2":
#         break
