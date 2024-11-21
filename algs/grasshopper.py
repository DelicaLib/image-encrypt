from PIL import Image
import numpy as np

import my_utils

translator = {
    'й': 'q',
    'ц': 'w',
    'у': 'e',
    'к': 'r',
    'е': 't',
    'н': 'y',
    'г': 'u',
    'ш': 'i',
    'щ': 'o',
    'з': 'p',
    'х': '[',
    'ъ': ']',
    'ф': 'a',
    'ы': 's',
    'в': 'd',
    'а': 'f',
    'п': 'g',
    'р': 'h',
    'о': 'j',
    'л': 'k',
    'д': 'l',
    'ж': ';',
    'э': '\'',
    'я': 'z',
    'ч': 'x',
    'с': 'c',
    'м': 'v',
    'и': 'b',
    'т': 'n',
    'ь': 'm',
    'б': ',',
    'ю': '.',
    'ё': '`',
    ' ': ' '
}
detranslator = {
    'q': 'й',
    'w': 'ц',
    'e': 'у',
    'r': 'к',
    't': 'е',
    'y': 'н',
    'u': 'г',
    'i': 'ш',
    'o': 'щ',
    'p': 'з',
    '[': 'х',
    ']': 'ъ',
    'a': 'ф',
    's': 'ы',
    'd': 'в',
    'f': 'а',
    'g': 'п',
    'h': 'р',
    'j': 'о',
    'k': 'л',
    'l': 'д',
    ';': 'ж',
    '\'': 'э',
    'z': 'я',
    'x': 'ч',
    'c': 'с',
    'v': 'м',
    'b': 'и',
    'n': 'т',
    'm': 'ь',
    ',': 'б',
    '.': 'ю',
    '`': 'ё',
    ' ': ' '
}


def __fill_msb(inp):
    inp = inp.split("b")[-1]
    inp = '0' * (7 - len(inp)) + inp
    return [int(x) for x in inp]


def __decrypt_pixels(pixels):
    pixels = [str(x % 2) for x in pixels]
    bin_repr = ''.join(pixels)
    return chr(int(bin_repr, 2))


def convert_into_eng(msg):
    res = ''
    for el in msg:
        if el in translator:
            res += translator[el]
        else:
            res += el
    return res


def convert_into_rus(msg):
    res = ''
    for el in msg:
        if el in detranslator:
            res += detranslator[el]
        else:
            res += el
    return res


@my_utils.load_save_image(is_output_image=True)
def encrypt(image: np.ndarray, msg: str, rus: int) -> np.array:
    if rus:
        msg = msg.lower()
        msg = convert_into_eng(msg)
        # print(msg)

    img = image
    img_arr = img.flatten()
    msg += "<-END->"
    msg_arr = [__fill_msb(bin(ord(ch))) for ch in msg]

    idx = 0
    for char in msg_arr:
        for bit in char:
            if bit == 1:
                if img_arr[idx] == 0:
                    img_arr[idx] = 1
                else:
                    img_arr[idx] = img_arr[idx] if img_arr[idx] % 2 == 1 else img_arr[idx] - 1
            else:
                if img_arr[idx] == 255:
                    img_arr[idx] = 254
                else:
                    img_arr[idx] = img_arr[idx] if img_arr[idx] % 2 == 0 else img_arr[idx] + 1
            idx += 1

    return img_arr


@my_utils.load_save_image(is_output_image=False)
def decrypt(image: np.ndarray, rus: int):
    img = image
    img_arr = np.array(img).flatten()

    decrypted_message = ""
    end_flag = False

    for i in range(7, len(img_arr), 7):
        decrypted_char = __decrypt_pixels(img_arr[i - 7:i])
        decrypted_message += decrypted_char

        if decrypted_message.find("<-END->") + 1:
            end_flag = True
            break

    if rus:
        msg = convert_into_rus(decrypted_message[:-7])
        # print(msg)
        return msg

    return decrypted_message[:-7] if end_flag else 'No message'


def convert_pict(image_path: str):
    im = Image.open(image_path)
    width, height = im.size
    mid = (width // 2, height // 2)
    # wid = 800, h = 600
    im_crop = im.crop((mid[0] - 399, mid[1] - 299, mid[0] + 399, mid[1] + 299))
    im_crop.save(image_path)


if __name__ == "__main__":
    # output_path = encrypt(image_path="../images/input/ims.png", output_dir="../images/other",
    #                       image_name="grasshopper1", msg="Я пидарас", rus=1)
    # print(output_path)
    print(decrypt(image_path="../images/input/ims.png", rus=1))
