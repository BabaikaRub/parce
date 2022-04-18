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

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    return driver


def collect_data():

    # headers = {
    #     'User-Agent': ua.random,
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Cache-Lontrol": "max - age = 0",
    #     "Connection": "keep-alive",
    # }

    with open("report_dixy.csv", 'w', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=',')

        writer.writerow(
            (
                'Продукт',
                'Цена',
                'Цена со скидкой',
            )
        )

    links = get_info("../db.xlsx", 11)
    chrome_driver = create_driver()

    for link in links:

        try:
            chrome_driver.get(url=link)
            chrome_driver.set_page_load_timeout(30)

            with open(f'index_dixy.html', 'w', encoding="utf-8") as file:
                file.write(chrome_driver.page_source)

            with open('index_dixy.html', encoding='utf-8') as file:
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

        except Exception as ex:
            print(ex)

        finally:
            chrome_driver.close()
            chrome_driver.quit()

    print('Файл успешно записан')
    os.remove('../index_dixy.html')


def main():
    collect_data()


if __name__ == "__main__":
    main()

