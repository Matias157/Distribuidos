
# Client 

import cryptography
from cryptography.hazmat.primitives.asymmetric import rsa

# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/

# RSA Algorithm

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)



