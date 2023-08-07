import rsa

def save_keys(public_key, private_key):
    # Save the public key to a file
    with open("public_key.pem", "wb") as f:
        f.write(public_key.save_pkcs1())

    # Save the private key to a file (protected with a password)
    with open("private_key.pem", "wb") as f:
        encrypted_private_key = rsa.encrypt(private_key.save_pkcs1(), "your_password")
        f.write(encrypted_private_key)

def load_keys():
    # Load the public key from the file
    with open("public_key.pem", "rb") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())

    # Load the private key from the file (decrypt with the password)
    with open("private_key.pem", "rb") as f:
        encrypted_private_key = f.read()
        private_key = rsa.PrivateKey.load_pkcs1(rsa.decrypt(encrypted_private_key, "your_password"))

    return public_key, private_key

# Generate new keys
public_key, private_key = rsa.newkeys(512)

# Save the keys to files
save_keys(public_key, private_key)




def encrypt(message, public_key):
    return rsa.encrypt(message.encode(), public_key)

def decrypt(ciphertext, private_key):
    return rsa.decrypt(ciphertext, private_key).decode()

if __name__ == "__main__":
    # Load the keys from files
    public_key, private_key = load_keys()

    # Encrypt and decrypt a message
    message = "Hello, RSA encryption!"
    encrypted_message = encrypt(message, public_key)
    decrypted_message = decrypt(encrypted_message, private_key)

    print("Original Message:", message)
    print("Encrypted Message:", encrypted_message)
    print("Decrypted Message:", decrypted_message)
