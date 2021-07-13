from PIL import Image
import hashlib
import os

# { folder1:{img1_hash:'img_name', img2_hash:'img_name'}, folder2:{img1_hash:'img_name', img2_hash:'img_name'}, ... }
dict_1 = {}

for directory_name in os.scandir('.'):
    """Searches for duplicates by comparing names in folders."""
    dir_name = directory_name.name
    dict_1[dir_name] = {}
    # dummy key
    dict_1[dir_name][None] = []
    for image_name in os.scandir(directory_name.path):
        path = image_name.path
        im = Image.open(path)
        image_hash = hashlib.sha256(im.tobytes()).hexdigest()
        try:
            _ = dict_1[dir_name][image_hash]
        except KeyError:
            dict_1[dir_name][image_hash] = []
        finally:
            dict_1[dir_name][image_hash].append(image_name.name)
    # in each directory, total number of duplicates and total number of files
    x = 0
    for v in dict_1[dir_name].values():
        if len(v) > 1:
            x += len(v) - 1
    print(f"{dir_name} -> number of duplicates:{x}, total file:{len(dict_1[dir_name])}")

