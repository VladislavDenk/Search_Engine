import os
import emails
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

SENDER: str = os.environ.get("sender_email")
PASSWORD: str = os.environ.get("password_sender_email")
HOST: str = os.environ.get("smtp_server_mail")
PORT: int = int(os.environ.get("smtp_port_mail"))


def send_message(file_name):
    message = emails.html(
        subject = "Реестр СИ.",
        html = "<p>Здравствуйте! Во вложении реестр СИ с актуализированными данными. Просьба сверить данные и в случае обнаружения несоответствий исправить их, выделяя цветом места испралений, и направить скорректированный реестр СИ ответным письмом.</p>",
        mail_from = ("me", SENDER)
    )

    message.attach(
        filename=file_name,
        data=open(file_name, "rb")
    )

    response = message.send(
        to = "ivanovvladislav070@xmail.ru",
        smtp={
            "host": HOST, 
            "port": PORT, 
            "ssl": True, 
            "user": SENDER, 
            "password": PASSWORD},
    )

    if response.status_code == 250:
        print("Сообщение успешно отправлено!")
    else:
        print(f"Отправка прекращена: {response.status_code}")