from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization

def generate_key():
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537, # RFC 4871, don't change it
        key_size=4096 # standard strong key, as suggested by GitHub
    )
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption())
    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )
    return private_key, public_key

from randomart import get_randomart

if __name__ == "__main__":
    # private_key, public_key = generate_key()
    public_key = bytes(input(), 'utf-8')
    art = get_randomart(public_key)
    print(art)
