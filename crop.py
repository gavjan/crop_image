import glob
import os
import sys
from PIL import Image
import platform

MAC_BINARY = platform.system() == "Darwin" and getattr(sys, 'frozen', False)
if not MAC_BINARY:
    import pillow_avif


def err_exit(*args, **kwargs):
    print("[ERROR] ", end="", file=sys.stderr)
    print(*args, file=sys.stderr, **kwargs)
    print("\nPress Enter to exit...", file=sys.stderr)
    input()
    exit(1)


def check_folders():
    if not os.path.exists("input"):
        err_exit("input folder is missing")

    if not os.path.exists("output"):
        os.mkdir("output")

    for f in glob.glob("output/*"):
        os.remove(f)


def get_images():
    return glob.glob("input/*")


def read_image(path):
    try:
        opened_image = Image.open(path)
        return opened_image
    except Exception:
        err_exit("error opening " + path)


def crop(img_path):
    white_back_x = 600
    white_back_y = 600
    paste_x = paste_y = 0

    img = read_image(img_path).convert("RGBA")
    back = Image.new(mode='RGB', size=(white_back_x, white_back_y), color=img.getpixel((0, 0)))

    size = white_back_x, white_back_y
    img.thumbnail(size, Image.LANCZOS)
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

    file_name = os.path.splitext(img_path)[-2].lower()
    back.save("output" + file_name[len("input"):] + ".jpg")


def main():
    if MAC_BINARY:
        app_path = os.path.dirname(sys.executable)
        os.chdir(app_path)
        print("CWD=" + os.getcwd())
    check_folders()
    for i in get_images():
        crop(i)


if __name__ == '__main__':
    main()
