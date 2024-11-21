import imutils
import numpy as np

import my_utils


@my_utils.load_save_image(is_output_image=True)
def encrypt(image_matrix: np.ndarray):
    img = np.reshape(image_matrix, np.array(image_matrix).shape)
    img_transformed = imutils.rotate(img, angle=90)
    return np.array(img_transformed)


@my_utils.load_save_image(is_output_image=True)
def decrypt(image_matrix: np.ndarray):
    img = np.reshape(image_matrix, np.array(image_matrix).shape)
    img_transformed = imutils.rotate(img, angle=-90)
    return np.array(img_transformed)


if __name__ == "__main__":
    out_path = encrypt(image_path="../images/input/input_square.png", output_dir="../images/other",
                       image_name="affine1")
    print(decrypt(image_path=out_path, output_dir="../images/other",
                  image_name="affine2"))
