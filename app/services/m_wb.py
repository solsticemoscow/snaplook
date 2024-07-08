import json
import time
from datetime import date
from os import path

import pandas as pd
import requests


class WildBerriesParser:

    def __init__(self):
        """
        Initialize a new instance of the WildBerriesParser class.

        This constructor sets up the parser object with default values
        for its attributes.

        Args:
            None

        Returns:
            None
        """
        self.headers = {'Accept': "*/*",
                        'User-Agent': "Chrome/51.0.2704.103 Safari/537.36"}
        self.run_date = date.today()
        self.product_cards = []
        self.directory = path.dirname(__file__)

    def download_current_catalogue(self) -> str:
        """
        Download the  catalogue from wildberries.ru and save it in JSON format.

        If an up-to-date catalogue already exists in the script's directory,
        it uses that instead.

        Returns:
            str: The path to the downloaded catalogue file.
        """
        local_catalogue_path = path.join(self.directory, 'wb_catalogue.json')
        if (not path.exists(local_catalogue_path)
                or date.fromtimestamp(int(path.getmtime(local_catalogue_path)))
                > self.run_date):
            url = ('https://static-basket-01.wb.ru/vol0/data/'
                   'main-menu-ru-ru-v2.json')
            response = requests.get(url, headers=self.headers).json()
            with open(local_catalogue_path, 'w', encoding='UTF-8') as my_file:
                json.dump(response, my_file, indent=2, ensure_ascii=False)
        return local_catalogue_path

    def traverse_json(self, parent_category: list, flattened_catalogue: list):
        """
        Recursively traverse the JSON catalogue and flatten it to a list.

        This function runs recursively through the locally saved JSON
        catalogue and appends relevant information to the flattened_catalogue
        list.
        It handles KeyError exceptions that might occur due to inconsistencies
        in the keys of the JSON catalogue.

        Args:
            parent_category (list): A list containing the current category
              to traverse.
            flattened_catalogue (list): A list to store the flattened
              catalogue.

        Returns:
            None
        """
        for category in parent_category:
            try:
                flattened_catalogue.append({
                    'name': category['name'],
                    'url': category['url'],
                    'shard': category['shard'],
                    'query': category['query']
                })
            except KeyError:
                continue
            if 'childs' in category:
                self.traverse_json(category['childs'], flattened_catalogue)

    def process_catalogue(self, local_catalogue_path: str) -> list:
        catalogue = []
        with open(local_catalogue_path, 'r') as my_file:
            self.traverse_json(json.load(my_file), catalogue)
        return catalogue

    def extract_category_data(self, catalogue: list, user_input: str) -> tuple:

        for category in catalogue:
            if (user_input.split("https://www.wildberries.ru")[-1]
                    == category['url'] or user_input == category['name']):
                return category['name'], category['shard'], category['query']

    def get_products_on_page(self, page_data: dict) -> list:
        products_on_page = []

        for item in page_data['data']['products']:
            products_on_page.append({
                'Link': f"https://www.wildberries.ru/catalog/"
                          f"{item['id']}/detail.aspx",
                'Name': item['name'],
                'Image': self.get_pics(item['id']),
                'Price': int(item['priceU'] / 100),
                'Sale': int(item['salePriceU'] / 100),
                'Rating': item['rating'],
                'Feed': item['feedbacks']
            })
            time.sleep(.2)
            if len(products_on_page) == 8:
                break
        return products_on_page

    def get_all_products_in_category(self, category_data: tuple):
        """
        Retrieve all products in a category by going through all pages.

        This function iterates over page numbers from 1 to 100, constructing
        the URL for each page in the specified category. It then calls the
        add_data_from_page method to retrieve and add the product data from
        each page to the class's product_cards list. If the add_data_from_page
        method returns True, indicating the end of product loading,
        the loop breaks.

        Note:
            The wildberries.ru website currently limits the maximum number of
            pages that can be parsed to 100.

        Args:
            category_data (tuple): A tuple containing the category name,
              shard, and query.

        Returns:
            None
        """
        for page in range(1, 101):
            print(f"Загружаю товары со страницы {page}")
            url = (f"https://catalog.wb.ru/catalog/{category_data[1]}/"
                   f"catalog?appType=1&{category_data[2]}&curr=rub"
                   f"&dest=-1257786&page={page}&sort=popular&spp=24")
            if self.add_data_from_page(url):
                break

    def get_sales_data(self):

        for card in self.product_cards:
            url = (f"https://product-order-qnt.wildberries.ru/by-nm/"
                   f"?nm={card['Артикул']}")
            try:
                response = requests.get(url, headers=self.headers).json()
                card['Продано'] = response[0]['qnt']
            except requests.ConnectTimeout:
                card['Продано'] = 'нет данных'
            print(f"Собрано карточек: {self.product_cards.index(card) + 1}"
                  f" из {len(self.product_cards)}")

    def save_to_excel(self, file_name: str) -> str:
        """
        Save the parsed data in xlsx format and return its path.

        This function takes the parsed data stored in the product_cards list
        and converts it into a Pandas DataFrame. It then saves the DataFrame
        as an xlsx file with the specified file name and the current run date
        appended to it. The resulting file path is returned.

        Args:
            file_name (str): The desired file name for the saved xlsx file.

        Returns:
            str: The path of the saved xlsx file.
        """
        data = pd.DataFrame(self.product_cards)
        result_path = (f"{path.join(self.directory, file_name)}_"
                       f"{self.run_date.strftime('%Y-%m-%d')}.xlsx")
        writer = pd.ExcelWriter(result_path)
        data.to_excel(writer, 'data', index=False)
        writer.close()
        return result_path

    def get_all_products_in_search_result(self, key_word: str):
        url = (f"https://search.wb.ru/exactmatch/ru/common/v4/search?"
               f"appType=1&curr=rub&dest=-1257786&page=1"
               f"&query={'%20'.join(key_word.split())}&resultset=catalog"
               f"&sort=popular&spp=24&suppressSpellcheck=false")

        response = requests.get(url, headers=self.headers).json()
        page_data = self.get_products_on_page(response)
        return page_data

    def get_pics(self, ID: int):
        _short_id = ID//100000

        if 0 <= _short_id <= 143:
            basket = '01'
        elif 144 <= _short_id <= 287:
            basket = '02'
        elif 288 <= _short_id <= 431:
            basket = '03'
        elif 432 <= _short_id <= 719:
            basket = '04'
        elif 720 <= _short_id <= 1007:
            basket = '05'
        elif 1008 <= _short_id <= 1061:
            basket = '06'
        elif 1062 <= _short_id <= 1115:
            basket = '07'
        elif 1116 <= _short_id <= 1169:
            basket = '08'
        elif 1170 <= _short_id <= 1313:
            basket = '09'
        elif 1314 <= _short_id <= 1601:
            basket = '10'
        elif 1602 <= _short_id <= 1655:
            basket = '11'
        elif 1656 <= _short_id <= 1919:
            basket = '12'
        elif 1920 <= _short_id <= 2045:
            basket = '13'
        elif 2046 <= _short_id <= 2189:
            basket = '14'
        elif 2190 <= _short_id <= 2405:
            basket = '15'
        else:
            basket = '16'

        link_str = f"https://basket-{basket}.wb.ru/vol{_short_id}/part{ID//1000}/{ID}/images/big/1.jpg"
        return link_str


ClassWB = WildBerriesParser()




