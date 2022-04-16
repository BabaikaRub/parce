import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import openpyxl
import os

book = openpyxl.open('../db.xlsx', read_only=True)

sheet = book.active

db = []

for row in range(7, sheet.max_row + 1):
    link = sheet[row][8].value

    if link is None:
        continue
    else:
        db.append(link)


def collect_data():
    ua = UserAgent()

    headers = {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }

    with open("report_ozon.csv", 'w', encoding='cp1251') as file:
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

        with open(f'../index_ozon.html', 'w', encoding="utf-8") as file:
            file.write(response.text)

        with open('../index_ozon.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        try:
            title = soup.find('h1', class_="x9k").text.strip()
            #print(title)
        except AttributeError:
            title = link

        try:
            disc_price = soup.find('span', class_='wk7').text.strip().split()[0]
            #print(disc_price)

        except AttributeError:
            disc_price = 'На товар есть скидка'

        try:
            old_price = soup.find('span', class_='k8w').text.strip().split()[0]

        except AttributeError:
            old_price = "На товар нет скидки"

        with open("report_ozon.csv", 'a', encoding='cp1251') as file:
            writer = csv.writer(file, delimiter=',')

            writer.writerow(
                (
                    title,
                    disc_price,
                    old_price,
                )
            )

    print('Файл успешно записан')
    os.remove('../index_ozon.html')


def main():
    collect_data()


if __name__ == "__main__":
    main()
