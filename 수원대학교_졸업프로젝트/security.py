import base64
import hashlib
from Cryptodome import Random
from Cryptodome.Cipher import AES 


class AESCipher():

    def __init__(self, key):
        self.block_size = 32
        self.key = hashlib.sha256(AESCipher.change_bytes(self,key)).digest()
        self.PADDING='|'

    def change_bytes(self,data):
        data_type = type("")
        #b''.decode('utf8')
        if isinstance(data, data_type):
            return data.encode('utf8')
        return data

    def _padding(self, s):
        # return s + (self.block_size - len(s) % self.block_size) * AESCipher.change_bytes(chr(self.block_size - len(s) % self.block_size))
        return  s + (self.block_size - len(s) % self.block_size) * self.PADDING.encode('utf-8')


    def _unpadding(self,s):
        return s[:-ord(s[len(s)-1:])]


    def encrypt(self, raw):
        raw = self._padding(AESCipher.change_bytes(self,raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key,AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')


    def decrypt(self, enc):

        enc = base64.b64decode(enc)
        iv=Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return cipher.decrypt(enc).rstrip(self.PADDING.encode('utf-8'))[16:]


