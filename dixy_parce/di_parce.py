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
        link = sheet[row][11].value

        if link is None:
            continue
        else:
            db.append(link)

    return db


def collect_data():
    ua = UserAgent()

    headers = {
        'User-Agent': ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Lontrol": "max - age = 0",
        "Connection": "keep-alive",
    }

    with open("report_dixy.csv", 'w', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=',')

        writer.writerow(
            (
                'Продукт',
                'Цена',
                'Цена со скидкой',
            )
        )

    links = get_info("../db.xlsx")

    for link in links:

        response = requests.get(url=f'{link}', headers=headers)

        with open(f'../index_dixy.html', 'w', encoding="utf-8") as file:
            file.write(response.text)

        with open('../index_dixy.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        try:
            title = soup.find('h1', id="pagetitle").text.strip()

        except AttributeError:
            title = link

        price_now = soup.find('span', class_='price_value').text.strip()

        try:
            old_price = soup.find('div', class_='sticker_aktsiya font_sxs rounded2').text.strip()

        except AttributeError:
            old_price = 'Скидки нет'

        with open("report_dixy.csv", 'a', encoding='cp1251') as file:
            writer = csv.writer(file, delimiter=',')

            writer.writerow(
                (
                    title,
                    price_now,
                    old_price,
                )
            )

    print('Файл успешно записан')
    os.remove('../index_dixy.html')


def main():
    collect_data()


if __name__ == "__main__":
    main()

