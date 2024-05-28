import os
import sys
import time
from PIL import Image, ImageSequence
import shutil
import threading

# Функция для очистки экрана
def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Функция для изменения размера изображения
def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / float(width)
    terminal_size = shutil.get_terminal_size()
    terminal_width = terminal_size.columns
    terminal_height = terminal_size.lines

    new_width = min(new_width, terminal_width)
    new_height = int(aspect_ratio * new_width)

    # Ограничиваем высоту изображения, чтобы оно полностью помещалось в окно терминала
    new_height = min(new_height, terminal_height - 1)  # оставляем место для командной строки

    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    return resized_image


# Функция для преобразования изображения в оттенки серого
def grayify(image):
    grayscale_image = image.convert("L")
    return grayscale_image

# Функция для преобразования пикселей в ASCII символы
def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_chars = "@#S+*:., "
    ascii_string = "".join([ascii_chars[min(pixel//len(ascii_chars), len(ascii_chars) - 1)] for pixel in pixels])
    return ascii_string


# Основная функция для обработки анимации
def main(file_path):
    try:
        image = Image.open(file_path)
    except Exception as e:
        print(e)
        return

    frames = [frame.copy() for frame in ImageSequence.Iterator(image)]

    ascii_frames = []
    for frame in frames:
        terminal_size = shutil.get_terminal_size()
        new_width = terminal_size.columns
        
        # Преобразовать изображение
        frame = resize_image(frame, new_width)
        frame = grayify(frame)
        ascii_str = pixels_to_ascii(frame)

        # Разделить строку на список строк
        ascii_img = "\n".join([ascii_str[i:i+new_width] for i in range(0, len(ascii_str), new_width)])
        ascii_frames.append(ascii_img)

    # Воспроизведение анимации
    while True:
        for frame in ascii_frames:
            clear_screen()
            print(frame)
            time.sleep(0.1)  # Управление скоростью воспроизведения


# Запуск анимации в отдельном потоке
if __name__ == '__main__':
    anim_thread = threading.Thread(target=main, args=('123.gif',))
    anim_thread.start()
