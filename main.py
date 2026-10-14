import os
import sqlite3 as sql
import pandas as pd
from pathlib import Path

from datetime import datetime

from models import adding_data, create_table_for_team, drop_tables
from sender_report import send_message, TEAMS, PATH_TO_FILE

today: datetime = datetime.now()


def get_value(name_base: str):
    "Получение значений из файла и запись их в БД"
    books = pd.read_excel(PATH_TO_FILE, sheet_name=name_base)
    for i, date in enumerate(books[31]):
        if isinstance(date, datetime) and date <= today:
            responsible = books[0][i]
            number_object = books[1][i]
            name_equipment = books[2][i]
            equipment_type = books[3][i]
            factory_number = books[4][i]
            verification_date = books[31][i].strftime("%d.%m.%Y")
            adding_data(
                responsible,
                number_object,
                name_equipment,
                equipment_type,
                factory_number,
                verification_date,
                name_base
            )


def write_value(book_title: str) -> str:
    "Запись данных в файл формата .xlsx"
    conn = sql.connect("verification.db")
    query = "SELECT * FROM {}".format(book_title)
    data = pd.read_sql_query(query, conn)
    file_name = f"Просроченные поверки СИ на ОПО {book_title.split("_")[1]} на {datetime.date(today).strftime("%d.%m.%Y")}г..xlsx"
    data.to_excel(file_name, index=False, sheet_name=book_title)
    print(f"✅ Экспорт данных компании {book_title.split("_")[1]} прошел успешно!")
    conn.close()
    return file_name


if __name__ == "__main__":
    
    print("🧹 Очистка старых таблиц в БД...")
    
    # Формирование списка наименований книг в таблице Excel
    BOOK_TITLES = [f"Оборудование_{team}" for team in TEAMS]
    
    # Удаление таблиц в БД
    drop_tables(BOOK_TITLES)
    
    for i, team in enumerate(TEAMS):
        print(f"Обработка данных компании {team}")
        # Получаем данные о СИ компании
        get_value(name_base=BOOK_TITLES[i])
        # Создаем файл отчета о состоянии СИ компании
        file_name: str = write_value(book_title=BOOK_TITLES[i])
        # Отправляем письмо с отчетом сотрудникам компании
        send_message(file_name=file_name, team_name=team)
    
    print("🏁 Все команды обработаны.")