import numpy as np
import math

import my_utils


def prepare_images(holder_path: str, image_path: str):
    my_utils.make_square(holder_path, "images/other/tmp_holder.png", 1024, min_size=1024)
    my_utils.make_square(image_path, "images/other/tmp_image.png", max_size=256)
    return "images/other/tmp_holder.png", "images/other/tmp_image.png"


def read_img(image_matrix: np.ndarray):
    res = []
    for i in range(len(image_matrix)):
        for j in range(len(image_matrix[i])):
            res.append([])
            for k in range(len(image_matrix[i][j])):
                res[-1].append('{0:08b}'.format(image_matrix[i][j][k]))
    return res


def logistic_gen(lamb, x_node):
    x_next = x_node
    while True:
        x_next = lamb * x_next * (1 - x_next)
        binary_x = eval(str(x_next)[str(x_next).find('.') + 1:].lstrip('0'))
        binary_x = bin(int(binary_x)).replace("0b", "")
        yield binary_x


def dtb_lengthier(value):
    x = value
    if len(value) < 8:
        filler = '0' * (8 - len(x))
        filler += x
        x = filler
    return x


def permute(pixel, s1, s2):
    new_pixel = []
    if s1 == 0 and s2 == 0:
        new_pixel = pixel
    elif s1 == 0 and s2 == 1:
        new_pixel.extend([pixel[2], pixel[0], pixel[1]])
    elif s1 == 1 and s2 == 0:
        new_pixel.extend([pixel[1], pixel[2], pixel[0]])
    elif s1 == 1 and s2 == 1:
        new_pixel.extend([pixel[2], pixel[1], pixel[0]])
    return tuple(new_pixel)


def unpermute(pixel, s1, s2):
    new_pixel = []
    if s1 == 0 and s2 == 0:
        new_pixel = pixel
    elif s1 == 0 and s2 == 1:
        new_pixel.extend([pixel[1], pixel[2], pixel[0]])
    elif s1 == 1 and s2 == 0:
        new_pixel.extend([pixel[2], pixel[0], pixel[1]])
    elif s1 == 1 and s2 == 1:
        new_pixel.extend([pixel[2], pixel[1], pixel[0]])
    return tuple(new_pixel)


def _encrypt(pixel_matrix):
    gen = logistic_gen(4, 0.2)
    new_pixel_matrix = []
    for pixel in pixel_matrix:
        new_pixel = []
        crypt1 = next(gen)
        crypt2 = next(gen)
        crypt3 = next(gen)
        s1, s2 = (int(crypt1[-1], 2) ^ int(crypt2[-1], 2) ^ int(crypt3[-1], 2),
                  int(crypt1[-2], 2) ^ int(crypt2[-2], 2) ^ int(crypt3[-2], 2))
        pixel = permute(pixel, s1, s2)
        # print(pixel)
        new_pixel.append(dtb_lengthier(bin(int(pixel[0], 2) ^ int(
            crypt1[-8:], 2)).replace('0b', '')))
        # print(int(crypt3[-8:], 2))
        new_pixel.append(dtb_lengthier(bin(int(pixel[1], 2) ^ int(
            crypt2[-8:], 2)).replace('0b', '')))
        new_pixel.append(dtb_lengthier(bin(int(pixel[2], 2) ^ int(
            crypt3[-8:], 2)).replace('0b', '')))
        new_pixel_matrix.append(new_pixel)
    return new_pixel_matrix


def _decrypt(pixel_matrix):
    gen = logistic_gen(4, 0.2)
    new_pixel_matrix = []
    for pixel in pixel_matrix:
        new_pixel = []
        crypt1 = next(gen)
        crypt2 = next(gen)
        crypt3 = next(gen)
        s1, s2 = (int(crypt1[-1], 2) ^ int(crypt2[-1], 2) ^ int(crypt3[-1], 2),
                  int(crypt1[-2], 2) ^ int(crypt2[-2], 2) ^ int(crypt3[-2], 2))
        new_pixel.append(dtb_lengthier(bin(int(pixel[0], 2) ^ int(
            crypt1[-8:], 2)).replace('0b', '')))
        # print(int(crypt3[-8:], 2))
        new_pixel.append(dtb_lengthier(bin(int(pixel[1], 2) ^ int(
            crypt2[-8:], 2)).replace('0b', '')))
        new_pixel.append(dtb_lengthier(bin(int(pixel[2], 2) ^ int(
            crypt3[-8:], 2)).replace('0b', '')))
        # print(s1, s2)
        new_pixel = unpermute(new_pixel, s1, s2)
        new_pixel_matrix.append(list(new_pixel))
    return new_pixel_matrix


def alter_img(img_matrix):
    matrix = img_matrix[:]
    for pixel in matrix:
        pixel[0] = int(pixel[0], 2)
        pixel[1] = int(pixel[1], 2)
        pixel[2] = int(pixel[2], 2)
        if (int(pixel[0]) not in range(0, 256) or
                int(pixel[1]) not in range(0, 256) or
                int(pixel[2]) not in range(0, 256)):
            input('Error')
    data = np.array(matrix)
    dim = int(math.sqrt(len(img_matrix)))
    shape = (dim, dim, 3)
    data = data.reshape(shape)
    data_sub = data.astype(np.uint8)
    return np.array(data_sub)


@my_utils.load_save_image(is_output_image=False, count_image=2)
def encrypt(holder_matrix: np.ndarray, image_matrix: np.array):
    holder_img = read_img(holder_matrix)
    input_img = read_img(image_matrix)

    input_img = _encrypt(input_img)
    i = 0
    for pixel in input_img:
        for x in range(8):
            holder_img[i + x][0] = holder_img[i + x][0][:-1] + pixel[0][x]
            holder_img[i + x][1] = holder_img[i + x][1][:-1] + pixel[1][x]
            holder_img[i + x][2] = holder_img[i + x][2][:-1] + pixel[2][x]
        i += 8

    return alter_img(holder_img), i


@my_utils.load_save_image(is_output_image=True)
def decrypt(holder_matrix: np.ndarray, number_of_pixels: int):
    holder = read_img(np.reshape(holder_matrix, np.array(holder_matrix).shape))
    new_img = []
    for x in range(number_of_pixels // 8):
        new_pix_r = ''
        new_pix_g = ''
        new_pix_b = ''
        for j in range(8):
            new_pix_r += holder[x * 8 + j][0][-1]
            new_pix_g += holder[x * 8 + j][1][-1]
            new_pix_b += holder[x * 8 + j][2][-1]
        new_img.append([new_pix_r, new_pix_g, new_pix_b])

    new_img = _decrypt(new_img)
    for pixel in new_img:
        pixel[0] = int(pixel[0], 2)
        pixel[1] = int(pixel[1], 2)
        pixel[2] = int(pixel[2], 2)
        if (int(pixel[0]) not in range(0, 256) or
                int(pixel[1]) not in range(0, 256) or
                int(pixel[2]) not in range(0, 256)):
            input('Error')
    data = np.array(new_img)
    dim = int(math.sqrt(number_of_pixels // 8))
    shape = (dim, dim, 3)
    data = data.reshape(shape)
    data_sub = data.astype(np.uint8)

    return np.array(data_sub)


if __name__ == "__main__":
    def main():
        holder_path, image_path = prepare_images("../images/input/input.png", "images/input/input2.png")
        out_path, number_of_pixels = encrypt(image_path=holder_path, image2_path=image_path,
                                             output_dir="../images/other", image_name="logistic1")
        print(out_path, number_of_pixels)
        print(decrypt(image_path=out_path, output_dir="../images/other",
                      image_name="logistic2", number_of_pixels=number_of_pixels))
    main()
