import random
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generateSalt():
    return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for i in range(10))




def encrypt(value, key, salt):#https://cryptography.io/en/latest/fernet/?highlight=pbkdf
    kdf = PBKDF2HMAC(
         algorithm=hashes.SHA256(),
         length=32,
         salt=str.encode(salt),
         iterations=100000,
         backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(str.encode(key)))
    f = Fernet(key)
    token = f.encrypt(str.encode(value))
    return token


def decrypt(value, key, salt):
    kdf = PBKDF2HMAC(
         algorithm=hashes.SHA256(),
         length=32,
         salt=str.encode(salt),
         iterations=100000,
         backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(str.encode(key)))
    f = Fernet(key)
    return str(f.decrypt(value))
a=encrypt("hi", "bye", "abc")
print(a)
print(decrypt(a,"bye","abc"))
