import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

base_url = 'http://ay.by/whoiswho.phtml?id=6479956&topic=1102096&page='
url_list = []
title_list = []
signed = []

for page in tqdm(range(1, 27)):
    page_url = base_url + str(page)
    page = requests.get(page_url)

    soup = BeautifulSoup(page.content, 'html.parser')
    soup = soup.find('table', class_='lots-table m-lots-table-1').findAll('tr')

    for tr in soup:
        tr = tr.find('td', class_='txt')
        if tr is None:
            continue

        product_url = tr.find('a')['href']
        title = tr.find('a').get_text()
        url_list.append(product_url)
        title_list.append(title)

        if 'Подпис' in title:
            signed.append('Подписана')
        elif 'Чист' in title or 'Чыст' in title:
            signed.append('Чистая')
        else:
            signed.append('Не указано')

df = pd.DataFrame()
df['url'] = pd.Series(url_list)
df['ID'] = 'Ay-by-' + pd.Series(df.index).astype(str)
df = df[['ID', 'url']]
df['title'] = pd.Series(title_list)
df['signed'] = pd.Series(signed)
df.to_csv('ay-by-database.csv')
