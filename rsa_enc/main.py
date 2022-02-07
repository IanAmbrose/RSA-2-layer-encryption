from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


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


def load_keys():
    priv1 = RSA.import_key(open("rsa_enc/keys/private1.pem").read())
    pub1 = RSA.import_key(open("rsa_enc/keys/public1.pem").read())

    priv2 = RSA.import_key(open("rsa_enc/keys/private2.pem").read())
    pub2 = RSA.import_key(open("rsa_enc/keys/public2.pem").read())
    session_key = get_random_bytes(16)

    return priv1,pub1,priv2,pub2,session_key
    

def display_keys(pub1,pub2):
    pub1 = pub1.exportKey().decode('UTF-8')
    pub2 = pub2.exportKey().decode('UTF-8')
    print(f'\n\n Generated RSA Keys...  ')
    print(f'\n Public key 1 -> Link(Private Key 1) : \n\n {pub1}')
    print(f'\n\n Public key 2 -> Link(Private Key 2) : \n\n {pub1}')


def encode(message, pub1,session_key):
    session_key = get_random_bytes(16)
    file_out = open("rsa_enc/encrypted_data/encrypted_data.bin", "wb")
    cipher_rsa = PKCS1_OAEP.new(pub1)
    enc_session_key = cipher_rsa.encrypt(session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(message)

    [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
    file_out.close()
    ciphertext = ciphertext
    return ciphertext


def decode(priv1):
    file_in = open("rsa_enc/encrypted_data/encrypted_data.bin", "rb")

    enc_session_key, nonce, tag, ciphertext = \
        [ file_in.read(x) for x in (priv1.size_in_bytes(), 16, 16, -1) ]

    cipher_rsa = PKCS1_OAEP.new(priv1)
    session_key = cipher_rsa.decrypt(enc_session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    try:
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        print(data.decode("UTF-8"))
        return data
    except:
        False


def print_menu():
    print('''\n
1: 'Encode New Message'
2: 'Display Public Keys'
3: 'Exit'
    ''')


def main():          
    message = input("\nEnter secret message:\n").encode("UTF-8")
    encoded_msg = encode(message, pub1, session_key)
    decoded_msg = decode(priv1).decode('UTF-8')

    print((f'\nEncoded message: {encoded_msg}'))
    if decoded_msg:
        print(f'\nDecoded message: {decoded_msg}\n')
    else:
        print("\n Unable to decode message")


if __name__ == "__main__" :

    generate_keys(1024)
    priv1, pub1, priv2, pub2,session_key = load_keys()

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
            print('Thanks message before exiting')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')


