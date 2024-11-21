from enum import Enum

import tiles_scramble
from scramble_combinations import *
from scramble_cipher_combinations import *


class TypeOfFunction(Enum):
    aes_arnold_encrypt = 1
    rsa_arnold_encrypt = 2
    aes_rsa_arnold_decrypt = 3
    aes_rsa_generate_keys = 4
    aes_henon_encrypt = 5
    rsa_henon_encrypt = 6
    aes_rsa_henon_decrypt = 7
    chacha_henon_encrypt = 8
    chacha_arnold_encrypt = 9
    chacha_henon_decrypt = 10
    chacha_arnold_decrypt = 11
    chaotic_henon_encrypt = 12
    chaotic_arnold_encrypt = 13
    chaotic_henon_decrypt = 14
    chaotic_arnold_decrypt = 15
    affine_arnold_encrypt = 16
    affine_arnold_decrypt = 17
    affine_henon_encrypt = 18
    affine_henon_decrypt = 19
    arnold_henon_encrypt = 20
    arnold_henon_decrypt = 21
    henon_logistic_encrypt = 22
    henon_logistic_decrypt = 23
    pycasso_logistic_encrypt = 24
    pycasso_logistic_decrypt = 25
    arnold_tiles_arnold_encrypt = 26
    arnold_tiles_arnold_decrypt = 27


def _input_info_encrypt():
    print("""Напишите нужную цифру:
    1. сгенерировать ключи для aes/rsa
    2. aes + arnold map (Спрятать текст в картинке)
    3. rsa + arnold map (Спрятать текст в картинке)
    4. aes + henon map (Спрятать текст в картинке)
    5. rsa + henon map (Спрятать текст в картинке)
    6. chacha20 + arnold map (Зашифровать картинку)
    7. chacha20 + henon map (Зашифровать картинку)
    8. теория хаоса + arnold map (Зашифровать картинку)
    9. теория хаоса + henon map (Зашифровать картинку)""")
    choice = input()
    if choice == "2":
        return TypeOfFunction.aes_arnold_encrypt
    elif choice == "3":
        return TypeOfFunction.rsa_arnold_encrypt
    elif choice == "1":
        return TypeOfFunction.aes_rsa_generate_keys
    elif choice == "4":
        return TypeOfFunction.aes_henon_encrypt
    elif choice == "5":
        return TypeOfFunction.rsa_henon_encrypt
    elif choice == "6":
        return TypeOfFunction.chacha_arnold_encrypt
    elif choice == "7":
        return TypeOfFunction.chacha_henon_encrypt
    elif choice == "8":
        return TypeOfFunction.chaotic_arnold_encrypt
    elif choice == "9":
        return TypeOfFunction.chaotic_henon_encrypt
    else:
        return None


def _input_info_decrypt():
    print("""Напишите нужную цифру:
    1. aes/rsa + arnold map
    2. aes/rsa + henon map
    3. chacha20 + arnold map
    4. chacha20 + henon map
    5. теория хаоса + arnold map
    6. теория хаоса + henon map
    7. affine map + arnold map
    8. affine map + henon map
    9. arnold map + henon map
    10. henon map + logistic map
    11. pycasso + logistic map""")
    choice = input()
    if choice == "1":
        return TypeOfFunction.aes_rsa_arnold_decrypt
    if choice == "2":
        return TypeOfFunction.aes_rsa_henon_decrypt
    if choice == "3":
        return TypeOfFunction.chacha_arnold_decrypt
    if choice == "4":
        return TypeOfFunction.chacha_henon_decrypt
    if choice == "5":
        return TypeOfFunction.chaotic_arnold_decrypt
    if choice == "6":
        return TypeOfFunction.chaotic_henon_decrypt
    if choice == "7":
        return TypeOfFunction.affine_arnold_decrypt
    if choice == "8":
        return TypeOfFunction.affine_henon_decrypt
    if choice == "9":
        return TypeOfFunction.arnold_henon_decrypt
    if choice == "10":
        return TypeOfFunction.henon_logistic_decrypt
    if choice == "11":
        return TypeOfFunction.pycasso_logistic_decrypt
    else:
        return None


def _input_info_scramble():
    print("""Напишите нужную цифру:
    1. affine map + arnold map
    2. affine map + henon map
    3. arnold map + henon map
    4. henon map + logistic map (спрятать картинку в картинке)
    5. pycasso + logistic map (спрятать картинку в картинке)""")
    choice = input()
    if choice == "1":
        return TypeOfFunction.affine_arnold_encrypt
    elif choice == "2":
        return TypeOfFunction.affine_henon_encrypt
    elif choice == "3":
        return TypeOfFunction.arnold_henon_encrypt
    elif choice == "4":
        return TypeOfFunction.henon_logistic_encrypt
    elif choice == "5":
        return TypeOfFunction.pycasso_logistic_encrypt
    else:
        return None


def _input_info_tiles_scramble():
    print("""Напишите нужную цифру:
        1. arnold tiles + arnold map""")
    choice = input()
    if choice == "1":
        return TypeOfFunction.arnold_tiles_arnold_encrypt
    else:
        return None


def _input_info_tiles_decrypt():
    print("""Напишите нужную цифру:
    1. arnold tiles + arnold map""")
    choice = input()
    if choice == "1":
        return TypeOfFunction.arnold_tiles_arnold_decrypt
    else:
        return None


def _input_info_combinations():
    print("""Напишите нужную цифру:
    1 - зашифровать 
    2 - заскремблировать 
    3 - расшифровать""")
    choice = input()
    if choice == "1":
        return _input_info_encrypt()
    elif choice == "2":
        return _input_info_scramble()
    elif choice == "3":
        return _input_info_decrypt()
    else:
        return None


def _input_info_tiles():
    print("""Напишите нужную цифру:
    1 - зашифровать 
    2 - заскремблировать 
    3 - расшифровать""")
    choice = input()
    if choice == "1":
        return _input_info_encrypt()
    elif choice == "2":
        return _input_info_tiles_scramble()
    elif choice == "3":
        return _input_info_tiles_decrypt()
    else:
        return None


def input_info():
    print("""Напишите нужную цифру:
        1 - Одиночные алгоритмы скремблирования
        2 - Одиночные алгоритмы шифрования 
        3 - Комбинации алгоритмов
        4 - Поблочные алгоритмы""")
    choice = input()
    if choice == "1":
        return None
    elif choice == "2":
        return None
    elif choice == "3":
        return _input_info_combinations()
    elif choice == "3":
        return _input_info_combinations()
    elif choice == "4":
        return _input_info_tiles()
    else:
        return None


def main():
    print()
    print("Проверьте наличие необходимого изображения в images/input/input.png")
    print("""Если вы планируете использовать алгоритм, который прячет картинку в картинке, 
то проверьте images/input/input2.png
Это изображение будет спрятано в images/input/input.png""")
    input("Если всё готово, нажмите Enter...")
    print()
    my_utils.make_square("images/input/input.png", "images/input/input_square.png")
    choice = input_info()
    if choice is None:
        print("Неизвестная команда")
        exit(0)
    if choice == TypeOfFunction.aes_rsa_generate_keys:
        output_dir = aes_rsa_generate_keys()
        print(f"Сохранено в {output_dir}")
    elif choice == TypeOfFunction.aes_arnold_encrypt:
        print("Введите текст, который хотите зашифровать:")
        text = input()
        output_image_path = aes_arnold_encrypt(text, "images/input/input_square.png",
                                               "keys/aes_rsa/", "images/output/")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.rsa_arnold_encrypt:
        print("Введите текст, который хотите зашифровать:")
        text = input()
        output_image_path = rsa_arnold_encrypt(text, "images/input/input_square.png",
                                               "keys/aes_rsa/", "images/output/")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.aes_rsa_arnold_decrypt:
        print("Введите путь к изображению")
        image_path = input()
        text = aes_rsa_arnold_decrypt(image_path, "keys/aes_rsa/", "images/output/decrypt/")
        if text is None:
            print("Хз вообще")
        else:
            print(text)
    elif choice == TypeOfFunction.aes_henon_encrypt:
        print("Введите текст, который хотите зашифровать:")
        text = input()
        output_image_path = aes_henon_encrypt(text, "images/input/input_square.png",
                                              "keys/aes_rsa/", "images/output/")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.rsa_henon_encrypt:
        print("Введите текст, который хотите зашифровать:")
        text = input()
        output_image_path = rsa_henon_encrypt(text, "images/input/input_square.png",
                                              "keys/aes_rsa/", "images/output/")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.aes_rsa_henon_decrypt:
        print("Введите путь к изображению")
        image_path = input()
        text = aes_rsa_henon_decrypt(image_path, "keys/aes_rsa/", "images/output/decrypt/")
        if text is None:
            print("Хз вообще")
        else:
            print(text)
    elif choice == TypeOfFunction.chacha_arnold_encrypt:
        print("Введите пароль шифрования")
        password = input()
        output_image_path = chacha_arnold_encrypt("images/input/input_square.png", password, "images/output")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.chacha_arnold_decrypt:
        print("Введите путь к изображению")
        image_path = input()
        print("Введите пароль шифрования")
        password = input()
        output_image_path = chacha_arnold_decrypt(image_path, password, "images/output/decrypt")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.chacha_henon_encrypt:
        print("Введите пароль шифрования")
        password = input()
        output_image_path = chacha_henon_encrypt("images/input/input_square.png", password, "images/output")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.chacha_henon_decrypt:
        print("Введите путь к изображению")
        image_path = input()
        print("Введите пароль шифрования")
        password = input()
        output_image_path = chacha_henon_decrypt(image_path, password, "images/output/decrypt")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.chaotic_arnold_encrypt:
        print("Введите пароль шифрования")
        password = input()
        output_image_path = chaotic_arnold_encrypt("images/input/input_square.png", password, "images/output")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.chaotic_arnold_decrypt:
        print("Введите путь к изображению")
        image_path = input()
        print("Введите пароль шифрования")
        password = input()
        output_image_path = chaotic_arnold_decrypt(image_path, password, "images/output/decrypt")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.chaotic_henon_encrypt:
        print("Введите пароль шифрования")
        password = input()
        output_image_path = chaotic_henon_encrypt("images/input/input_square.png", password, "images/output")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.chaotic_henon_decrypt:
        print("Введите путь к изображению")
        image_path = input()
        print("Введите пароль шифрования")
        password = input()
        output_image_path = chaotic_henon_decrypt(image_path, password, "images/output/decrypt")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.affine_arnold_encrypt:
        output_image_path = affine_arnold_encrypt("images/input/input_square.png", "images/output")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.affine_arnold_decrypt:
        print("Введите путь к изображению")
        image_path = input()
        output_image_path = affine_arnold_decrypt(image_path, "images/output/decrypt")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.affine_henon_encrypt:
        output_image_path = affine_henon_encrypt("images/input/input_square.png", "images/output")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.affine_henon_decrypt:
        print("Введите путь к изображению")
        image_path = input()
        output_image_path = affine_henon_decrypt(image_path, "images/output/decrypt")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.arnold_henon_encrypt:
        output_image_path = arnold_henon_encrypt("images/input/input_square.png", "images/output")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.arnold_henon_decrypt:
        print("Введите путь к изображению")
        image_path = input()
        output_image_path = arnold_henon_decrypt(image_path, "images/output/decrypt")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.henon_logistic_encrypt:
        output_image_path, number_of_pixel = henon_logistic_encrypt("images/input/input.png", "images/input/input2.png",
                                                                    "images/output")
        print(f"Сохранено в {output_image_path}. Обязательно запомните число {number_of_pixel}")
    elif choice == TypeOfFunction.henon_logistic_decrypt:
        print("Введите путь к изображению")
        image_path = input()
        print("Введите число, полученное при шифровании")
        number = int(input())
        output_image_path = henon_logistic_decrypt(image_path, number, "images/output/decrypt")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.pycasso_logistic_encrypt:
        output_image_path, number_of_pixel = pycasso_logistic_encrypt("images/input/input.png",
                                                                      "images/input/input2.png",
                                                                      "images/output")
        print(f"Сохранено в {output_image_path}. Обязательно запомните число {number_of_pixel}")
    elif choice == TypeOfFunction.pycasso_logistic_decrypt:
        print("Введите путь к изображению")
        image_path = input()
        print("Введите число, полученное при шифровании")
        number = int(input())
        output_image_path = pycasso_logistic_decrypt(image_path, number, "images/output/decrypt")
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.arnold_tiles_arnold_encrypt:
        print("Введите размер блоков")
        tile_size = int(input())
        print("Введите количество итераций (по умолчанию 26)")
        max_iteration = int(input())
        output_image_path = tiles_scramble.tiles_arnold_arnold_encrypt("images/input/input_square.png", "images/output/",
                                                                       tile_size, max_iteration)
        print(f"Сохранено в {output_image_path}")
    elif choice == TypeOfFunction.arnold_tiles_arnold_decrypt:
        print("Введите путь к изображению")
        image_path = input()
        print("Введите размер блоков")
        tile_size = int(input())
        print("Введите количество итераций (по умолчанию 26)")
        max_iteration = int(input())
        output_image_path = tiles_scramble.tiles_arnold_arnold_decrypt(image_path, "images/output/decrypt",
                                                                       tile_size, max_iteration)
        print(f"Сохранено в {output_image_path}")

    # 524288


if __name__ == "__main__":
    main()
