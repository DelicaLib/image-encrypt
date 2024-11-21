from algs import arnold_map


def tiles_arnold_arnold_encrypt(image_path: str, output_dir: str,
                                tile_size: int = 10, max_iteration: int = 26):
    output_image_path = arnold_map.encrypt_tiles(image_path=image_path, output_dir=output_dir,
                                                 image_name="tiles_arnold_arnold_debug", tile_size=tile_size,
                                                 max_iteration=max_iteration)
    return arnold_map.encrypt(image_path=output_image_path, output_dir=output_dir,
                              image_name="tiles_arnold_arnold", max_iteration=max_iteration)


def tiles_arnold_arnold_decrypt(image_path: str, output_dir: str,
                                tile_size: int = 10, max_iteration: int = 26):
    output_image_path = arnold_map.decrypt(image_path=image_path, output_dir=output_dir,
                                           image_name="tiles_arnold_arnold_debug", max_iteration=max_iteration)
    return arnold_map.decrypt_tiles(image_path=output_image_path, output_dir=output_dir,
                                    image_name="tiles_arnold_arnold", tile_size=tile_size,
                                    max_iteration=max_iteration)
