import sqlite3 as sql
import pandas as pd

from datetime import datetime

from models import adding_data, create_table_for_team, drop_tables
from sender_report import send_message, TEAMS

today = datetime.now()


def get_value(name_base: str):
    "Получение значений из файла и запись их в БД"
    books = pd.read_excel("base.xls", sheet_name=name_base)
    for i, date in enumerate(books[13]):
        if isinstance(date, datetime) and date <= today:
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
                verification_date,
                name_base
            )


def write_value(name: str) -> str:
    "Запись данных в файл формата .xlsx"
    conn = sql.connect("verification.db")
    query = "SELECT * FROM {}".format(name)
    data = pd.read_sql_query(query, conn)
    file_name = "{}.xlsx".format(name)
    data.to_excel(file_name, index=False, sheet_name=name)
    print(f"✅ Экспорт данных компании {name} прошел успешно!")
    conn.close()
    return file_name


if __name__ == "__main__":
    
    print("🧹 Очистка старых таблиц в БД...")
    drop_tables(TEAMS)
    
    for team in TEAMS:
        print(f"Обработка данных компании {team}")
        # Создаем таблицу указанной компании
        create_table_for_team(team)
        # Получаем данные о СИ компании
        get_value(name_base=team)
        # Создаем файл отчета о состоянии СИ компании
        file_name: str = write_value(name=team)
        # Отправляем письмо с отчетом сотрудникам компании
        send_message(file_name=file_name)
    
    print("🏁 Все команды обработаны.")