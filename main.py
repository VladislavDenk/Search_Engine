import sqlite3 as sql
import pandas as pd

from datetime import datetime

from models import adding_data, name_team
from sender_report import send_message, TEAMS

today = datetime.now()


def get_value(name_base: str):
    "Получение значений из файла и запись их в БД"
    books = pd.read_excel("base.xls", sheet_name=name_base)
    # result_list = []
    for i, date in enumerate(books[13]):
        if isinstance(date, datetime) and date <= today:
            # # Для вывода значений в консоль
            # responsible = books[0][i]
            # number_object = books[2][i]
            # name_equipment = books[4][i]
            # equipment_type = books[5][i]
            # factory_number = books[6][i]
            # verification_date = books[13][i].strftime('%d.%m.%Y')
            # print(verification_date)
            # result = (responsible, number_object, name_equipment, equipment_type, factory_number, verification_date)
            # result_list.append(result)
            # for i in result_list:
            #     print(i)

            # Для записи в БД
            responsible = books[0][i]
            number_object = books[2][i]
            name_equipment = books[4][i]
            equipment_type = books[5][i]
            factory_number = books[6][i]
            verification_date = books[13][i].strftime("%d.%m.%Y")
            adding_data(
                responsible,
                number_object,
                name_equipment,
                equipment_type,
                factory_number,
                verification_date
            )


def write_value(name: str) -> str:
    "Запись данных в файл формата .xlsx"
    conn = sql.connect("verification.db")
    query = "SELECT * FROM {}".format(name_team)
    data = pd.read_sql_query(query, conn)
    file_name = "{}.xlsx".format(name)
    data.to_excel(file_name, index=False, sheet_name=name_team)
    print("Экспорт прошел успешно!")
    return file_name


if __name__ == "__main__":
    if name_team in TEAMS:
        get_value(name_base=name_team)
        file_name: str = write_value(name=name_team)
        send_message(file_name=file_name)
    else:
        print("Указанной компании нет в конфигурационном файле или указано не верное название компании.")
