from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization as crypto_serialization


def generate_key():
    # Generate an Ed25519 private key
    key = ed25519.Ed25519PrivateKey.generate()

    # Serialize the private key to PEM format
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption(),
    )

    # Serialize the public key to OpenSSH format
    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH,
    )

    return private_key, public_key
