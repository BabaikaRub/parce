import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import openpyxl

book = openpyxl.open('../db.xlsx', read_only=True)

sheet = book.active

db = []

for row in range(7, sheet.max_row + 1):
    link = sheet[row][5].value

    if link is None:
        continue
    else:
        db.append(link)


def collect_data():
    ua = UserAgent()

    headers = {
        'User-Agent': ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Lontrol": "max - age = 0",
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

    for link in db:

        response = requests.get(url=f'{link}', headers=headers)

        with open(f'../index_per.html', 'w', encoding="utf-8") as file:
            file.write(response.text)

        with open('../index_per.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        title = soup.find('h1', class_="product__title").text.strip()

        try:
            old_price = soup.find('div', class_='price-old').text.strip().split()[0]

        except AttributeError:
            old_price = "На товар нет скидки"

        price_now = soup.find('div', class_='price-new').text.strip().split()[0]

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


def main():
    collect_data()


if __name__ == "__main__":
    main()
