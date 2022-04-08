import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import openpyxl

import os


def get_info(file_name):
    book = openpyxl.open(file_name, read_only=True)

    sheet = book.active

    db = []

    for row in range(7, sheet.max_row + 1):
        link = sheet[row][9].value

        if link is None:
            continue
        else:
            db.append(link)

    return db


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

    links = get_info("../db.xlsx")

    for link in links:
        # Добавить проверку существования данного арктикля
        response = requests.get(url=f'{link}', headers=headers)
        #print('успешно')
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
            #print(price_now)
        except AttributeError:
            sale_price = 'Скидки нет'
            old_price = 'Скидки нет'



        #difference = float(old_price) - float(price_now)

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
