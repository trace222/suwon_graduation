from socket import *
import security
import hmac
import hashlib
import json
from collections import namedtuple
import OPRFSetup
import pymysql
import time

class Server:
    def __init__(self):
        self.TsetG=namedtuple("Asd","label value")
        self.port=8080
        self.serversock=socket(AF_INET,SOCK_STREAM)
        self.serversock.bind(('',self.port))
        self.serversock.listen(1)
        # self.conn = pymysql.connect(host='localhost', user='kwon', password='awgw9383',db='kwon', charset='utf8')
        # self.conn=""
        # self.curs = self.conn.cursor()
        self.connectionSock=""
        self.addr=""
        self.Tset=""
        self.Xset=""
        self.sql=""
        self.stag=""
        self.xtoken=""
        self.p=""
        self.Ys=[]
        self.IDs=[]
        self.IDs2=[]
        self.file_list=[]

    def send(self,sock):
        sendData1 = input('>>>')
        self.serversock.send(sendData1.encode('utf-8'))


    def receive(self,sock):
        
        recvData2=""
        recvData4=""
        try:
            while 1:
                recvData=""
                recvData=self.connectionSock.recv(1460).decode('utf-8')
                if(recvData=="exit"):
                    break
                if(recvData=="error"):
                    self.disconnect_db()
                    self.receive(sock)
                    return
                # recvData2=json.loads(recvData)
                self.connectionSock.send("Nerr".encode('utf-8'))
                recvData2=recvData2+recvData
            while 1:
                recvData3=""
                recvData3=self.connectionSock.recv(1460).decode('utf-8')
                if(recvData3=="exit"):
                    break
                if(recvData3=="error"):
                    self.disconnect_db()
                    self.receive(sock)
                    return
                # recvData2=json.loads(recvData)
                self.connectionSock.send("Nerr".encode('utf-8'))
                recvData4=recvData4+recvData3
            
            # windows 버전    
            # recvData=self.connectionSock.recv(200000).decode('utf-8')
            # recvData3=self.connectionSock.recv(200000).decode('utf-8')
            recvData2=json.loads(recvData2)
            recvData4=json.loads(recvData4)
        except Exception as e:
            print("Tset 에러", e)
            self.connectionSock.send("error".encode('utf-8'))
            self.receive(sock)

        return recvData2,recvData4


    def recive_from_client(self):
        try:
            print('%d번 포트로 접속 대기중...'%self.port)
            print(self.serversock.getsockname())
            self.connectionSock, self.addr = self.serversock.accept()
            print(str(self.addr), '에서 접속되었습니다.')
        except:
            print("접속 에러")
        # print('DB 접속되었습니다.')
        # self.Tset, self.Xset=self.receive(self.connectionSock)

    def recive_DB(self):
        id=self.connectionSock.recv(1460).decode('utf-8')
        time.sleep(0.1)
        pw=self.connectionSock.recv(1460).decode('utf-8')
        time.sleep(0.1)
        print(id)
        print(pw)
        try:
            self.conn=pymysql.connect(host='localhost', user=id, password=pw ,db='kwon', charset='utf8')
            self.connectionSock.send("OK".encode('utf-8'))
            self.curs = self.conn.cursor()
            print('DB 접속되었습니다.')
        except:
            self.connectionSock.send("NO".encode('utf-8'))
            print('DB 접속 실패했습니다.')
            self.recive_DB()
        

    def recive_TXset(self):
        self.Tset, self.Xset=self.receive(self.connectionSock)
        # if self.Tset=="error" or self.Xset=="error":
        #     self.disconnect_db()
        #     return 0
        # return 1

    def send_sql(self):
        error_i=0
        try:
            self.sql = "CREATE TABLE test(label VARCHAR(255), value VARCHAR(255), yvalue TEXT)"
            self.curs.execute(self.sql)
            self.conn.commit()
            i=0
            j=0
            while i<128:
                j=0
                while j<128:
                    if self.Tset[i][j]=='':
                        j=j+1
                        continue
                    
                    label=self.Tset[i][j][0]
                    value1=self.Tset[i][j][1][0]
                    yvalue1=str(self.Tset[i][j][1][1])
                    insert_sentese=""" INSERT INTO test(label,value,yvalue) VALUES (%s,%s,%s)"""
                    insert_value=(label,value1,yvalue1)
                    self.curs.execute(insert_sentese,insert_value)
                    self.conn.commit()
                    j=j+1
                i=i+1
        except:
            print("sql 전송중 에러")
            self.drop_table()
            error_i=error_i+1
            if error_i==10:
                print("10번이상 sql 에러 발생")
                return
            self.send_sql()
            
    def recive_stag(self):
        self.stag=self.connectionSock.recv(1460)
        if(self.p=="!#loop_check#%"):
            return "loop_go"
        return
    def recive_from_client2(self):
        recvData2=""
        recvData=""
        try:
            while 1:
                recvData=self.connectionSock.recv(1460).decode('utf-8')
                if(recvData=="exit"):
                    break
                # recvData2=json.loads(recvData)
                elif(recvData=="error"):
                    self.recive_from_client2()
                    return
                elif(recvData=="!#loop_check#%"):
                    return "loop_go"
                self.connectionSock.send("Nerr".encode('utf-8'))
                recvData2=recvData2+recvData

            self.xtoken=recvData2
            self.xtoken=json.loads(self.xtoken)
            # 윈도우 버전
            # self.xtoken=self.connectionSock.recv(200000).decode('utf-8')
            # self.xtoken=json.loads(self.xtoken)
            self.p=self.connectionSock.recv(1460).decode('utf-8')
            if(self.p=="!#loop_check#%"):
                return "loop_go"
            self.p=int(self.p)
        except:
            print("xtoken 에러")
            self.connectionSock.send("error".encode('utf-8'))
            self.recive_from_client2()
        return
   


    def Tsetvalue_select(self):

        beta=1
        i=1
        V=[]
        make_k=0b1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110000000
        try:
            while beta==1 and i<100:
                j=0
                stagF = hmac.new(chr(i).encode('utf-8'), self.stag).hexdigest()
                hashl=hashlib.sha256(stagF.encode('utf-8')).digest()
                b=hashl[26]&0b01111111
                L=int(hashl[0:10].hex(),16)
                K=int(hashl[10:27].hex(),16)&make_k
                # value_select=""" select value from test where label=%s"""
                value_select="SELECT value,yvalue FROM test where label=%s"
                self.curs.execute(value_select,L)
                rows=self.curs.fetchall()
                print("rows")
                print(rows)
                for row in rows:
                    num=0
                    values2=[]
                    checkzero=row[0][0]
                    value=int(row[0][1:])
                    values=value^K
                    values=format(values,'b')
                        
                        
                    while num<int(checkzero):
                        values="0"+str(values)
                        num=num+1
                    num=0
                    beta=values[-8:]
                    values=values[0:-8]
                    while num< len(values):
                        values2.append(chr(int(values[num:num+8],2)))
                        num=num+8

                    num=0

                    Yvalue=[]
                    Yvalue.append("".join(values2))
                    Yvalue.append(int(row[1]))
                    self.Ys.append(Yvalue)

                    beta=int(chr(int(beta,2)))
                
                
                i=i+1
        except:
            self.Ys=[]
            print("Tset 검색 에러")
            self.Tsetvalue_select()




    def insert_IDS(self):
        i=0
        GS=OPRFSetup.OPRFSetup()
        # print("ys")
        # print(self.Ys)
        # print(xtoken)
        # print(self.Ys)
        # print(len(xtoken))
        try:
            while i<len(self.xtoken):
                j=0
                self.IDs.append([])
                while j<len(self.xtoken[i]):
                    v=self.xtoken[i][j]
                    # print("v")
                    # print(v)
                    # print("ys[1]")
                    # print(self.Ys[i][1])
                    v2=OPRFSetup.OPRFSetup.left_to_right_binary(GS,v,(self.Ys[i][1]),self.p)
                    # v2=pow(v,self.Ys[i][1])%p
                    # print("v2")
                    # print(v2)
                    # print("v2")
                    # print(v2)
                    if v2 in self.Xset:
                        self.IDs[i].append(self.Ys[i][j])
                    j=j+1

                if len(self.IDs[i])==len(self.xtoken[i]):
                    self.IDs2.append(self.IDs[i][0])
                else:
                    print("아니")
                i=i+1
        except:
            print("ID 삽입중 에러")
            self.IDs=[]
            self.IDs2=[]
            self.insert_IDS()
    
    def send_IDS(self):
        # print("xset")
        # print(Xset)
        i=0
        # print("IDS")
        # print(IDs)
        print("IDS2")
        print(self.IDs2)
        while True:
            
            if i==len(self.IDs2):
                time.sleep(0.1)
                self.connectionSock.send("exit".encode('utf-8'))
                break
            time.sleep(0.1)
            self.connectionSock.send(self.IDs2[i].encode('utf-8'))
            # print(IDs2[i].encode('utf-8'))

            i=i+1


    def write_file(self,data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)

    def select_file(self):
        Index_id=self.connectionSock.recv(100000).decode('utf-8')
        if(Index_id=="!#loop_check#%"):
            return "loop_go"
        Index_id=json.loads(Index_id)

        print(Index_id)
        # key = hmac.new('MBiQyKxOkH'.encode('utf-8'), 'rVtNNIywrx'.encode('utf-8'), hashlib.sha1).hexdigest()
        # AES=security.AESCipher(key)
        for file_id in Index_id:
            sql = "SELECT file from edb where file_id=%s"
            self.curs.execute(sql,file_id)
            file1=self.curs.fetchone()
            self.file_list.append(file1)
            # sql_fetch_blob_query = """SELECT * from edb where file_id = %s"""
            # curs.execute(sql_fetch_blob_query,file_id)
            # rows = curs.fetchall()
            # for row in rows:
            #     print("Id = ", row[0], )
            #     file = row[1]
            #     decryptdata=security.AESCipher.decrypt(AES,file)
            #     print(decryptdata)

            #     write_file(decryptdata, "./kwon.txt")
        print(self.file_list)
        # curs.execute(sql)
        # conn.commit()
        # decryptdata=security.AESCipher.decrypt(AES,file_list[0][0])
        # with open("test.txt", 'wb') as file:
        #     file.write(decryptdata)
        return
    def send_files(self):
        for files in self.file_list:

            time.sleep(0.1)
            self.connectionSock.send(files[0])
        time.sleep(0.1)
        self.connectionSock.send("exit".encode('utf-8'))
    def drop_table(self):
        sql = "DROP TABLE test"
        self.curs.execute(sql)
        self.conn.commit()
    def disconnect_db(self):
        self.conn.close()

    def loop_check(self):
        check_num=self.connectionSock.recv(1000).decode('utf-8')
        self.Ys=[]
        self.IDs=[]
        self.IDs2=[]
        self.file_list=[]
        return check_num


if __name__ == "__main__":
    
    Server1=Server()
    Server.recive_from_client(Server1)
 
    Server.recive_DB(Server1)
    Server.recive_TXset(Server1)
    Server.send_sql(Server1)

            
        
    while 1:
        error_loop=""
        error_loop=Server.recive_stag(Server1)
        if(error_loop=="loop_go"):
            continue
        error_loop=Server.recive_from_client2(Server1)
        if(error_loop=="loop_go"):
            continue
        Server.Tsetvalue_select(Server1)

        Server.insert_IDS(Server1)

        Server.send_IDS(Server1)

        error_loop=Server.select_file(Server1)
        if(error_loop=="loop_go"):
            continue
        Server.send_files(Server1)

        if Server.loop_check(Server1)=="!#loop_check2#%":
            break

    Server.drop_table(Server1)
    Server.disconnect_db(Server1)

# if __name__ == "__main__":