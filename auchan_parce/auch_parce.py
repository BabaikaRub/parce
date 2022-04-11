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
        link = sheet[row][10].value

        if link is None:
            continue
        else:
            db.append(link)

    return db


