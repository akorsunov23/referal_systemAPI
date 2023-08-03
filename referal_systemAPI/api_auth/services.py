import os

import requests
from dotenv import load_dotenv

load_dotenv()


def send_sms(phones, code):
    login = os.getenv('LOGIN_SMS')
    password = os.getenv("PASS_SMS")
    message = f"Код для аутентификации на сервисе: {code}"
    response = requests.post(
        f"https://smsc.ru/sys/send.php?"
        f"login={login}&"
        f"psw={password}&"
        f"phones={phones}&"
        f"mes={message}"
    )

    if "ERROR" in response.content.decode("utf-8"):
        return False
    return True
