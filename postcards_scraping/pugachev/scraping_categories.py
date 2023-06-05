import requests
from bs4 import BeautifulSoup
from pprint import pprint

page_url = 'http://pugachev-studio.ru/index.php?categoryID=8'

page = requests.get(page_url)
soup = BeautifulSoup(page.content, 'html.parser')

soup = soup.findAll(class_='clearfix')[1].findAll('div')[1].findAll('a')
# pprint(soup)
# print(len(soup))

with open('category_metadata.txt', 'w+') as fout:
    for a_tag in soup:
        href = a_tag['href']
        title = a_tag.get_text()
        fout.write(title + '\t' + href + '\n')
