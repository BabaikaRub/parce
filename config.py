
import openpyxl


def get_info(file_name, column):
    book = openpyxl.open(file_name, read_only=True)

    sheet = book.active

    db = []

    for row in range(7, sheet.max_row + 1):
        link = sheet[row][column].value

        if link is None:
            continue
        else:
            db.append(link)

    return db
