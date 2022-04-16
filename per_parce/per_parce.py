import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os

from config import get_info


def collect_data():
    ua = UserAgent()

    headers = {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max - age = 0",
    }

    with open("report_perek.csv", 'w', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=',')

        writer.writerow(
            (
                'Продукт',
                'Текущ. цена',
                'Цена до скидки'
            )
        )

    links = get_info("../db.xlsx", 5)

    for link in links:

        response = requests.get(url=f'{link}', headers=headers)

        with open(f'../index_per.html', 'w', encoding="utf-8") as file:
            file.write(response.text)

        with open('../index_per.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        try:
            title = soup.find('h1', class_="product__title").text.strip()

        except AttributeError:
            title = link

        try:
            old_price = soup.find('div', class_='price-old').text.strip().split()[0]

        except AttributeError:
            old_price = "На товар нет скидки"

        try:
            price_now = soup.find('div', class_='price-new').text.strip().split()[0]

        except AttributeError:
            price_now = "Перепроверь товар!"

        with open("report_perek.csv", 'a', encoding='cp1251') as file:
            writer = csv.writer(file, delimiter=',')

            writer.writerow(
                (
                    title,
                    price_now,
                    old_price
                )
            )

    print('Файл успешно записан')
    os.remove('../index_per.html')


def main():
    collect_data()


if __name__ == "__main__":
    main()
