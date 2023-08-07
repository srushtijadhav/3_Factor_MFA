# import sqlite3

# conn = sqlite3.connect('DataBase.db') 
# c = conn.cursor()

# c.execute('''
#           CREATE TABLE people (
#    person_id INTEGER PRIMARY KEY AUTOINCREMENT,
#    first_name text NOT NULL,
#    last_name text ,
#    username text NOT NULL UNIQUE,
#    password text NOT NULL,
#    role text NOT NULL,
#    MFA_FLG VARCHAR(1) NOT NULL,
#    IMAGE BLOB   
# )
#           ''')
          

                     
# conn.commit()

# ---------------------------
# import sqlite3
# db_file_path = "DataBase.db"
# def retrieve_data(name):
#     try:
#         # Connect to the SQLite database
#         connection = sqlite3.connect(db_file_path)
#         cursor = connection.cursor()

#         # Use parameterized query to prevent SQL injection
#         query = "select username "
#         query+= " ,password from people  "
#         query+=" where username = ?"
        
#         print(query)
#         cursor.execute(query,(name,))
#         # Fetch the data
#         data = cursor.fetchall()
        

#         # Print or process the retrieved data
#         for row in data:
            
#             print(row)

#     except sqlite3.Error as e:
#         print("Error occurred:", e)

#     finally:
#         # Close the connection
#         if connection:
#             connection.close()



# name = input('Name:  ')
# retrieve_data(name)


#------------------------------------------------------------------------- Public & Private key

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# def generate_rsa_keypair():
#     from cryptography.hazmat.primitives.asymmetric import rsa
#     private_key = rsa.generate_private_key(
#         public_exponent=65537,
#         key_size=2048,
#         backend=default_backend()
#     )
#     public_key = private_key.public_key()

#     # Serialize the keys to PEM format
#     private_pem = private_key.private_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PrivateFormat.PKCS8,
#         encryption_algorithm=serialization.NoEncryption()
#     )
#     public_pem = public_key.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     )

#     # Save the keys to files (Optional)
#     with open('private_key.pem', 'wb') as f:
#         f.write(private_pem)
#     with open('public_key.pem', 'wb') as f:
#         f.write(public_pem)

#     return True

# flg = generate_rsa_keypair()
# print(flg)

def read_private_key(file_path):
    with open(file_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

def read_public_key(file_path):
    with open(file_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

# def encrypt(message, public_key):
#     ciphertext = public_key.encrypt(
#         message.encode(),
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=padding.SHA256()),
#             algorithm=padding.SHA256(),
#             label=None
#         )
#     )
#     return ciphertext

# def decrypt(ciphertext, private_key):
#     plaintext = private_key.decrypt(
#         ciphertext,
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=padding.SHA256()),
#             algorithm=padding.SHA256(),
#             label=None
#         )
#     )
#     return plaintext.decode()

# if __name__ == "__main__":
#     # Read RSA private key
#     private_key_path = "private_key.pem"
#     private_key = read_private_key(private_key_path)

#     # Read RSA public key
#     public_key_path = "public_key.pem"
#     public_key = read_public_key(public_key_path)

#     # Encrypt and decrypt a message
#     message = "Hello, RSA encryption!"
#     encrypted_message = encrypt(message, public_key)
#     decrypted_message = decrypt(encrypted_message, private_key)

#     print("Original Message:", message)
#     print("Encrypted Message:", encrypted_message)
#     print("Decrypted Message:", decrypted_message)





import rsa

# generate public and private keys with
# rsa.newkeys method,this method accepts
# key length as its parameter
# key length should be atleast 16
#publicKey, privateKey = rsa.newkeys(512)

# this is the string that we will be encrypting
message = "hello geeks"
publicKey, privateKey = rsa.newkeys(512)
# private_key_path = "private_key.pem"
# private_key = read_private_key(private_key_path)
# public_key_path = "public_key.pem"
# public_key = read_public_key(public_key_path)

# rsa.encrypt method is used to encrypt
# string with public key string should be
# encode to byte string before encryption
# with encode method
encMessage = rsa.encrypt(message.encode(),
						publicKey)

print("original string: ", message)
print("encrypted string: ", encMessage)

# the encrypted message can be decrypted
# with ras.decrypt method and private key
# decrypt method returns encoded byte string,
# use decode method to convert it to string
# public key cannot be used for decryption
decMessage = rsa.decrypt(encMessage, privateKey).decode()

print("decrypted string: ", decMessage)
