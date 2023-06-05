import requests
from bs4 import BeautifulSoup

domain = 'http://pugachev-studio.ru'

with open('category_metadata.txt', 'r') as fin:
    for s in fin:
        print(s)

        category_title, category_url = s.strip().split('\t')
        category_id = category_url.split('=')[1]
        base_url = domain + category_url + '&offset='

        offset = 0
        product_ids = []

        while True:
            page_url = base_url + str(offset)
            page = requests.get(page_url)

            soup = BeautifulSoup(page.content, 'html.parser')
            soup = soup.findAll(class_='product_brief_block')
            if not soup:
                break

            for item in soup:
                product_id = item.findAll('input')[1]['value']
                # print(product_id)
                product_ids.append(int(product_id))

            offset += 100

        product_ids_filename = 'product_ids_by_category/' + category_id + '.txt'
        product_ids = sorted(product_ids)
        with open(product_ids_filename, 'w') as fout:
            for product_id in product_ids:
                fout.write(str(product_id) + '\n')
