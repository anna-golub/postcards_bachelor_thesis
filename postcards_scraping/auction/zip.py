import os
import shutil


def redistribute_photos(dir_main_path):
    dir_main = os.fsencode(dir_main_path)
    size_running = 0
    dir_number = 0
    dir_paths = [dir_main_path]

    for f in os.listdir(dir_main):
        filename = os.fsdecode(f)
        if dir_number != 0:
            os.rename(dir_main_path + filename, dir_new_path + filename)

        size_running += os.path.getsize(dir_main_path + filename)
        if size_running // 10e9 > 1.5:
            dir_number += 1
            dir_new_path = f'{dir_main_path}_{dir_number}'
            os.mkdir(dir_new_path)
            dir_paths.append(dir_new_path)
            size_running = 0

    return dir_paths


def zip_folders(dir_paths):
    for dir_path in dir_paths:
        shutil.make_archive(f'zip/{dir_path.split("/")[1]}', 'zip', dir_path)
