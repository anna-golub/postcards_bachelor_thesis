from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
import traceback
from tqdm import tqdm


def scrape_from_exceptions(seller_username, exceptions_filename, exceptions_new_filename, df=None):
    if not os.path.isfile(exceptions_filename):
        print('--- no exceptions occurred')
        return

    if df is None:
        df = pd.read_csv(f'db_by_seller/auction_database_{seller_username}.csv', index_col=0)
    base_filename = f'photos/photos_{seller_username}/'

    with open(exceptions_filename, 'r') as exceptions_file:
        # num_lines = sum(1 for line in exceptions_file)
        # print(num_lines)
        # for s in tqdm(exceptions_file, total=num_lines):
        for s in exceptions_file:
            if not s.startswith('url:'):
                continue
            url = s[5:].strip()
            row = df[df['url'] == url].iloc[0]

            try:
                page_url = row['url']
                page = requests.get(page_url)
                soup = BeautifulSoup(page.content, 'html.parser')
                soup = soup.find('div', class_='fotorama').findAll('a')

                for num, a in enumerate(soup):
                    href = a['href']

                    filename = base_filename + row['ID'] + '-' + str(num) + '.jpg'
                    photo_content = requests.get(href).content
                    with open(filename, 'wb') as photo_file:
                        photo_file.write(photo_content)

            except:
                with open(exceptions_new_filename, 'a') as exceptions_new:
                    exceptions_new.write('url: ' + page_url + '\n')
                    exceptions_new.write(traceback.format_exc() + '\n\n\n')
