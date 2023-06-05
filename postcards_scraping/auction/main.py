from get_seller_info import get_seller_info
from scrape_from_exceptions import scrape_from_exceptions
from scrape_photos import scrape_photos
from scrape_urls import scrape_urls
from zip import redistribute_photos, zip_folders
import os
import pandas as pd


def prep_folders():
    os.makedirs('urls_source_html', exist_ok=True)
    os.makedirs('db', exist_ok=True)
    os.makedirs('photos', exist_ok=True)
    os.makedirs('zip', exist_ok=True)
    os.makedirs('exceptions', exist_ok=True)


def auction_scrape(input_url):
    print('Getting seller info...')
    seller_id, seller_username, num_pages = get_seller_info(input_url)
    # seller_id, seller_username, num_pages = '35866717', 'cat2006062', 30
    print(f'ID: {seller_id}, username: {seller_username}, pages: {num_pages}')

    print('\nScraping urls...')
    df = scrape_urls(seller_id, seller_username, num_pages)
    # df = pd.read_csv('db/auction_db_cat2006062.csv', index_col=0)

    exceptions_filename = f'exceptions/exceptions_{seller_username}.txt'
    print('\nScraping photos...')
    dir_main_path = scrape_photos(seller_username, exceptions_filename, df)
    # dir_main_path = 'photos/photos_cat2006062/'

    exceptions_new_filename = f'exceptions/exceptions_new_{seller_username}.txt'
    print('\nScraping from exceptions...')
    scrape_from_exceptions(seller_username, exceptions_filename, exceptions_new_filename, df)

    print('\nCreating archives...')
    dir_paths = redistribute_photos(dir_main_path)
    zip_folders(dir_paths)


if __name__ == "__main__":
    prep_folders()

    # put seller urls here
    input_url_list = [
        ''
    ]

    for input_url in input_url_list:
    # try:
        auction_scrape(input_url)
        print('Done!\n\n\n')
    # except:
    #     print('Fail:', input_url)
    # raise
