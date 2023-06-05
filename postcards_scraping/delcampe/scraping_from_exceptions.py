import requests
from bs4 import BeautifulSoup
import pandas as pd
import traceback

seller = 'cpa-collection'
df = pd.read_csv(f'db/delcampe_{seller}.csv', index_col=0)
base_filename = f'photos_{seller}/'

with open('exceptions.txt', 'r') as exceptions_file:
    for s in exceptions_file:
        if not s.startswith('url:'):
            continue
        url = s[5:].strip()
        row = df[df['url'] == url].iloc[0]
        print(row['url'])

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
            with open('exceptions_new.txt', 'a') as exceptions_new_file:
                exceptions_new_file.write('url: ' + page_url + '\n')
                exceptions_new_file.write(traceback.format_exc() + '\n\n\n')

    # break
