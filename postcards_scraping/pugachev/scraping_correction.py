import os
from PIL import Image
import requests

counter = 0

# checking for invalid images
for subdir, dirs, files in os.walk('photos'):
    for dir in dirs:
        print(dir)
        dir_name = 'photos/' + dir

        for photo in os.listdir(dir_name):
            photo_name = dir_name + '/' + photo

            try:
                img = Image.open(photo_name)
                img.verify()  # valid image
            except:
                os.remove(photo_name)  # invalid image
                counter += 1

print(counter)

# checking for postcards with more than 2 scans


