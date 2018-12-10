#This file contains all of the functions used for storing the passwords

import random
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#This generates a ten character random alphanumeric string
def generateSalt():
    return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for i in range(10))



#This functions takes in a value, a key, and a salt and outputs an encrypted version
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
    return token.decode()

#This function takes in a value encrypted by encrypt(), as well as the same salt and key passed in to encrypt()
#It outputs the unencrypted value
def decrypt(value, key, salt):
    value=str.encode(value)
    kdf = PBKDF2HMAC(
         algorithm=hashes.SHA256(),
         length=32,
         salt=str.encode(salt),
         iterations=100000,
         backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(str.encode(key)))
    f = Fernet(key)
    return (f.decrypt(value)).decode()
