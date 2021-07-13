import numpy as np
import cv2


def view_img(img: np.array):
    cv2.imshow('lorem ipsum', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# slices images horizontally into given pieces
def slice_into(number_of_pieces: int, img: np.array):
    h, w, c = img.shape
    piece_height = h // number_of_pieces
    pieces = []
    prev_point = 0
    for i in range(number_of_pieces):
        if i == (number_of_pieces - 1):
            # the last piece
            pieces.append(img[prev_point:, :, :])
            break
        pieces.append(img[prev_point:(prev_point+piece_height), :, :])
        prev_point += piece_height
    return pieces


def save_slices(images: list, image_name: str, folder_path="."):
    image_name, image_extension = image_name.split(".")
    split_names_list = []
    for ix, img in enumerate(images, start=1):
        new_image_name = (
            'Sliced_'
            + image_name
            + "_part_"
            + str(ix)
            + "."
            + image_extension
            )
        img_path = folder_path + '/' + new_image_name
        cv2.imwrite(img_path, img)
        split_names_list.append(img_path)
    return split_names_list
