import glob
from PIL import Image, ImageFont, ImageDraw, ImageOps
from multiprocessing import Pool, cpu_count


def read_image(path):
    try:
        opened_image = Image.open(path)
        return opened_image
    except Exception as e:
        print("[ERROR] error opening " + path)


def exec(img_path, num):
    white_back_x = 600
    white_back_y = 600
    paste_x = paste_y = 0

    img = read_image(img_path).convert("RGBA")
    back = Image.new(mode='RGB', size=(white_back_x, white_back_y), color=img.getpixel((0, 0)))

    size = white_back_x, white_back_y
    img.thumbnail(size, Image.ANTIALIAS)
    img_x, img_y = img.size

    if img_x < white_back_x and img_y < white_back_y:
        scaler = white_back_y / float(img.size[1])
        img_x, img_y = new_size = tuple([int(x * scaler) for x in img.size])
        img = img.resize(new_size)

    if img_x > img_y:
        paste_y = int((white_back_y - img_y) / 2)
    elif img_x < img_y:
        paste_x = int((white_back_x - img_x) / 2)

    back.paste(im=img, box=(paste_x, paste_y), mask=img)

    back.save("output" + img_path[5:])


imgs = glob.glob("input/*.jpg")

pool = Pool(processes=(cpu_count()))
for i in imgs:
    pool.apply_async(exec, args=(i, 1))
pool.close()
pool.join()

## Sequential
# for i in imgs:
#    exec(i, 1)
