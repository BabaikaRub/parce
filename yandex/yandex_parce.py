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

    with open("report_yandex.csv", 'w', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=',')

        writer.writerow(
            (
                'Продукт',
                'Цена',
                'Цена со скидкой',
            )
        )

    links = get_info("../db.xlsx", 6)

    for link in links:

        try:
            chrome_driver = create_driver()
            chrome_driver.get(url=link)
            chrome_driver.set_page_load_timeout(10)

            with open(f'index_yandex.html', 'w', encoding="utf-8") as file:
                file.write(chrome_driver.page_source)

            with open('index_yandex.html', encoding='utf-8') as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')

            try:
                title = soup.find('span', class_="ttu50to t18stym3 hbhlhv b1ba12f6 b1wwsurb n1wpn6v7 l14lhr1r").text.strip()

            except AttributeError:
                title = link

            try:
                price_now = soup.find('span', class_="t15aiivf t18stym3 t38p0ru b1ba12f6 bkuxkry t1wnuyqt l14lhr1r").text.strip().split()[0]

            except AttributeError:
                price_now = "Товара нет"

            try:
                old_price = soup.find('span', class_='t18stym3 b1clo64h r88klks r1b0wfc3 tnicrlv l14lhr1r').text.strip().split()[0]

            except AttributeError:
                old_price = 'Скидки нет'

            with open("report_yandex.csv", 'a', encoding='cp1251') as file:
                writer = csv.writer(file, delimiter=',')

                writer.writerow(
                    (
                        title,
                        price_now,
                        old_price,
                    )
                )

        except Exception as ex:
            print(ex)

        finally:
            chrome_driver.close()
            chrome_driver.quit()

    print('Файл успешно записан')
    os.remove('index_yandex.html')


def main():
    collect_data()


if __name__ == "__main__":
    main()
