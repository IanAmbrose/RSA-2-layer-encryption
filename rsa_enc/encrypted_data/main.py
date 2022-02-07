from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


# Generat 4 keys - 2 private, 2 public and write out to files sorted in /keys
def generate_keys(lens):
    key1 = RSA.generate(lens)
    key2 = RSA.generate(lens)

    private_key1 = key1.export_key()
    file_out = open("rsa_enc/keys/private1.pem", "wb")
    file_out.write(private_key1)
    file_out.close()

    public_key1 = key1.publickey().export_key()
    file_out = open("rsa_enc/keys/public1.pem", "wb")
    file_out.write(public_key1)
    file_out.close()

    private_key2 = key2.export_key()
    file_out = open("rsa_enc/keys/private2.pem", "wb")
    file_out.write(private_key2)
    file_out.close()

    public_key2 = key2.publickey().export_key()
    file_out = open("rsa_enc/keys/public2.pem", "wb")
    file_out.write(public_key2)
    file_out.close()

    return private_key1,public_key1,private_key2,public_key2

#load the private, public and session keys and return for variable allocation

def load_keys():
    priv1 = RSA.import_key(open("rsa_enc/keys/private1.pem").read())
    pub1 = RSA.import_key(open("rsa_enc/keys/public1.pem").read())

    priv2 = RSA.import_key(open("rsa_enc/keys/private2.pem").read())
    pub2 = RSA.import_key(open("rsa_enc/keys/public2.pem").read())
    session_key1 = get_random_bytes(16)
    session_key2 = get_random_bytes(16)

    return priv1,pub1,priv2,pub2,session_key1, session_key2
    
# display function to allow the used to see the public keys used in the encryption
def display_keys(pub1,pub2):
    pub1 = pub1.exportKey().decode('UTF-8')
    pub2 = pub2.exportKey().decode('UTF-8')
    print(f'\n\n Generated RSA Keys...  ')
    print(f'\n Public key 1 -> Link(Private Key 1) : \n\n {pub1}')
    print(f'\n\n Public key 2 -> Link(Private Key 2) : \n\n {pub1}')

#encrypt the plaintext, and layer 1 encryption.
# this function is ran twice, for each layer of the encryption.
# Each of the encrypted data is stored in a file inside /encrypted_data

def encrypt(message, pub1,session_key, filename):
    file_out = open(f'rsa_enc/encrypted_data/{filename}.bin', "wb")
    cipher_rsa = PKCS1_OAEP.new(pub1)
    enc_session_key = cipher_rsa.encrypt(session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX)

    ciphertext, tag = cipher_aes.encrypt_and_digest(message)

    [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
    file_out.close()

    return ciphertext

#decrypt layer 2 and layer 1 encryption - Ran twice
#The decrption of layer 2 is stored in a file named decoded

def decrypt(priv1,session_key,filename):
    file_in = open(f'rsa_enc/encrypted_data/{filename}.bin', "rb")
    file_out = open(f'rsa_enc/encrypted_data/decoded.bin', "wb")

    enc_session_key, nonce, tag, ciphertext = \
        [ file_in.read(x) for x in (priv1.size_in_bytes(), 16, 16, -1) ]

    cipher_rsa = PKCS1_OAEP.new(priv1)
    session_key = cipher_rsa.decrypt(enc_session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    try:
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
        file_out.close()

        print(data.decode("UTF-8"))
        return data
    except:
        False

# Text Menu function 
def print_menu():
    print('''\n
1: 'Encode New Message'
2: 'Display Public Keys'
3: 'Exit'
    ''')


# Main function, runs the functions needed for the program to run
# Prints the function outputs to the screen.
def main():

    filename1 = 'encrpyted_data1'
    filename2 = 'encrpyted_data2'
    message = input("\nEnter secret message: ").encode("UTF-8")
    encrypted_msg = encrypt(message, pub1, session_key1, filename1)
    print(f'Layer 1 Encrypted Message (publicKey1): {encrypted_msg}')

    encrypted_msg = encrypt(encrypted_msg, pub2, session_key2, filename2)
    print(f'Layer 2 Encrypted Message (publicKey1&2): {encrypted_msg}\n\n')

    decrypted_msg = decrypt(priv2,session_key2, filename2)
    decrypted_msg = decrypt(priv1,session_key2, filename1).decode('UTF-8')

    print((f'\nSecret Message (2 Layer Encryption): {encrypted_msg}'))

    if decrypted_msg:
        print(f'\nDecoded message: {decrypted_msg}\n')
    else:
        print("\n Unable to decode message")

if __name__ == "__main__" :
    # Input for the encryption bytre size when generating keys, can be changed needs to be a multiple of 4, (1024 being the lowest value accepted)
    generate_keys(2048)
    priv1, pub1, priv2, pub2, session_key1, session_key2 = load_keys()

    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')

        if option == 1:
            main()
        elif option == 2:
            display_keys(pub1, pub2)    

        elif option == 3:
            print('Exiting...')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 3.')


