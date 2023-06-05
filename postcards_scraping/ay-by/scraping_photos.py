import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import traceback

df = pd.read_csv('ay-by-database-new.csv', index_col=0)
# df = df.head(5000)
df = df[df.index.isin(range(21000, 30000))]

for ind, row in tqdm(df.iterrows(), total=df.shape[0]):
    try:
        if row['signed'] == 'Чистая':
            continue

        page_url = row['url']
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup = soup.findAll('figure')

        base_filename = 'all/22309 - 31870/'
        if row['signed'] == 'Подписана':
            base_filename += 'подписанные/'
        elif row['signed'] == 'Прошла почту':
            base_filename += 'прошли почту/'
        elif row['signed'] == 'Не указано':
            base_filename += 'не указано/'
        base_filename += row['ID'] + '-'

        for fig_num, figure in enumerate(soup):
            a = figure.find('a')
            href = a['href']

            filename = base_filename + str(len(soup) - fig_num) + '.jpg'
            photo_content = requests.get(href).content
            with open(filename, 'wb') as photo_file:
                photo_file.write(photo_content)

    except:
        with open('exceptions.txt', 'a') as exceptions_file:
            exceptions_file.write('url: ' + page_url + '\n')
            exceptions_file.write(traceback.format_exc() + '\n\n\n')
