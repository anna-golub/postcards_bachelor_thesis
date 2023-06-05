# -*- coding: utf-8 -*-

import pandas as pd
from pic_processing import *
from tqdm import tqdm
import argparse

from yandex_service import get_yandex_service

FILE_SIZE_EXCEEDED = 'Превышен допустимый размер файла'
FULLSIZE_UNAVAILABLE = 'Исходник недоступен'

# python resize_main.py df_base_1_to_4.csv s3_cred_write.txt
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('df_file_path', help='df_file_path')
    parser.add_argument('s3_cred_filename', help='s3_cred_filename')
    args = parser.parse_args()
    print(f'args: {args}')

    client = get_yandex_service(args.s3_cred_filename)
    bucket_name = 'postcards-resize-880pix'
    df = pd.read_csv(args.df_file_path, index_col=0)
    df = df.head()
    # print(df)

    fullsize_filename = 'fullsize.jpg'
    resize_filename = 'resize.jpg'

    print('Resizing started...')

    for ind, row in tqdm(df.iterrows(), total=df.shape[0]):
        for num in [1, 2]:  # front and back
            fullsize_url = row[f'Pic_url_{num}']
            resize_url = row[f'Resize_url_{num}']

            # download fullsize
            pic_download(fullsize_url, fullsize_filename)

            # resize
            readable = pic_resize(fullsize_filename, resize_filename)
            if readable:  # if resized successfully
                if check_file_size(resize_filename):  # check file size
                    resize_url = pic_upload(client, bucket_name, resize_filename, resize_url)
                    df.at[ind, f'Resize_url_{num}'] = resize_url
                else:
                    df.at[ind, f'Resize_url_{num}'] = FILE_SIZE_EXCEEDED
            else:
                df.at[ind, f'Resize_url_{num}'] = FULLSIZE_UNAVAILABLE

    print('Resizing done!')

    df_resize_file_path = 'df_resize_urls.csv'
    df.to_csv(df_resize_file_path, index=False)
    print(f'Saved to {df_resize_file_path}')

    print(f"{FILE_SIZE_EXCEEDED}: \n"
          f"Front - "
          f"{df[df['Resize_url_1'] == FILE_SIZE_EXCEEDED].shape[0]}\n"
          f"Back - "
          f"{df[df['Resize_url_2'] == FILE_SIZE_EXCEEDED].shape[0]}\n"
          f"{FULLSIZE_UNAVAILABLE}:\n"
          "Front - "
          f"{df[df['Resize_url_1'] == FULLSIZE_UNAVAILABLE].shape[0]}\n"
          f"Back - "
          f"{df[df['Resize_url_2'] == FULLSIZE_UNAVAILABLE].shape[0]}\n")
