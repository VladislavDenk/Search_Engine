import os
import emails
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PATH_TO_FILE: str = Path(r"{}".format(os.environ.get("path_to_file")))

SENDER: str = os.environ.get("sender_email")
PASSWORD: str = os.environ.get("password_sender_email")
HOST: str = os.environ.get("smtp_server_mail")
PORT: int = int(os.environ.get("smtp_port_mail"))
MESSAGE = os.environ.get("message")

TEAMS_ROW = os.environ.get("teams", "")
TEAMS = [t.strip() for t in TEAMS_ROW.split(",") if t.strip()]

RECIPIENTS_SCL = os.environ.get("recipients_scl", "")
RECIPIENTS_GAZOIL = os.environ.get("recipients_gazoil", "")
RECIPIENTS_RAZVITIE = os.environ.get("recipients_razvitie", "")


def pars_recipients(row: str | None):
    """Парсинг получателей"""
    if not row:
        return []
    return [r.strip() for r in row.split(",") if r.strip()]

def send_message(file_name: str, team_name: str):
    """Отправляет письма с отчетом назначенным получателям"""
    # Определение получателей письма
    recipients = None
    if team_name == TEAMS[0]:
        recipients = RECIPIENTS_SCL
    elif team_name == TEAMS[1]:
        recipients = RECIPIENTS_GAZOIL
    elif team_name == TEAMS[2]:
        recipients = RECIPIENTS_RAZVITIE
        
    if recipients is None:
        print(f"❗Не найден получатель для команды: {team_name}")
        return
    
    # Формирование списка получателей
    recipients_list = pars_recipients(recipients)
    if not recipients_list:
        print("❗Список получателей пуст после парсинга.")
        return

    # Формирование письма
    message = emails.html(
        subject = f"Реестр СИ - {team_name}.",
        html = MESSAGE or "<p>Реестр СИ с актуализированными данными.</p>",
        mail_from = ("Иванов Владислав", SENDER),
    )

    # Вставка файла с отчетом в письмо
    message.attach(
        filename=file_name,
        data=open(file_name, "rb")
    )
    
    # Отправление письма
    try:
        response = message.send(
            to = recipients_list,
            smtp={
                "host": HOST, 
                "port": PORT, 
                "ssl": True, 
                "user": SENDER, 
                "password": PASSWORD},
        )

        if response.status_code == 250:
            print(f"✅ Сообщение успешно отправлено сотрудникам {team_name}!")
        else:
            print(f"❌ Отправка прекращена: {response.status_code}")
    except Exception as e:
        # Это покажет реальную ошибку SMTP (аутентификации, соединения и пр.)
        print(f"❗ Ошибка при отправке письма: {e}")
        raise