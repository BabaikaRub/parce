import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import os

from config import get_info


def collect_data():
    ua = UserAgent()

    headers = {
        'User-Agent': ua.random
    }

    with open("report_utk.csv", 'w', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=',')

        writer.writerow(
            (
                'Продукт',
                'Цена',
                'Цена со скидкой',
                'Цена до скидки'
            )
        )

    links = get_info("../db.xlsx", 9)

    for link in links:
        # Добавить проверку существования данного арктикля
        response = requests.get(url=f'{link}', headers=headers)

        with open(f'../index_utk.html', 'w', encoding="utf-8") as file:
            file.write(response.text)

        with open('../index_utk.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        try:
            title = soup.find('h1', class_="product-base-info_name title-l2 ng-star-inserted").text.strip()

        except AttributeError:
            title = link

        try:
            def_price = soup.find('span', class_='product-sale-price title-l1 ng-star-inserted').text.strip().split()[0]
        except AttributeError:
            def_price = "На этот товар есть скидка"

        try:
            sale_price = soup.find('span', class_="product-sale-price title-l1 __accent ng-star-inserted").text.strip().split()[0]
            old_price = soup.find('span', class_="product-old-price--strike ng-star-inserted").text.strip().split()[0]

        except AttributeError:
            sale_price = 'Скидки нет'
            old_price = 'Скидки нет'

        with open("report_utk.csv", 'a', encoding='cp1251') as file:
            writer = csv.writer(file, delimiter=',')

            writer.writerow(
                (
                    title,
                    def_price,
                    sale_price,
                    old_price,
                )
            )

    print('Файл успешно записан')
    os.remove('../index_utk.html')


def main():
    collect_data()


if __name__ == "__main__":
    main()
