from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# https://stackoverflow.com/a/39126754/43839
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/


def make_private_key():
    return rsa.generate_private_key(
        backend=default_backend(),
        public_exponent=65537,
        key_size=2048)


def public_key_string(private_key):
    return private_key.public_key().public_bytes(
        serialization.Encoding.OpenSSH,
        serialization.PublicFormat.OpenSSH
    ).decode()


def private_key_string(private_key):
    return private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()).decode()


def public_private_key():
    private_key = make_private_key()
    public = public_key_string(private_key)
    private = private_key_string(private_key)
    return public, private
