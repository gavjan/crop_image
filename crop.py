import glob
from PIL import Image, ImageFont, ImageDraw, ImageOps


def read_image(path):
    try:
        opened_image = Image.open(path)
        return opened_image
    except Exception as e:
        print("[ERROR] error opening " + path)


def exec(img_path):
    white_back_x = 600
    white_back_y = 600
    paste_x = paste_y = 0

    img = read_image(img_path).convert("RGBA")
    back = Image.new('RGB', (white_back_x, white_back_y), 'white')

    size = white_back_x, white_back_y
    img.thumbnail(size, Image.ANTIALIAS)
    img_x, img_y = img.size

    if img_x > img_y:
        paste_y = int((white_back_y - img_y) / 2)
    else:
        paste_x = int((white_back_x - img_x) / 2)

    back.paste(im=img, box=(paste_x, paste_y), mask=img)

    back.save("output" + img_path[5:])


imgs = glob.glob("input/*.png")

for i in imgs:
    exec(i)
