from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import traceback

from selenium import webdriver

browser = webdriver.Chrome()
base_url = 'http://collect.ay.by/otkrytki-konverty-kalendari/otkrytki/do-1990/'

for page in range(1, 2918):
    page_url = base_url
    if page > 1:
        page_url += '?page=' + str(page)
    browser.get(page_url)
    html = browser.page_source

    filename = 'all/page_source/' + str(page) + '.txt'
    with open(filename, 'w', encoding='utf-8') as fout:
        fout.write(html)

url_list = []
title_list = []
signed = []

for i in tqdm(range(1, 730)):
    try:
        filename = 'all/page_source/' + str(i) + '.txt'
        with open(filename, 'r', encoding='utf-8') as page_source:
            html = page_source.read()

        soup = BeautifulSoup(html, "html.parser")
        soup = soup.findAll('a', class_='item-type-card__link')
        for a in soup:
            href = a['href']
            url_list.append(href)

            title = a.get_text().lstrip().rstrip()
            title_list.append(title)

            if 'подпис' in title.lower():
                signed.append('Подписана')
            elif 'чист' in title.lower() or 'чыст' in title.lower():
                signed.append('Чистая')
            elif 'прошла почту' in title.lower():
                signed.append('Прошла почту')
            else:
                signed.append('Не указано')

    except:
        with open('exceptions.txt', 'a') as exceptions_file:
            exceptions_file.write('page: ' + str(i) + '\n')
            exceptions_file.write(traceback.format_exc() + '\n\n\n')

df = pd.DataFrame()
df['url'] = pd.Series(url_list)
df['title'] = pd.Series(title_list)
df['signed'] = pd.Series(signed)

df = df.drop_duplicates(subset=['url'])
df['ID'] = 'ay-by-' + pd.Series(df.index).astype(str)
df = df[['ID', 'url', 'title', 'signed']]

df.to_csv('ay-by-database.csv')
print(df.shape)
