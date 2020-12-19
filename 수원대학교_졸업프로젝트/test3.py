import pymysql
import os
import security
import hmac
import hashlib
import string
import random
# MySQL Connection 연결
def choice_key():
    key=""
    key_length=10
    string_rand=string.ascii_letters
    for i in range(key_length):
        key = key + random.choice(string_rand)

    return key
conn = pymysql.connect(host='localhost', user='kwon', password='awgw9383',
                       db='kwon', charset='utf8')
 
# Connection 으로부터 Cursor 생성
curs = conn.cursor()
 
# SQL문 실행

sql_insert_blob_query = " UPDATE edb SET file=%s WHERE file_id=%s "
sql_select = " SELECT file_id from edb "
curs.execute(sql_select)
id_list=curs.fetchall()
print(id_list)
# 데이타 Fetch 
filename="./2.txt"
path_dir='./file'
key1=choice_key() #MBiQyKxOkH
key2=choice_key()#rVtNNIywrx
print(key1)
print(key2)
file_list=os.listdir(path_dir)
key = hmac.new(key1.encode('utf-8'), key2.encode('utf-8'), hashlib.sha1).hexdigest()
AES=security.AESCipher(key)
print(file_list)
i=0
for file_id in file_list:

    with open('./file/'+file_id, 'rb') as file:
        binaryData = file.read()

    encryptdata=security.AESCipher.encrypt(AES,binaryData)
    blob_data=(encryptdata,id_list[i])
    result=curs.execute(sql_insert_blob_query,blob_data)
    conn.commit()
    i=i+1
print("Image and file inserted successfully as a BLOB into python_employee table", result)
rows = curs.fetchall()
print(rows)     # 전체 rows
# print(rows[0])  # 첫번째 row: (1, '김정수', 1, '서울')
# print(rows[1])  # 두번째 row: (2, '강수정', 2, '서울')
 
# Connection 닫기
conn.close()