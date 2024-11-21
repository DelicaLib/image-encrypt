from algs import affine_map, arnold_map, henon_map, logistic_map, pycasso_ed


def affine_arnold_encrypt(image_path: str, output_dir: str):
    output_image_path = affine_map.encrypt(image_path=image_path, output_dir=output_dir,
                                           image_name="affine_arnold_debug")
    return arnold_map.encrypt(image_path=output_image_path, output_dir=output_dir,
                              image_name="affine_arnold")


def affine_arnold_decrypt(image_path: str, output_dir: str):
    output_image_path = arnold_map.decrypt(image_path=image_path, output_dir=output_dir,
                                           image_name="affine_arnold_debug")
    return affine_map.decrypt(image_path=output_image_path, output_dir=output_dir,
                              image_name="affine_arnold")


def affine_henon_encrypt(image_path: str, output_dir: str):
    output_image_path = affine_map.encrypt(image_path=image_path, output_dir=output_dir,
                                           image_name="affine_henon")
    return henon_map.encrypt(image_path=output_image_path, output_dir=output_dir)


def affine_henon_decrypt(image_path: str, output_dir: str):
    output_image_path = henon_map.decrypt(image_path=image_path, output_dir=output_dir)
    return affine_map.decrypt(image_path=output_image_path, output_dir=output_dir)


def arnold_henon_encrypt(image_path: str, output_dir: str):
    output_image_path = arnold_map.encrypt(image_path=image_path, output_dir=output_dir,
                                           image_name="arnold_henon_debug")
    return henon_map.encrypt(image_path=output_image_path, output_dir=output_dir,
                             image_name="arnold_henon")


def arnold_henon_decrypt(image_path: str, output_dir: str):
    output_image_path = henon_map.decrypt(image_path=image_path, output_dir=output_dir)
    return arnold_map.decrypt(image_path=output_image_path, output_dir=output_dir)


def henon_logistic_encrypt(holder_path: str, image_path: str, output_dir: str):
    if output_dir[-1] != '/':
        output_dir += '/'
    holder_path, image_path = logistic_map.prepare_images(holder_path, image_path)
    output_image_path = henon_map.encrypt(image_path=image_path, output_dir=output_dir,
                                          image_name="henon_logistic_debug")
    return logistic_map.encrypt(image_path=holder_path, image2_path=output_image_path,
                                output_dir=output_dir, image_name="henon_logistic")


def henon_logistic_decrypt(image_path: str, number_of_pixels: int, output_dir: str):
    output_image_path = logistic_map.decrypt(image_path=image_path, output_dir=output_dir,
                                             number_of_pixels=number_of_pixels)
    return henon_map.decrypt(image_path=output_image_path, output_dir=output_dir)


def pycasso_logistic_encrypt(holder_path: str, image_path: str, output_dir: str):
    holder_path, image_path = logistic_map.prepare_images(holder_path, image_path)
    output_image_path = pycasso_ed.encrypt(image_path=image_path, output_dir=output_dir,
                                           image_name="pycasso_logistic_debug")
    return logistic_map.encrypt(image_path=holder_path, image2_path=output_image_path,
                                output_dir=output_dir, image_name="pycasso_logistic")


def pycasso_logistic_decrypt(image_path: str, number_of_pixels: int, output_dir: str):
    output_image_path = logistic_map.decrypt(image_path=image_path, output_dir=output_dir,
                                             number_of_pixels=number_of_pixels)
    return pycasso_ed.decrypt(image_path=output_image_path, output_dir=output_dir)
