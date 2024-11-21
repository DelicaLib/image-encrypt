import cv2
import numpy as np

import my_utils


def _encrypt(image_matrix: np.ndarray, debug: bool = False, max_iteration: int = 26):
    img = np.reshape(image_matrix, np.array(image_matrix).shape)
    encrypted_image = img.copy()
    for i in range(1, max_iteration):
        encrypted_image = encrypt_transform(encrypted_image, i, "../debug/encrypt/arnold/", debug)
    return np.array(encrypted_image.astype(np.uint8))


def _decrypt(image_matrix: np.ndarray, debug=False, max_iteration: int = 26):
    img = np.reshape(image_matrix, np.array(image_matrix).shape)
    decrypted_image = img.copy()
    for i in range(1, max_iteration):
        decrypted_image = decrypt_transform(decrypted_image, i, "../debug/decrypt/arnold/", debug)
    return np.array(decrypted_image.astype(np.uint8))


@my_utils.load_save_image(is_output_image=True)
def encrypt_tiles(image_matrix: np.ndarray, tile_size: int, debug=False, max_iteration: int = 26):
    tiles = my_utils.split_image_into_tiles(image_matrix, tile_size)
    res = tiles.copy()
    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            res[i][j] = _encrypt(tiles[i][j], debug=debug, max_iteration=max_iteration)
    return my_utils.join_tiles_into_image(res)


@my_utils.load_save_image(is_output_image=True)
def decrypt_tiles(image_matrix: np.ndarray, tile_size: int, debug=False, max_iteration: int = 26):
    tiles = my_utils.split_image_into_tiles(image_matrix, tile_size)
    res = tiles.copy()
    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            res[i][j] = _decrypt(tiles[i][j], debug=debug, max_iteration=max_iteration)
    return my_utils.join_tiles_into_image(res)


@my_utils.load_save_image(is_output_image=True)
def encrypt(image_matrix: np.ndarray, debug: bool = False, max_iteration: int = 26):
    return _encrypt(image_matrix, debug, max_iteration)


@my_utils.load_save_image(is_output_image=True)
def decrypt(image_matrix: np.ndarray, debug=False, max_iteration: int = 26):
    return _decrypt(image_matrix, debug, max_iteration)


def encrypt_transform(img, num, output_dir, debug):
    rows, cols, ch = img.shape
    if rows == cols:
        n = rows
        img2 = np.zeros([rows, cols, ch])

        for x in range(0, rows):
            for y in range(0, cols):

                img2[x][y] = img[(x+y) % n][(x+2*y) % n]
        if debug:
            cv2.imwrite(output_dir + str(num) + ".png", img2)
        return img2

    else:
        print("The image is not square.")


def decrypt_transform(img, num, output_dir, debug):
    rows, cols, ch = img.shape
    if rows == cols:
        n = rows
        img2 = np.zeros([rows, cols, ch])

        for x in range(0, rows):
            for y in range(0, cols):
                img2[(x + y) % n][(x + 2 * y) % n] = img[x][y]
        if debug:
            cv2.imwrite(output_dir + str(num) + ".png", img2)
        return img2

    else:
        print("The image is not square.")


if __name__ == "__main__":
    # out_path = encrypt(image_path="../images/input/input_square.png", output_dir="../images/other/",
    #                    image_name="arnold1")
    # print(out_path)
    # print(decrypt(image_path=out_path, output_dir="../images/other/",
    #               image_name="arnold2"))
    out_path = encrypt_tiles(image_path="../images/input/input_square.png", output_dir="../images/other/",
                             image_name="arnold_tiles1", tile_size=200)
    print(out_path)
    print(decrypt_tiles(image_path=out_path, output_dir="../images/other/",
                        image_name="arnold_tiles2", tile_size=200))
