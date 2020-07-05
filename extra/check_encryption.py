# from simplecrypt import encrypt, decrypt
# password = 'something'
# message = "To be encrypted!"
# ciphertext = encrypt(password, message).decode('latin-1')

# cipher2 = ciphertext.encode('latin-1')
# print(cipher2)
# decrypted = decrypt(password, cipher2)

# print(decrypted)
# password = decrypted.decode('utf-8')
# print(password)
# bytearray

from cryptography.fernet import Fernet
key = Fernet.generate_key()
f = Fernet(key)
message = input()
token = f.encrypt(message.encode('utf-8'))
answer = f.decrypt(token)

print(answer)

