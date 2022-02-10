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

    return private_key1, public_key1, private_key2, public_key2


# load the private, public and session keys and return for variable allocation


def load_keys():
    priv1 = RSA.import_key(open("rsa_enc/keys/private1.pem").read())
    pub1 = RSA.import_key(open("rsa_enc/keys/public1.pem").read())

    priv2 = RSA.import_key(open("rsa_enc/keys/private2.pem").read())
    pub2 = RSA.import_key(open("rsa_enc/keys/public2.pem").read())
    session_key1 = get_random_bytes(16)
    session_key2 = get_random_bytes(16)

    return priv1, pub1, priv2, pub2, session_key1, session_key2


# display function to allow the used to see the public keys used in the encryption
def display_keys(pub1, pub2):
    pub1 = pub1.exportKey().decode("UTF-8")
    pub2 = pub2.exportKey().decode("UTF-8")
    print(f"\n\n Generated RSA Keys...  ")
    print(f"\n Public key 1 -> Link(Private Key 1) : \n\n {pub1}")
    print(f"\n\n Public key 2 -> Link(Private Key 2) : \n\n {pub1}")


# encrypt the plaintext, and layer 1 encryption.
# this function is ran twice, for each layer of the encryption.
# Each of the encrypted data is stored in a file inside /encrypted_data


def encrypt(message, pub, session_key, filename):
    file_out = open(f"rsa_enc/data/encrypted_{filename}.bin", "wb")
    cipher_rsa = PKCS1_OAEP.new(pub)
    enc_session_key = cipher_rsa.encrypt(session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX)

    ciphertext, tag = cipher_aes.encrypt_and_digest(message)

    [file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
    file_out.close()

    return ciphertext


# decrypt layer 2 and layer 1 encryption - Ran twice
# The decrption of layer 2 is stored in a file named decoded


def decrypt(priv, filename):
    file_in = open(f"rsa_enc/data/encrypted_{filename}.bin", "rb")

    enc_session_key, nonce, tag, ciphertext = [
        file_in.read(x) for x in (priv.size_in_bytes(), 16, 16, -1)
    ]

    cipher_rsa = PKCS1_OAEP.new(priv)
    try:
        l2_enc_session_key = cipher_rsa.decrypt(enc_session_key)
        cipher_aes = AES.new(l2_enc_session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return data
    except:
        return


# Text Menu function
def print_menu():
    print(
        """\n
1: Encode New Message
2: Display Public Keys
3: Exit
    """
    )


# Display the Encryption, Decryption, Encrypted Message and plaintext to the screen
def display(encrypted_msg1, encrypted_msg2, decrypted_msg_1, message, filename):

    print("\n\n----ENCRYPTION----\n")
    print(f"Layer1 (publicKey1):\n{encrypted_msg1}\n")
    print(f"Layer2 (publicKey2):\n{encrypted_msg2}\n")
    print((f"\n\n----ENCRYPTED Message---- \n{encrypted_msg2}\n\n"))

    if decrypted_msg_1 == encrypted_msg1:
        print("\n----DECRYPTION----\n")
        print("Layer 2 decryption Successful...\n")
        print((f"Layer 2 Contents:\n {decrypted_msg_1}\n\n"))

        decrypted_msg = decrypt(priv1, filename).decode("utf-8")
        if decrypted_msg == message.decode("utf-8"):
            print("Layer 1 decryption Successful...\n")
            print((f"plaintext:\n{decrypted_msg}\n\n"))
        else:
            print("Layer 1 decryption failed")
    else:
        print("Layer 2 decryption failed")


# Main function, runs the functions needed for the program to run
# Prints the function outputs to the screen.


def main():
    filename1 = "data1"
    filename2 = "data2"

    message = input("\nEnter message: ").encode("utf-8")
    encrypted_msg1 = encrypt(message, pub1, session_key1, filename1)
    encrypted_msg2 = encrypt(encrypted_msg1, pub2, session_key2, filename2)
    decrypted_msg_1 = decrypt(priv2, filename2)

    display(encrypted_msg1, encrypted_msg2, decrypted_msg_1, message, filename1)


if __name__ == "__main__":
    # Input for the encryption bytre size when generating keys, can be changed needs to be a multiple of 4, (1024 being the lowest value accepted)
    generate_keys(2048)
    priv1, pub1, priv2, pub2, session_key1, session_key2 = load_keys()

    while True:
        print_menu()
        option = ""
        try:
            option = int(input("Enter your choice: "))
        except:
            print("Wrong input. Please enter a number ...")

        if option == 1:
            main()
        elif option == 2:
            display_keys(pub1, pub2)

        elif option == 3:
            print("Exiting...")
            exit()
        else:
            print("Invalid option. Please enter a number between 1 and 3.")
