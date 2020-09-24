import glob
import os
import sys

from PIL import Image
from multiprocessing import Pool, cpu_count


def err_exit(*args, **kwargs):
    print("[ERROR] ", end="", file=sys.stderr)
    print(*args, file=sys.stderr, **kwargs)
    input("Press Enter to exit...")
    exit(1)


def check_folders():
    if not os.path.exists("input"):
        err_exit("input folder is missing")

    if not os.path.exists("output"):
        os.mkdir("output")

    for f in glob.glob("output/*"):
        os.remove(f)


def get_images():
    types = ("input/*.jpg", "input/*.jpeg", "input/*.png", "input/*.webp", "input/*.jfif")
    img_arr = []
    for files in types:
        img_arr.extend(glob.glob(files))
    return img_arr


def read_image(path):
    try:
        opened_image = Image.open(path)
        return opened_image
    except Exception:
        err_exit("[ERROR] error opening " + path)


def crop(img_path, num):
    white_back_x = 600
    white_back_y = 600
    paste_x = paste_y = 0

    img = read_image(img_path).convert("RGBA")
    back = Image.new(mode='RGB', size=(white_back_x, white_back_y), color=img.getpixel((0, 0)))

    size = white_back_x, white_back_y
    img.thumbnail(size, Image.ANTIALIAS)
    img_x, img_y = img.size

    if img_x > img_y:
        if img_x < white_back_x:
            scaler = white_back_x / float(img.size[0])
            img_x, img_y = new_size = tuple([int(x * scaler) for x in img.size])
            img = img.resize(new_size)
        paste_y = int((white_back_y - img_y) / 2)
    elif img_x < img_y:
        if img_y < white_back_y:
            scaler = white_back_y / float(img.size[1])
            img_x, img_y = new_size = tuple([int(x * scaler) for x in img.size])
            img = img.resize(new_size)
        paste_x = int((white_back_x - img_x) / 2)

    back.paste(im=img, box=(paste_x, paste_y), mask=img)

    back.save("output" + img_path[5:])

if __name__ == '__main__':
    check_folders()
    images = get_images()

    pool = Pool(processes=(cpu_count()))
    for i in images:
        pool.apply_async(crop, args=(i, 1))

    pool.close()
    pool.join()

    # Sequential
    #for i in images:
    #   crop(i, 1)

