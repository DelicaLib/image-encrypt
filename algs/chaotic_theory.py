import hashlib
import numpy as np

import my_utils


def lorenz_system(x, y, z, sigma=10, rho=28, beta=8 / 3, dt=0.01):
    dx = sigma * (y - x) * dt
    dy = (x * (rho - z) - y) * dt
    dz = (x * y - beta * z) * dt
    return x + dx, y + dy, z + dz


def generate_chaotic_sequence(key: str, length):
    hashed_key = int(hashlib.sha256(key.encode()).hexdigest(), 16)
    seed = hashed_key % (2 ** 32 - 1)
    np.random.seed(seed)
    x, y, z = np.random.rand(3)
    chaotic_sequence = []
    for _ in range(length):
        x, y, z = lorenz_system(x, y, z)
        chaotic_sequence.append(x)

    return np.array(chaotic_sequence)


@my_utils.load_save_image(is_output_image=True, do_result_shape=False)
def encrypt_decrypt_image(image_matrix: np.ndarray, key: str):
    image_array = np.array(image_matrix)

    key_sequence = generate_chaotic_sequence(key, image_array.size)
    encrypted_image_array = np.bitwise_xor(image_array.flatten(), key_sequence.astype(np.uint8))
    return np.array(encrypted_image_array)


if __name__ == "__main__":
    out_path = encrypt_decrypt_image(image_path="../images/input/input_square.png", output_dir="../images/other/",
                                     image_name="chaotic1", key="password")
    print(out_path)
    print(encrypt_decrypt_image(image_path=out_path, output_dir="../images/other/",
                                image_name="chaotic2", key="password"))
