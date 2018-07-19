import binascii
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa, utils

# https://stackoverflow.com/a/39126754/43839
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/

KEY_SIZE = 2048
PUBLIC_EXPONENT = 65537
BACKEND = default_backend()


def make_private_key():
    """Return a new RSA private key"""
    return rsa.generate_private_key(
        backend=BACKEND,
        public_exponent=PUBLIC_EXPONENT,
        key_size=KEY_SIZE)


def public_key_string(private_key):
    return private_key.public_key().public_bytes(
        serialization.Encoding.OpenSSH,
        serialization.PublicFormat.OpenSSH,
    ).decode()


def private_key_string(private_key):
    return private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption()).decode()


def public_private_key():
    private_key = make_private_key()
    public = public_key_string(private_key)
    private = private_key_string(private_key)
    return public, private


def string_to_private_key(str):
    s = str.encode()
    return serialization.load_pem_private_key(s, password=None, backend=BACKEND)


def _make_padding():
    return padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH)


def sign(private_key, hexdigest):
    digest = bytes.fromhex(hexdigest)
    pad = _make_padding()
    prehashed = utils.Prehashed(hashes.SHA256())
    return to_hex(private_key.sign(digest, pad, prehashed))


def verify(private_key, hexdigest, signature):
    sig = bytes.fromhex(signature)
    digest = bytes.fromhex(hexdigest)
    pad = _make_padding()
    prehashed = utils.Prehashed(hashes.SHA256())
    public_key = private_key.public_key()

    return public_key.verify(sig, digest, pad, prehashed)


def to_hex(s):
    # For Python 3.4 compatibility
    return binascii.hexlify(s).decode()
