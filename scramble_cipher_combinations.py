import my_utils
from algs import rsa_aes, arnold_map, henon_map, chacha, chaotic_theory


def aes_arnold_encrypt(text: str, image_path: str, keys_dir: str, output_dir: str):
    output_image_path = rsa_aes.aes_encrypt(image_path=image_path, output_dir=output_dir,
                                            image_name="aes_arnold_debug", text=text,
                                            public_key_path=keys_dir + "public.pem")
    output_image_path = arnold_map.encrypt(image_path=output_image_path, output_dir=output_dir,
                                           image_name="aes_arnold")
    return output_image_path


def aes_rsa_arnold_decrypt(image_path: str, keys_dir: str, output_dir: str):
    output_image_path = arnold_map.decrypt(image_path=image_path, output_dir=output_dir)
    return rsa_aes.decrypt_image(image_path=output_image_path, private_key_path=keys_dir + "private.pem")


def rsa_arnold_encrypt(text: str, image_path: str, keys_dir: str, output_dir: str):
    output_image_path = rsa_aes.rsa_encrypt(image_path=image_path, output_dir=output_dir,
                                            image_name="rsa_arnold", text=text,
                                            public_key_path=keys_dir + "public.pem")
    output_image_path = arnold_map.encrypt(image_path=output_image_path, output_dir=output_dir)
    return output_image_path


def aes_rsa_generate_keys(output_dir: str = "keys/aes_rsa/"):
    if output_dir[-1] != '/':
        output_dir += '/'
    public_key, private_key = rsa_aes.generate_key_pair()
    my_utils.save_file(output_dir + "public.pem", public_key)
    my_utils.save_file(output_dir + "private.pem", private_key)
    return output_dir


def aes_henon_encrypt(text: str, image_path: str, keys_dir: str, output_dir: str):
    output_image_path = rsa_aes.aes_encrypt(image_path=image_path, output_dir=output_dir,
                                            image_name="aes_henon", text=text,
                                            public_key_path=keys_dir + "public.pem")
    output_image_path = henon_map.encrypt(image_path=output_image_path, output_dir=output_dir)
    return output_image_path


def aes_rsa_henon_decrypt(image_path: str, keys_dir: str, output_dir: str):
    output_image_path = henon_map.decrypt(image_path=image_path, output_dir=output_dir)
    return rsa_aes.decrypt_image(image_path=output_image_path, private_key_path=keys_dir + "private.pem")


def rsa_henon_encrypt(text: str, image_path: str, keys_dir: str, output_dir: str):
    output_image_path = rsa_aes.rsa_encrypt(image_path=image_path, output_dir=output_dir,
                                            image_name="rsa_henon", text=text,
                                            public_key_path=keys_dir + "public.pem")
    output_image_path = henon_map.encrypt(image_path=output_image_path, output_dir=output_dir)
    return output_image_path


def chacha_arnold_encrypt(image_path: str, password: str, output_dir: str):
    output_image_path = arnold_map.encrypt(image_path=image_path, output_dir=output_dir,
                                           image_name="chacha_arnold_debug")
    return chacha.encrypt(image_path=output_image_path, output_dir=output_dir,
                          image_name="chacha_arnold", password=password)


def chacha_henon_encrypt(image_path: str, password: str, output_dir: str):
    output_image_path = henon_map.encrypt(image_path=image_path, output_dir=output_dir,
                                          image_name="chacha_henon_debug")
    return chacha.encrypt(image_path=output_image_path, output_dir=output_dir,
                          image_name="chacha_henon", password=password)


def chacha_arnold_decrypt(image_path: str, password: str, output_dir: str):
    output_image_path = chacha.decrypt(image_path=image_path, output_dir=output_dir,
                                       password=password)
    return arnold_map.decrypt(image_path=output_image_path, output_dir=output_dir)


def chacha_henon_decrypt(image_path: str, password: str, output_dir: str):
    output_image_path = chacha.decrypt(image_path=image_path, output_dir=output_dir,
                                       password=password)
    return henon_map.decrypt(image_path=output_image_path, output_dir=output_dir)


def chaotic_arnold_encrypt(image_path: str, password: str, output_dir: str):
    output_image_path = chaotic_theory.encrypt_decrypt_image(image_path=image_path, output_dir=output_dir,
                                                             image_name="chaotic_arnold_debug", key=password)
    return arnold_map.encrypt(image_path=output_image_path, output_dir=output_dir,
                              image_name="chaotic_arnold")


def chaotic_henon_encrypt(image_path: str, password: str, output_dir: str):
    output_image_path = chaotic_theory.encrypt_decrypt_image(image_path=image_path, output_dir=output_dir,
                                                             image_name="chaotic_henon_debug", key=password)
    return henon_map.encrypt(image_path=output_image_path, output_dir=output_dir,
                             image_name="chaotic_henon")


def chaotic_arnold_decrypt(image_path: str, password: str, output_dir: str):
    output_image_path = arnold_map.decrypt(image_path=image_path, output_dir=output_dir)
    return chaotic_theory.encrypt_decrypt_image(image_path=output_image_path, output_dir=output_dir,
                                                key=password)


def chaotic_henon_decrypt(image_path: str, password: str, output_dir: str):
    output_image_path = henon_map.decrypt(image_path=image_path, output_dir=output_dir)
    return chaotic_theory.encrypt_decrypt_image(image_path=output_image_path, output_dir=output_dir,
                                                key=password)
