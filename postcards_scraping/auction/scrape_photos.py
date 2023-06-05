from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import os
import requests
import traceback


def scrape_photos(seller, exceptions_filename, df=None):
    if df is None:
        df = pd.read_csv(f'db_by_seller/auction_database_{seller}.csv', index_col=0)

    dir_name = f'photos/photos_{seller}/'
    os.makedirs(dir_name, exist_ok=True)

    for ind, row in tqdm(df.iterrows(), total=df.shape[0]):
        if row['signed'] == 'Чистая':
            continue

        try:
            page_url = row['url']
            page = requests.get(page_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            soup = soup.find('div', class_='fotorama').findAll('a')

            for num, a in enumerate(soup):
                href = a['href']

                filename = dir_name + row['ID'] + '-' + str(num) + '.jpg'
                photo_content = requests.get(href).content
                with open(filename, 'wb') as photo_file:
                    photo_file.write(photo_content)

        except:
            with open(exceptions_filename, 'a') as exceptions_file:
                exceptions_file.write('url: ' + page_url + '\n')
                exceptions_file.write(traceback.format_exc() + '\n\n\n')

    return dir_name