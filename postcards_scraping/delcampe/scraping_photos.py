import os

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import traceback

seller = 'fabienne06140'
df = pd.read_csv(f'db/delcampe_{seller}.csv', index_col=0)
# df = df.tail(1600)
# print(df.head())
# print(df.shape)

base_filename = f'photos_{seller}/'
os.makedirs(base_filename, exist_ok=True)

for ind, row in tqdm(df.iterrows(), total=df.shape[0]):
    try:
        page_url = row['url']
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        soup = soup.findAll('div', class_='slick-slide')
        for num, div in enumerate(soup):
            img_url = div.find('img')['src']
            img_url = img_url.replace('img_small', 'img_large')
            filename = base_filename + row['ID'] + '-' + str(num) + '.jpg'
            photo_content = requests.get(img_url).content
            with open(filename, 'wb') as photo_file:
                photo_file.write(photo_content)

    except:
        # raise
        with open('exceptions.txt', 'a') as exceptions_file:
            exceptions_file.write('url: ' + page_url + '\n')
            exceptions_file.write(traceback.format_exc() + '\n\n\n')

    # break
