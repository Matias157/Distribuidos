
# Client 

import secrets
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

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