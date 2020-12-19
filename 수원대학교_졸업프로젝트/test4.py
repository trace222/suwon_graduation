import pymysql
import os
import security
import hmac
import hashlib

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
# MySQL Connection 연결
conn = pymysql.connect(host='localhost', user='kwon', password='awgw9383',
                       db='kwon', charset='utf8')
 
# Connection 으로부터 Cursor 생성
curs = conn.cursor()
 
# SQL문 실행
key = hmac.new('MBiQyKxOkH'.encode('utf-8'), 'rVtNNIywrx'.encode('utf-8'), hashlib.sha1).hexdigest()
AES=security.AESCipher(key)

sql_fetch_blob_query = """SELECT * from edb where file_id = %s"""
curs.execute(sql_fetch_blob_query,'F1')
rows = curs.fetchall()
for row in rows:
    print("Id = ", row[0], )
    file = row[1]
    decryptdata=security.AESCipher.decrypt(AES,file)
    print(decryptdata)

    write_file(decryptdata, "./kwon.txt")


conn.commit()


print(rows)     # 전체 rows
# print(rows[0])  # 첫번째 row: (1, '김정수', 1, '서울')
# print(rows[1])  # 두번째 row: (2, '강수정', 2, '서울')
 
# Connection 닫기
conn.close()