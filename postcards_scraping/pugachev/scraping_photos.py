import requests
from bs4 import BeautifulSoup
from pprint import pprint
import traceback
import os

counter = 0

for file in os.listdir('product_ids_by_category'):
    filename = os.fsdecode(file)

    print(filename)
    category_id = filename.split('.txt')[0]
    filename = 'product_ids_by_category/' + filename
    dir_name = 'photos/' + category_id
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    with open(filename, 'r') as fin:
        for s in fin:
            product_id = s.strip()

            page_url = 'http://pugachev-studio.ru/index.php?productID=' + product_id
            # print(page_url)
            page = requests.get(page_url)

            # if page.status_code != 200:
            #     continue
            counter += 1

            try:
                soup = BeautifulSoup(page.content, 'html.parser')
                temp = soup.find(class_='cpt_product_images').find_all('a')

                front_url = temp[1]['href']
                back_url = temp[2]['href']

                front_content = requests.get('http://pugachev-studio.ru' + front_url).content
                back_content = requests.get('http://pugachev-studio.ru' + back_url).content

                front_filename = dir_name + '/pugachev-' + str(product_id) + '-1.jpg'
                back_filename = dir_name + '/pugachev-' + str(product_id) + '-2.jpg'

                with open(front_filename, 'wb') as front_file:
                    front_file.write(front_content)

                with open(back_filename, 'wb') as back_file:
                    back_file.write(back_content)

            except:
                with open('exceptions.txt', 'a') as exceptions_file:
                    exceptions_file.write('url: ' + page_url + '\n')
                    exceptions_file.write(traceback.format_exc() + '\n\n\n')

print(counter)
