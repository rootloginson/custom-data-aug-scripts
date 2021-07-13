import os
import random
from PIL import Image
import magician_PIL as m
import json
import datetime


# There are augmentation methods to apply each folder.
# These methods and its parameters defined in task dictionary.
# main() function applies these tasks to given image folder.
# The converted images are saved separately into the folder containing the original images.
# logging has not been updated yet.

# { folder1:{'dir_path': dir_name.path, 'image_names': []}, folder2:{'dir_path': dir_name.path, 'image_names': []}, ... }
def scan_train_folder():
    dict_1 = {}
    for directory_name in os.scandir('.'):
        dir_name = directory_name.name
        dict_1[dir_name] = {'dir_path': directory_name.path, 'image_names': []}
        for image_name in os.scandir(directory_name.path):
            dict_1[dir_name]['image_names'].append(image_name.name)
    return dict_1


def random_image_pick(d, percentage):
    """
    percentage is between 0-100
    return path of the folder and image list
    """
    image_name_list = d['image_names']
    folder_path = d['dir_path']
    selection_list = []
    no_of_images = len(image_name_list)
    no_of_selections = int((no_of_images * percentage) / 100)
    selection_list = random.sample(image_name_list, no_of_selections)
    return folder_path, selection_list


def equalize_files(d):
    # the function equalizes the number of items in the subfolders by picking the items randomly and removing
    avg_folder_length = sum([len(v['image_names']) for v in d.values()]) // len(d)
    for k, v in d.items():
        img_names = v['image_names']
        img_path = v['dir_path']
        del_number = len(img_names) - avg_folder_length
        if del_number <= 0:
            continue
        images_that_will_be_deleted = random.sample(list(img_names), del_number)
        for i in images_that_will_be_deleted:
            os.remove(img_path + '/' + i)
    print("Equalized.")


def main(tasks_dict):
    d_all = scan_train_folder()
    equalize_files(d_all)
    d_all = scan_train_folder()
    print("Folder length:", [len(v['image_names']) for v in d_all.values()])

    folder_names = list(d_all.keys())
    # if there is a json file, exit. os.scandir gives not a directory error due to json file. better for now.
    # for _, i2 in zip([f_name.split(".") for f_name in folder_names]):
    #     if i2 == 'json':
    #         sys.exit()

    # { folder_name1 = (folder_path, [images]), folder_name2 = (folder_path, [images]) }
    task_definition = ""
    settings = {}
    rand_images_dict_folders = {}
    processed_images_dict = {}
    # keys are name of the folders
    for current_folder_name in folder_names:
        # user_input_exit = input("Do you want to continue: 'y' or 'n'")
        # if user_input_exit == 'n':
        #     break
        print(f"Current folder: {current_folder_name}.")
        # task_list = {'i': [task1, task2...], 'ii': [task1, task2..], ...}
        for task_i in tasks_dict[current_folder_name]:
            try:
                task_definition, percentage, (task, args) = task_i
            except KeyError:
                continue
            folder_path, image_names = random_image_pick(d_all[current_folder_name], percentage=percentage)
            processed_images_dict[current_folder_name] = []
            print(f"slicing image process folder -> {folder_path}")
            for image_name in image_names:
                img = Image.open(folder_path + "/" + image_name)
                args[0] = img
                processed_image = task(*args)
                saved_img_path = m.save_image(processed_image, task_definition, image_name, folder_path)
                processed_images_dict[current_folder_name].append(
                            (task_definition, saved_img_path)
                            )
        settings[current_folder_name] = task_definition
        rand_images_dict_folders[current_folder_name] = image_names
    d_all = scan_train_folder()
    equalize_files(d_all)
    print("Folder length:", [len(v['image_names']) for v in d_all.values()])
    utc_datetime = datetime.datetime.utcnow()
    utc_datetime = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
    settings['date'] = utc_datetime

    log_them_all = {
            'folder_scan': d_all,
            'folder_process_settings': settings,
            'randomly_picked_images': rand_images_dict_folders,
            'processed_images_dict': processed_images_dict
            }
    with open(f"../{utc_datetime}.json", 'w') as f:
        json.dump(log_them_all, f)


rxc = m.rotate_x_degree_crop_inner_square
rsc = m.random_square_crop
# that looks like a flag :)
tasks_dict1 =[
            {
              'i': ['rotate_left_right', 40, [rxc, [None, random.choice([-15, 15])]]],
              'ii': ['rotate_left_right', 40, [rxc, [None, random.choice([-15, 15])]]],
              'iii': ['rotate_left_right', 40, [rxc, [None, random.choice([-15, 15])]]],
              'iv': ['rotate_left_right', 40, [rxc, [None, random.choice([-15, 15])]]],
              'v': ['rotate_left_right', 40, [rxc, [None, random.choice([-15, 15])]]],
              'vi': ['rotate_left_right', 40, [rxc, [None, random.choice([-15, 15])]]],
              'vii': ['rotate_left_right', 40, [rxc, [None, random.choice([-15, 15])]]],
              'viii': ['rotate_left_right', 40, [rxc, [None, random.choice([-15, 15])]]],
              'ix': ['rotate_left_right', 40, [rxc, [None, random.choice([-15, 15])]]],
              'x': ['rotate_left_right', 40, [rxc, [None, random.choice([-15, 15])]]],
            },

            {
              'i': ['random_square_crop', 50, [rsc, [None, 85]]],
              'ii': ['random_square_crop', 50, [rsc, [None, 85]]],
              'iii': ['random_square_crop', 50, [rsc, [None, 85]]],
              'iv': ['random_square_crop', 50, [rsc, [None, 85]]],
              'v': ['random_square_crop', 50, [rsc, [None, 85]]],
              'vi': ['random_square_crop', 50, [rsc, [None, 85]]],
              'vii': ['random_square_crop', 50, [rsc, [None, 85]]],
              'viii': ['random_square_crop', 50, [rsc, [None, 85]]],
              'ix': ['random_square_crop', 50, [rsc, [None, 85]]],
              'x': ['random_square_crop', 50, [rsc, [None, 85]]]
            },
            ]

tasks_dict = {}
for j in tasks_dict1:
    for k,v in j.items():
        try:
            tasks_dict[k].append(v)
        except KeyError:
            tasks_dict[k] = []
            tasks_dict[k].append(v)
#print(tasks_dict)
main(tasks_dict)
