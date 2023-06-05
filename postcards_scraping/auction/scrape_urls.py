from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from selenium import webdriver


def check_signed(s):
    s = s.lower()
    if 'подпис' in s:
        return 'Подписана'
    elif 'чист' in s or 'чыст' in s:
        return 'Чистая'
    elif 'прошла почту' in s:
        return 'Прошла почту'
    else:
        return 'Не указано'


def scrape_urls(seller_id, seller_username, num_pages):
    browser = webdriver.Chrome()
    base_url = f'https://auction.ru/listing/offer/otkrytki-48537?flt_prp_owner={seller_id}&ipp=180&pg='
    urls_source_dir = 'urls_source_html/'

    for i in range(num_pages):
        url = base_url + str(i)
        browser.get(url)
        html = browser.page_source

        filename = urls_source_dir + str(i) + '.txt'
        with open(filename, 'w', encoding='utf-8') as fout:
            fout.write(html)

    domain = 'https://auction.ru'
    url_list = []
    titles = []

    for i in tqdm(range(num_pages)):
        filename = urls_source_dir + str(i) + '.txt'
        with open(filename, 'r', encoding='utf-8') as page_source:
            html = page_source.read()

        soup = BeautifulSoup(html, "html.parser")
        soup = soup.findAll('a', class_='offers__item__title')
        for a in soup:
            href = domain + a['href']
            title = a['title']
            url_list.append(href)
            titles.append(title)

    df = pd.DataFrame()
    df['url'] = pd.Series(url_list)
    df['ID'] = f'auction-{seller_username}-' + pd.Series(df.index).astype(str)
    df = df[['ID', 'url']]
    df['title'] = pd.Series(titles)
    df['signed'] = df['title'].apply(check_signed)
    df.to_csv(f'db/auction_db_{seller_username}.csv')

    return df
