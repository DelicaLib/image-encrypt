import numpy as np
from PIL import Image

import my_utils


@my_utils.load_save_image(is_output_image=True)
def encrypt(image_matrix: np.ndarray):
    im = Image.fromarray(np.reshape(image_matrix, np.array(image_matrix).shape))
    px = im.load()
    w, h = im.size

    y0 = 1
    x0 = 1
    n_cords = []

    for i in range(0, h * w):
        x = 1 - 1.4 * pow(x0, 2) + y0
        y = 0.3 * x0
        xr = int(('%.12f' % x)[5:9]) % w
        yr = int(('%.12f' % y)[5:9]) % h
        n_cords.append((xr, yr))
        x0 = float('%.14f' % x)
        y0 = float('%.14f' % y)

    n_cords.reverse()

    for i in range(0, h * w):
        (xr, yr) = n_cords[i]
        j = h * w - i - 1
        p = px[j % w, int(j / w)]
        pr = px[xr, yr]
        px[j % w, int(j / w)] = pr
        px[xr, yr] = p
    return np.array(im)


@my_utils.load_save_image(is_output_image=True)
def decrypt(image_matrix: np.ndarray):
    im = Image.fromarray(np.reshape(image_matrix, np.array(image_matrix).shape))
    px = im.load()
    w, h = im.size

    y0 = 1
    x0 = 1
    for i in range(0, h * w):
        x = 1 - 1.4 * pow(x0, 2) + y0
        y = 0.3 * x0
        x0 = float('%.14f' % x)
        y0 = float('%.14f' % y)
        xr = int(('%.11f' % x)[5:9]) % w
        yr = int(('%.11f' % y)[5:9]) % h

        p = px[i % w, int(i / w)]
        pr = px[xr, yr]
        px[i % w, int(i / w)] = pr
        px[xr, yr] = p
    return np.array(im)


if __name__ == "__main__":
    out_path = encrypt(image_path="../images/input/input_square.png", output_dir="../images/other",
                       image_name="henon1")
    print(out_path)
    print(decrypt(image_path=out_path, output_dir="../images/other",
                  image_name="henon2"))
