from io import BytesIO
import numpy as np
from PIL import Image
from pycasso import Canvas

import my_utils


@my_utils.load_save_image(is_output_image=True)
def encrypt(image_matrix: np.ndarray, seed: str = "seed", tile_width: int = 1, tile_height: int = 1):
    image_tmp = Image.fromarray(image_matrix)
    bytes_io = BytesIO()
    image_tmp.save(bytes_io, format="png")
    image_pil = Image.open(Canvas(bytes_io, (tile_width, tile_height), seed).export('scramble'))
    return np.array(image_pil)


@my_utils.load_save_image(is_output_image=True)
def decrypt(image_matrix: np.ndarray, seed: str = "seed", tile_width: int = 1, tile_height: int = 1):
    image_tmp = Image.fromarray(image_matrix)
    bytes_io = BytesIO()
    image_tmp.save(bytes_io, format="png")
    image_pil = Image.open(Canvas(bytes_io, (tile_width, tile_height), seed).export('unscramble'))
    return np.array(image_pil)


if __name__ == "__main__":
    out_path = encrypt(image_path="../images/input/input_square.png", output_dir="../images/other",
                       image_name="pycasso1", tile_width=70,
                       tile_height=70, seed="secret")
    print(out_path)
    print(decrypt(image_path=out_path, output_dir="../images/other",
                  image_name="pycasso2", tile_width=70,
                  tile_height=70, seed="secret"))
