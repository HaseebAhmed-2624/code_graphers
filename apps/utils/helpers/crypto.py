import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class CryptoHelperUtils:
    class Symmetric:
        class AES:
            class CBC:
                @staticmethod
                def encrypt(plain_text: str, key: str, iv: str = None):
                    # Convert to bytes and pads by 16 for AES block size
                    data = pad(plain_text.encode('utf-8'), 16)
                    # Creates an AES CBS cipher
                    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC,
                                     (iv and iv.encode("utf-8")) or get_random_bytes(16))
                    # Encrypt the padded data using the AES cipher and encode the result as a base64 string, then convert to string for return
                    cipher_text, iv = base64.b64encode(cipher.encrypt(data)).decode(
                        'utf-8'), base64.b64encode(cipher.iv).decode(
                        'utf-8')
                    return {
                        "cipher_text": cipher_text,
                        "iv": iv
                    }
                @staticmethod
                def decrypt(cipher_text: str, key: str, iv: str):
                    enc = base64.b64decode(cipher_text.encode('utf-8'))
                    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, base64.b64decode(iv.encode('utf-8')))
                    return {
                        "plain_text": unpad(cipher.decrypt(enc), 16).decode('utf-8')
                    }
