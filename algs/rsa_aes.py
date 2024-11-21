from base64 import b64encode, b64decode
from typing import Union

import numpy as np
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from PIL import Image

import my_utils
from my_utils import data_to_binary


def _encrypt_rsa(data: Union[bytes, str], public_key_path: str,
                 header: Union[bytes, str] = b'', sep: Union[bytes, str] = b';') -> bytes:
    if isinstance(data, str):
        data = data.encode('utf-8')
    if isinstance(header, str):
        header = header.encode('utf-8')
    if isinstance(sep, str):
        sep = sep.encode('utf-8')
    with open(public_key_path, 'rb') as file:
        public_key = file.read()
    cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
    encrypted = cipher.encrypt(data)
    return sep.join(b64encode(i) for i in [header, encrypted])


def _decrypt_rsa(data: bytes, private_key_path: str, sep: Union[bytes, str] = b';') -> tuple[bytes, bytes]:
    if isinstance(sep, str):
        sep = sep.encode('utf-8')
    header, encrypted = [b64decode(i) for i in data.split(sep)]
    with open(private_key_path, 'rb') as file:
        private_key = file.read()
    cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
    decrypted = cipher.decrypt(encrypted)
    return header, decrypted


def _encrypt_aes(data: Union[bytes, str], public_key_path: str,
                 header: Union[bytes, str] = b'', sep: Union[bytes, str] = b';',
                 key_size: int = 16) -> bytes:
    if isinstance(data, str):
        data = data.encode('utf-8')
    if isinstance(header, str):
        header = header.encode('utf-8')
    if isinstance(sep, str):
        sep = sep.encode('utf-8')
    aes_key = get_random_bytes(key_size)
    aes_key_encrypted = _encrypt_rsa(aes_key, public_key_path)
    cipher = AES.new(aes_key, AES.MODE_GCM)
    encrypted, tag = cipher.encrypt_and_digest(data)
    return sep.join(b64encode(i) for i in [header, aes_key_encrypted, cipher.nonce, tag, encrypted])


def _decrypt_aes(data: bytes, private_key_path: str, sep: Union[bytes, str] = b';') -> tuple[bytes, bytes]:
    if isinstance(sep, str):
        sep = sep.encode('utf-8')
    header, aes_key_encrypted, nonce, tag, encrypted = [b64decode(i) for i in data.split(sep)]
    _, aes_key = _decrypt_rsa(aes_key_encrypted, private_key_path)
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce)
    decrypted = cipher.decrypt_and_verify(encrypted, tag)
    return header, decrypted


def modify_pixels(pixels, data: bytes):
    binary_strings = data_to_binary(data)
    data_length = len(binary_strings)
    image_data = iter(pixels)
    for i in range(data_length):
        pixels = [value for value in next(image_data)[:3] + next(image_data)[:3] + next(image_data)[:3]]
        for j in range(0, 8):
            if binary_strings[i][j] == '0' and pixels[j] % 2 != 0:
                pixels[j] -= 1
            elif binary_strings[i][j] == '1' and pixels[j] % 2 == 0:
                if pixels[j] > 0:
                    pixels[j] -= 1
                else:
                    pixels[j] += 1
        if i == data_length - 1:
            if pixels[-1] % 2 == 0:
                if pixels[-1] > 0:
                    pixels[-1] -= 1
                else:
                    pixels[-1] += 1
        else:
            if pixels[-1] % 2 != 0:
                pixels[-1] -= 1
        pixels = tuple(pixels)
        yield pixels[0:3]
        yield pixels[3:6]
        yield pixels[6:9]


def encode(data: bytes, image_matrix: np.ndarray):
    image = Image.fromarray(np.reshape(image_matrix, np.array(image_matrix).shape))
    new_image = image.copy()
    width = new_image.size[0]
    x, y = 0, 0
    for pixel in modify_pixels(new_image.getdata(), data):
        new_image.putpixel((x, y), pixel)
        if x == width - 1:
            x = 0
            y += 1
        else:
            x += 1
    return np.array(new_image)


def decode(image_matrix: np.ndarray) -> bytes:
    image = Image.fromarray(np.reshape(image_matrix, np.array(image_matrix).shape))
    data = b''
    image_data = iter(image.getdata())
    while True:
        pixels = [value for value in next(image_data)[:3] + next(image_data)[:3] + next(image_data)[:3]]
        binary_string = ''
        for i in pixels[:8]:
            if i % 2 == 0:
                binary_string += '0'
            else:
                binary_string += '1'
        data += bytes((int(binary_string, 2),))
        if pixels[-1] % 2 != 0:
            return data


def generate_key_pair(size: int = 3072):
    key_pair = RSA.generate(size)
    private_key = key_pair.export_key()
    public_key = key_pair.public_key().export_key()
    return public_key, private_key


def get_header(data: bytes, sep: Union[bytes, str] = b';') -> bytes:
    if isinstance(sep, str):
        sep = sep.encode('utf-8')
    header, *_ = [b64decode(i) for i in data.split(sep)]
    return header


@my_utils.load_save_image(is_output_image=True)
def rsa_encrypt(image_matrix: np.ndarray, text: str, public_key_path: str):
    encrypted = _encrypt_rsa(text, public_key_path, 'rsa')
    return encode(encrypted, image_matrix)


@my_utils.load_save_image(is_output_image=True)
def aes_encrypt(image_matrix: np.ndarray, text: str, public_key_path: str,):
    encrypted = _encrypt_aes(text, public_key_path, 'aes')
    return encode(encrypted, image_matrix)


@my_utils.load_save_image(is_output_image=False)
def decrypt_image(image_matrix: np.ndarray, private_key_path: str):
    encrypted = decode(image_matrix)
    header = get_header(encrypted)
    if header == b"rsa":
        header, decrypted = _decrypt_rsa(encrypted, private_key_path)
    elif header == b"aes":
        header, decrypted = _decrypt_aes(encrypted, private_key_path)
    else:
        return "Непонятно что за алгоритм"
    return decrypted.decode()


if __name__ == "__main__":
    out_path_aes = aes_encrypt(image_path="../images/input/input_square.png", output_dir="../images/other",
                               image_name="aes1", text="АЕС шифрование жёсткое",
                               public_key_path="../keys/aes_rsa/public.pem")
    print(out_path_aes)
    print(decrypt_image(image_path=out_path_aes, private_key_path="../keys/aes_rsa/private.pem"))

    out_path_rsa = rsa_encrypt(image_path="../images/input/input_square.png", output_dir="../images/other",
                               image_name="rsa1", text="РСА шифрование жёсткое",
                               public_key_path="../keys/aes_rsa/public.pem")
    print(out_path_rsa)
    print(decrypt_image(image_path=out_path_rsa, private_key_path="../keys/aes_rsa/private.pem"))
