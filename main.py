from passlib.hash import pbkdf2_sha256
dbs = {}
import hashlib
import random
import ast
import string
from Crypto.Cipher import AES
import os
ascii_dict = {}
hex_dict = {}
for i in range(1,128):
    if (i % 2) == 0:
        hex1=(chr(8204)*i)
    else:
        hex1=(chr(8205)*i)
    ascii_dict[hex1] = chr(i)
for i in range(1,128):
    if (i % 2) == 0:
        hex11=(chr(8204)*i + chr(32))
    else:
        hex11=(chr(8205)*i + chr(32))
    hex_dict[chr(i)] = hex11
def encoder(words, cipher):
    result = ''
    for letter in words:
        if letter in cipher:
            result = result + cipher[letter]
        else:
            result = result + letter
    return result
def decoder(words, cipher):
    result = ''
    wordo = words.split(chr(32))
    for i in range(len(wordo)):
        if wordo[i] in cipher:
            result = result + cipher[wordo[i]]
        else:
            result = result + wordo[i]
    return result
characters=os.path.getsize('dbs.txt')
print(characters)
if characters > 0:  
  hmm = open('dbs.txt', 'r')
  data = str(hmm.read())
  data = ast.literal_eval(decoder(str(data), ascii_dict))
  dbs = data
while True:
  if len(dbs) > 5000:
    print("Sorry the dbs is full")
    break
  lor = input("Would you like to login or register:")
  if lor == "login":
    user = input("What is your username:")
    if user in dbs:
      pswd = input("What is your password:")
      x = len(pswd)
      if x < 32:
        pswd = pswd+('x'*(32-x))
      pswd = bytes(pswd, 'utf-8')
      my_key = pswd
      cipher = AES.new(my_key,AES.MODE_ECB)
      key = hashlib.sha256(pswd).digest()
      iv = dbs[user][1]
      iv = cipher.decrypt(iv)
      iv = iv.strip()
      aes = AES.new(key, AES.MODE_CBC, iv)
      pswd = str(aes.encrypt(pswd))[2:-1]
      pswd2 = dbs[user][0]
      pswd3 = pswd2[x:]
      if pbkdf2_sha256.verify(pswd, pswd3):
        print ("Welcome,", user)
        break
      else:
        print("You entered the wrong password")
    else: 
      print ("Your username is not in our database")
  elif lor == "register":
    user = input("What would you like your username to be:")
    while True:
      if user not in dbs:
        pswd = input("What would you like your password to be:")
        if len(pswd)>=10 and len(pswd)<=32: 
          x = len(pswd)
          if x < 32:
            pswd = pswd+('x'*(32-x))
          pswd = bytes(pswd, 'utf-8')
          my_key = pswd
          cipher = AES.new(my_key, AES.MODE_ECB)
          key = hashlib.sha256(pswd).digest()
          iv = ''.join(random.choice
          (string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
          enc = str(iv).rjust(32)
          aes = AES.new(key, AES.MODE_CBC, iv)
          pswd = str(aes.encrypt(pswd))[2:-1]
          print("Your account has been created.")
          ghb = random.randint(60, 250)
          slt = random.randint(3, 7)
          pswd = pbkdf2_sha256.encrypt(pswd, rounds=ghb,salt_size=slt)
          strng = list(string.printable)
          def random_char(y):
            return ''.join(random.choice(strng) for x in range(y))
          salt = random_char(x)
          pswd = salt + pswd
          iv = (cipher.encrypt(enc))
          dbs[user] = (pswd, iv)
          break
        else:
          print("your password must be between 10 and 32 characters")
      else:
        print("Your username is already taken")
  else:
    print("invlaid input")
with open('dbs.txt', 'w', encoding='utf-8') as fp:
    fp.write(encoder(str(dbs), hex_dict))

