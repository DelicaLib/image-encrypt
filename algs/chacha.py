import hashlib
import numpy as np
from Crypto.Cipher import ChaCha20
from PIL import Image

import my_utils


@my_utils.load_save_image(is_output_image=True)
def encrypt(image_matrix: np.ndarray, password: str):
    img = Image.fromarray(np.reshape(image_matrix, np.array(image_matrix).shape)).convert("RGB")
    pixel_data = list(img.getdata())
    encrypt_bytes = bytearray()
    for pixel in pixel_data:
        for value in pixel:
            encrypt_bytes.append(value)
    secret_key = hashlib.sha256(password.encode()).digest()[:32]
    cipher = ChaCha20.new(key=secret_key)
    ciphertext = cipher.nonce + cipher.encrypt(encrypt_bytes)
    new_img = Image.new('RGB', (img.width, img.height))
    new_img.frombytes(bytes(ciphertext))
    return np.array(new_img)


@my_utils.load_save_image(is_output_image=True)
def decrypt(image_matrix: np.ndarray, password: str):
    img = Image.fromarray(np.reshape(image_matrix, np.array(image_matrix).shape)).convert("RGB")
    pixel_data_de = list(img.getdata())
    byte_data_de = bytearray()
    for pixel in pixel_data_de:
        for value in pixel:
            byte_data_de.append(value)

    bytes_to_decrypt = byte_data_de + b'\0' * 8
    secret_key = hashlib.sha256(password.encode()).digest()[:32]
    msg_nonce = bytes_to_decrypt[:8]
    ciphertext = bytes_to_decrypt[8:]
    cipher = ChaCha20.new(key=secret_key, nonce=msg_nonce)
    decrypted_bytes = cipher.decrypt(ciphertext)
    decrypted_image = Image.new('RGB', (img.width, img.height))
    decrypted_image.frombytes(decrypted_bytes)
    return np.array(decrypted_image)


if __name__ == "__main__":
    out_path = encrypt(image_path="../images/input/input_square.png", output_dir="../images/other/",
                       image_name="chacha1", password="1234")
    print(out_path)
    print(decrypt(image_path=out_path, output_dir="../images/other",
                  image_name="chacha2", password="1234"))
