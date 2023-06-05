# -*- coding: utf-8 -*-

import requests
import os
import cv2
import imutils
import uuid
import pandas as pd

resize_max_value = 880
resize_min_value = 600
max_file_size = 1e6


def pic_download(url, filename):
    pic_content = requests.get(url).content
    with open(filename, 'wb') as pic_file:
        pic_file.write(pic_content)


def do_resize(img):
    # print('orig shape:', img.shape[:2])
    size_ratio = min(img.shape[0], img.shape[1]) / max(img.shape[0], img.shape[1])

    if 0.5 < size_ratio < 0.8:  # открытки стандартных размеров
        if img.shape[0] > img.shape[1]:
            img = imutils.resize(img, height=resize_max_value)
        else:
            img = imutils.resize(img, width=resize_max_value)
    else:  # нестандартные открытки
        if img.shape[0] > img.shape[1]:
            img = imutils.resize(img, width=resize_min_value)
        else:
            img = imutils.resize(img, height=resize_min_value)

    # print('resized shape:', img.shape[:2])
    return img


def pic_resize(fullsize_filename, resize_filename):
    try:
        img = cv2.imread(fullsize_filename)
        img = do_resize(img)
        cv2.imwrite(resize_filename, img)
        return True
    except:
        return False


def check_file_size(filename):
    file_size = os.path.getsize(filename)
    return file_size <= max_file_size


def pic_upload(client, bucket_name, local_filename, s3_url):
    # make a random UUID
    # image_uuid = str(uuid.uuid4())
    # '16fd2706-8baf-433b-82eb-8c7fada847da'

    # если еще не сжимали, генерируем ссылку
    if pd.isna(s3_url):
        s3_filename = str(uuid.uuid4())
        s3_url = f'https://storage.yandexcloud.net/{bucket_name}/{s3_filename}'
    else:  # иначе загружаем по старой ссылке
        s3_filename = s3_url.split('/')[-1]

    client.upload_file(local_filename, bucket_name, s3_filename)
    return s3_url
