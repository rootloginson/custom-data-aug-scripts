from PIL import Image
from PIL import ImageOps
import random
import math

# Custom data augmentation methods to apply to image folders

def rotate_x_degree(img, x: int):
    return img.rotate(x, fillcolor='black')

def rotate_x_degree_crop_inner_square(img, x: int):
    if not((-90 <= x) and (x <= 90)):
        print("angle should be between 0 and 90 degree")
        return None
    flag = 0
    if x < 0:
        flag = 1
        img = ImageOps.mirror(img)
        x = abs(x)
    img = center_square_crop(img, 99)
    L = img.size[0]
    img = img.rotate(x, fillcolor='black')
    inner_square_L = L / (math.sin(math.pi/180*x) + math.cos(math.pi/180*x))
    new_percentage = (inner_square_L/L) * 100
    img = center_square_crop(img, new_percentage)
    if not flag:
        return img
    if flag:
        return ImageOps.mirror(img)
    return


def center_square_crop(img, percentage: int):
    if percentage < 10:
        print("percentage can't be lower than 10")
        print("process finished.")
        return None
    w, h = img.size
    square_max = w if (w<=h) else h
    center_w, center_h = w//2, h//2
    side_length = int(square_max * (percentage/100))
    a = side_length // 2
    c1 = 0 if center_w-a <= 0 else center_w-a
    c2 = 0 if center_h-a <= 0 else center_h-a
    c3 = w if center_w+a >= w else center_w+a
    c4 = h if center_h+a >= h else center_h+a
    return img.crop((c1, c2, c3, c4))


def mirror_img(img):
    return ImageOps.mirror(img)


def random_square_crop(img, percentage: int):
    if percentage < 10:
        print("percentage can't be lower than 10")
        print("process finished.")
        return None
    w, h = img.size
    square_max = w if (w<=h) else h
    side_length = int(square_max * (percentage/100))
    if h <= w:
        if 50 < w-h:
            starting_point_w = random.randint(0,w-h-1)
        else:
            starting_point_w = 0
        if percentage < 100:
            h_gap = int(h * ((100-percentage)/100))
            starting_point_h = random.randint(0, h_gap-1)
        else:
            starting_point_h = 0
        return img.crop((
            starting_point_w,
            starting_point_h,
            starting_point_w+side_length,
            starting_point_h+side_length
            )
        )
    else:
        if 50 < h-w:
            starting_point_h = random.randint(0,h-w-1)
        else:
            starting_point_h = 0
        if percentage < 100:
            w_gap = int(w * ((100-percentage)/100))
            starting_point_w = random.randint(0, w_gap-1)
        else:
            starting_point_w = 0
        return img.crop((
            starting_point_w,
            starting_point_h,
            starting_point_w+side_length,
            starting_point_h+side_length
            )
        )


def save_image(img, func_name: str, image_name: str, folder_path="."):
    new_image_name = (func_name + "_" + image_name)
    img_path = folder_path + '/' + new_image_name
    img.save(img_path)
    return img_path

if __name__ == '__main__':
    im = Image.open('./test_image.png')
    # cs = center_square_crop
    # rs = random_square_crop