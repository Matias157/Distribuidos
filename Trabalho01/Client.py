
# Client 

import secrets
import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
# https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/

# RSA Algorithm

def generateAsymmetricKeys(exponent, keysize):
    private_key = rsa.generate_private_key(
    public_exponent=exponent,
    key_size=keysize,
    backend=default_backend()
    )
    public_key = private_key.public_key()

    return public_key, private_key

def signIn(username, password):
    # TODO: Sign In Method for logging users.


    return -1

def checkUsername(username):
    # TODO: Check username

    return -1

def signUp(username, password):
    # TODO: Sign Up Method for registering users.

    # TODO: Generate exponent e keysize randomly for each user. Use 'secrets' library for that.
    # userkeys = generateAsymmetricKeys(exponent, keysize)

    # TODO: Verify if current username is already taken.
    # storeUserCredentials(username, password, userkeys)

    return -1

def storeUserCredentials(username, password, userkeys):

    # Step 1 - Serialize keys created by RSA Algorithm.

    private_key = userkeys[1]
    public_key = userkeys[0]

    pvt_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
    )

    pb_key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # TODO: Create file to store user credentials.

    return -1

# # Sign a message
# message = b"A message I want to sign"
# signature = private_key.sign(
#     message,
#     padding.PSS(
#         mgf=padding.MGF1(hashes.SHA256()),
#         salt_length=padding.PSS.MAX_LENGTH
#     ),
#     hashes.SHA256()
# )

def loginMenu():
    logginMenu = True
    while(logginMenu):
        print(" Welcome to client.py ")
        print(" Please, Log In or Sign Up")
        print(" #1 - Log In")
        print(" #2 - Sign Up")
        print(" #0 - Leave")
        menu = input()

        if menu == '0':
            print(" Closing...")
            logginMenu = False
            sys.exit()

        elif menu == '1':
            print(" Please enter your credentials: ")
            usernameData = input('Username: ')
            passwordData = input('Password: ')

            # TODO: Check credentials.
            # TODO: If okay, move to next step

        
        elif menu == '2':
            print(' Please add your information: ')
            usernameData = input('Username: ')
            # TODO: Only continue when valid username.
            nameData = input('Name: ')
            passwordData = input('Password: ')

            # TODO: Save credentials, move to next step.
            

def main():

    # Step 1 - Login user
    loginMenu()

    # TODO: Step 2 - Menu for interaction.

    return -1

if __name__ == '__main__':
    main()
    
