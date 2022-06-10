from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import os
import csv

from config import get_info


def create_driver():
    ua = UserAgent()

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver


def collect_data():

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

        try:

            chrome_driver = create_driver()
            chrome_driver.get(url=link)

            with open(f'../index_per.html', 'w', encoding="utf-8") as file:
                file.write(chrome_driver.page_source)

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

        except Exception as ex:
            print(ex)

        finally:
            chrome_driver.close()
            chrome_driver.quit()

    print('Файл успешно записан')
    os.remove('../index_per.html')


def main():
    collect_data()


if __name__ == "__main__":
    main()
