import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

df_all = pd.read_csv('ay-by-database-new.csv', index_col=0)
# df_all = df_all.head(10000)
# all_urls = df_all['url'].to_list()

# oldman = pd.read_csv('oldman/ay-by-database-2.csv', index_col=0)
# oldman_urls = oldman['url'].to_list()
#
# chr = pd.read_csv('чертова дюжина/ay-by-database-otkr.csv', index_col=0)
# chr_urls = chr['url'].to_list()
#
# # print('oldman')
# # for ind, url in enumerate(oldman_urls):
# #     if url in all_urls:
# #         print(url)
# #
# # print('chr')
# # for ind, url in enumerate(chr_urls):
# #     if url in all_urls:
# #         print(url)
#
# duplicates = []
# for ind, row in df_all.iterrows():
#     if row['url'] in oldman_urls or row['url'] in chr_urls:
#         duplicates.append(ind)
#
# print(len(duplicates))
# print(df_all.shape)
# df_all = df_all.drop(duplicates)
# print(df_all.shape)
# df_all.to_csv('ay-by-database-new.csv')
# print(duplicates[:10])

duplicates = []
for ind, row in tqdm(df_all.iterrows(), total=df_all.shape[0]):
    if ind < 1050:
        continue
    url = row['url']
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup = soup.find('span', class_='b-seller-info-summary__user-name')
        seller = soup.get_text().lstrip().rstrip()

        if seller.lower() in ('чертова дюжина', 'oldman'):
            duplicates.append(url)
    except:
        continue

    # break

pd.Series(duplicates).to_csv('possible_duplicates.csv')
