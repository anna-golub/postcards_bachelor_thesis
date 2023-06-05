import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

seller = 'fabienne06140'
seller_id = 1707662
base_url = f'https://www.delcampe.net/en_GB/collectables/search?seller_ids%5B0%5D={seller_id}&categories%5B0%5D=30002&size=480&page='
num_pages = 26
domain = 'https://delcampe.net'
url_list = []

for i in tqdm(range(1, num_pages + 1)):
    page_url = base_url + str(i)

    html = requests.get(page_url).content
    soup = BeautifulSoup(html, "html.parser")
    soup = soup.findAll('div', class_='item-info')
    for div in soup:
        href = domain + div.find('a')['href']
        url_list.append(href)

df = pd.DataFrame()
df['url'] = pd.Series(url_list)
df['ID'] = f'delcampe-{seller}-' + pd.Series(df.index).astype(str)
df = df[['ID', 'url']]
df.to_csv(f'db/delcampe_{seller}.csv')
