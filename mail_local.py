import json
import os
import asyncio
from recevoir_mail import *

def enregistrer_mail():
    data = recevoir_email()  # On attend que recevoir_email soit aussi async
    os.makedirs('mail', exist_ok=True)
    with open("mail/mail.json", "w") as f:
        json.dump(data, f)

def lire_mail():
    os.makedirs('mail', exist_ok=True)
    with open("mail/mail.json", "r") as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    print(lire_mail())