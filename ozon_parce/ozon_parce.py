from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec

import csv
import os

from config import get_info


def create_driver():
    ua = UserAgent()

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver


def collect_data():

    with open("report_ozon.csv", 'w', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=',')

        writer.writerow(
            (
                'Продукт',
                'Текущ. цена',
                'Цена до скидки'
            )
        )

    links = get_info("../db.xlsx", 8)

    for link in links:

        try:
            chrome_driver = create_driver()
            chrome_driver.get(url=link)
            element = WebDriverWait(chrome_driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))

            with open(f'index_ozon.html', 'w', encoding="utf-8") as file:
                file.write(chrome_driver.page_source)

            with open('index_ozon.html', encoding='utf-8') as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')

            try:
                title = soup.find('h1', class_="z3l").text.strip()

            except AttributeError:
                title = soup.find('h1', class_="z3l").text.strip()

            try:
                disc_price = soup.find('span', class_='yl1 ly2').text.strip().split()[0]

            except AttributeError:
                disc_price = soup.find('span', class_='yl1 y1l').text.strip().split()[0]

            try:
                old_price = soup.find('span', class_='l2y').text.strip().split()[0]

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

        except Exception as ex:
            print(ex)

        finally:
            chrome_driver.close()
            chrome_driver.quit()

    print('Файл успешно записан')
    os.remove('index_ozon.html')


def main():
    collect_data()


if __name__ == "__main__":
    main()
