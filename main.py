import rsa

def generate_keys():
    (pubKey, privKey) = rsa.newkeys(1024)
    with open('rsa_enc_signature/keys/pubkey1.pem', 'wb') as f:
        f.write(pubKey.save_pkcs1('PEM'))

    with open('rsa_enc_signature/keys/privkey1.pem', 'wb') as f:
        f.write(privKey.save_pkcs1('PEM'))

    with open('rsa_enc_signature/keys/pubkey2.pem', 'wb') as f:
        f.write(pubKey.save_pkcs1('PEM'))

    with open('rsa_enc_signature/keys/privkey2.pem', 'wb') as f:
        f.write(privKey.save_pkcs1('PEM'))

def load_keys():
    with open('rsa_enc_signature/keys/pubkey1.pem', 'rb') as f:
        pubKey1 = rsa.PublicKey.load_pkcs1(f.read())

    with open('rsa_enc_signature/keys/privkey1.pem', 'rb') as f:
        privKey1 = rsa.PrivateKey.load_pkcs1(f.read())

    with open('rsa_enc_signature/keys/pubkey2.pem', 'rb') as f:
        pubKey2 = rsa.PublicKey.load_pkcs1(f.read())

    with open('rsa_enc_signature/keys/privkey2.pem', 'rb') as f:
        privKey2 = rsa.PrivateKey.load_pkcs1(f.read())

    return pubKey1, privKey1, pubKey2, privKey2

def encrypt(msg, key):
    return rsa.encrypt(msg, key)

def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode("UTF-8")
    except:
        return False

def sign_sha1(msg, key):
    return rsa.sign(msg.encode("UTF-8"), key, 'SHA-1')

def verify_sha1(msg, signature, key):
    try:
        return rsa.verify(msg.encode('ascii'), signature, key) == 'SHA-1'
    except:
        return False

generate_keys()
pubKey1, privKey1, pubKey2, privKey2 = load_keys()

message = input('Enter a message:')

ciphertext1 = encrypt(message, pubKey1)
print(ciphertext1)
ciphertext1 = ciphertext1.encode("ascii")
print(ciphertext1)

signature = sign_sha1(message, privKey1)

ciphertext2 = encrypt(ciphertext1, pubKey2)

decrypt_msg_layer2 = decrypt(ciphertext2, privKey2)

plaintext = decrypt(decrypt_msg_layer2, privKey1)


print(f'Cipher text: {ciphertext2}')
print(f'Signature: {signature}')

if plaintext:
    print(f'Plain text: {plaintext}')
else:
    print('Could not decrypt the message.')

if verify_sha1(plaintext, signature, pubKey1):
    print('Signature verified!')
else:
    print('Could not verify the message signature.')

