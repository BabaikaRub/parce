from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import os
import csv

from config import get_info


def create_driver():
    ua = UserAgent()

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument("--headless")

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"  # не дожидаемся полноценной загрузки страницы (eager)

    driver = webdriver.Chrome(desired_capabilities=caps, service=Service(ChromeDriverManager().install()))

    return driver


def collect_data():

    with open("report_metro.csv", 'w', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=',')

        writer.writerow(
            (
                'Продукт',
                'Цена',
                'Цена со скидкой',
            )
        )

    links = get_info("../db.xlsx", 7)

    for link in links:

        try:
            chrome_driver = create_driver()
            chrome_driver.get(url=link)
            # delay = 3
            #
            # try:
            #     page = WebDriverWait(chrome_driver, delay).until(EC.presence_of_element_located((By.ID, "price-card__oldprice")))
            #
            #     with open(f'index_metro.html', 'w', encoding="utf-8") as file:
            #         file.write(chrome_driver.page_source)
            #
            # except TimeoutException:
            #     print("Загрузка слишком долгая!!!") # не работает, надо фиксить

            with open('index_metro.html', encoding='utf-8') as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')

            try:
                title = soup.find('h1', itemprop="name").text.strip()

            except AttributeError:
                title = link

            price_now = soup.find('span', itemprop='price').text.strip().split()[0]

            try:
                old_price = soup.find('div', class_='price-card__oldprice').text.strip().split()[0]

            except AttributeError:
                old_price = 'Скидки нет'

            with open("report_metro.csv", 'a', encoding='cp1251') as file:
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
    os.remove('index_metro.html')


def main():
    collect_data()


if __name__ == "__main__":
    main()