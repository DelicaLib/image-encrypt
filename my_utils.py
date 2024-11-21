import os
from typing import Optional

import cv2
import re

import numpy as np
from PIL import Image
from functools import wraps


def save_image(output_dir, output_image, image_name="output.png"):
    if output_dir[-1] != '/':
        output_dir += '/'
    if output_image is not None:
        cv2.imwrite(output_dir + image_name, output_image)
        return output_dir + image_name


def save_file(path: str, data: bytes):
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'xb') as file:
        file.write(data)


def get_image_name(image_path):
    tmp = re.split(r"/|\.", image_path)
    if len(tmp) > 2:
        return tmp[-2]


def data_to_binary(data: bytes) -> list:
    binary_strings = []
    for i in data:
        binary_strings.append(format(i, '08b'))
    return binary_strings


def make_square(old_path, new_path, max_size=600, fill_color=(0, 0, 0), min_size=0):
    # find image dimensions
    old_img = Image.open(old_path)
    size = (min(max_size, max(old_img.size)),) * 2
    size = (max(min_size, size[0]),) * 2
    # resize if old image is larger than max_size
    if size[0] < old_img.size[0] or size[1] < old_img.size[1]:
        old_img.thumbnail(size)

    # create new image with the given color and computed size
    new_img = Image.new(old_img.mode, size, fill_color)

    # find coordinates of upper-left corner to center the old image in the new image
    assert new_img.size[0] >= old_img.size[0]
    assert new_img.size[1] >= old_img.size[1]

    x = (new_img.size[0] - old_img.size[0]) // 2
    y = (new_img.size[1] - old_img.size[1]) // 2

    # paste image
    new_img.paste(old_img, (x, y))

    # save image
    new_img.save(new_path)


def split_image_into_tiles(image_matrix: np.ndarray, tile_size: int):
    tile_size = len(image_matrix) // np.ceil(len(image_matrix) / tile_size).astype('int')
    res = []
    for tile_i in range(len(image_matrix) // tile_size):
        res.append([])
        for tile_j in range(len(image_matrix) // tile_size):
            tile = []
            for i in range(tile_size):
                tile.append([])
                for j in range(tile_size):
                    tile[-1].append(image_matrix[tile_i*tile_size + i][tile_j*tile_size + j])
            res[-1].append(tile.copy())
    return np.array(res)


def join_tiles_into_image(tiles_matrix: np.ndarray):
    tile_size = len(tiles_matrix[0][0])
    res = []
    for _ in range(tile_size):
        for _ in range(len(tiles_matrix)):
            res.append([])
            for _ in range(tile_size):
                for _ in range(len(tiles_matrix)):
                    res[-1].append(None)
    for tile_i in range(len(tiles_matrix)):
        for tile_j in range(len(tiles_matrix)):
            for i in range(tile_size):
                for j in range(tile_size):
                    res[tile_i*tile_size + i][tile_j*tile_size + j] = tiles_matrix[tile_i][tile_j][i][j]
    return np.array(res)


def load_save_image(is_output_image: bool = True, count_image: int = 1, do_result_shape: bool = True):
    def decorator(func):
        @wraps(func)
        def wrapper(image_path: str, image2_path: Optional[str] = None,
                    output_dir: Optional[str] = None, image_name: Optional[str] = None,
                    *args, **kwargs):
            if count_image == 2 and image2_path is None:
                raise ValueError("count_image == 2, а image2_path не задан")
            if output_dir is None and is_output_image:
                raise ValueError("output_dir не задан")
            if image_name is None and is_output_image:
                image_name = get_image_name(image_path)
            if output_dir is not None and output_dir[-1] != '/':
                output_dir += '/'
            image_matrix = np.array(Image.open(image_path))
            if count_image == 2:
                image2_matrix = np.array(Image.open(image2_path))
                result = func(image_matrix, image2_matrix, *args, **kwargs)
            else:
                result = func(image_matrix, *args, **kwargs)
            if not is_output_image:
                if count_image == 2:
                    result_image = Image.fromarray(np.reshape(result[0], np.array(result[0]).shape))
                    result_image.save(output_dir + image_name + ".png", optimize=False, progressive=False, quality=100)
                    return output_dir + image_name + ".png", result[1]
                return result
            if do_result_shape:
                image_matrix = result
            result_image = Image.fromarray(np.reshape(result, np.array(image_matrix).shape))
            result_image.save(output_dir + image_name + ".png", optimize=False, progressive=False, quality=100)
            return output_dir + image_name + ".png"
        return wrapper
    return decorator


if __name__ == "__main__":
    def main():
        matrix = [[1, 2, 3, 4, 5, 6],
                  [7, 8, 9, 10, 11, 12],
                  [13, 14, 15, 16, 17, 18],
                  [19, 20, 21, 22, 23, 24],
                  [25, 26, 27, 28, 29, 30],
                  [31, 32, 33, 34, 35, 36]]
        print(split_image_into_tiles(np.array(matrix), 3))
        print(join_tiles_into_image((split_image_into_tiles(np.array(matrix), 3))))
    main()
