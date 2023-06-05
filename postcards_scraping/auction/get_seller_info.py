from bs4 import BeautifulSoup
import requests
import re


def get_seller_info(input_url):
    if input_url.startswith('https://auction.ru/user/'):
        seller_id = re.search('-i(.+?)\.html', input_url).group(1)
    elif 'flt_prp_owner' in input_url:
        seller_id = re.search('flt_prp_owner=[0-9]+', input_url).group()
        seller_id = seller_id.split('=')[1]
    else:
        raise Exception(f'Failed to get seller id from url: {input_url}')

    proper_url = f'https://auction.ru/listing/offer/otkrytki-48537?flt_prp_owner={seller_id}&ipp=180'
    html = requests.get(proper_url).content
    soup = BeautifulSoup(html, "html.parser")

    seller_username = soup.find('div', class_='row content').find('p').find('span').find('a')['href']
    seller_username = seller_username.split('-')[0][6:]

    try:
        num_pages = soup.find('div', class_='row content') \
            .find('div', class_='col-sm-9 offers_container') \
            .find('div', class_='listing') \
            .findAll('li', class_='listing__pager__page')[2].find('a').find('span').get_text()
        num_pages = int(num_pages)
    except:
        num_pages = 1

    return seller_id, seller_username, num_pages
