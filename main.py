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

def diff(a_art, b_art):
    return 0

if __name__ == "__main__":
    with open('target.art') as f:
        target_art = f.read()
    print("Target Art:")
    print(target_art)
    print()

    import os
    _, _, art_files = next(os.walk('./keys'))
    approx_file = './keys/' + sorted(art_files)[-1]

    with open(approx_file) as f:
        approx_art = f.read()
    print("Approx Art:")
    print(approx_art)
    print()

    print("Starting search...")
    private_key, public_key = generate_key()
    art = get_randomart(public_key)
    print(art)