import json
import os
import asyncio
from recevoir_mail import *

async def enregistrer_mail():
    data = await recevoir_email()  # On attend que recevoir_email soit aussi async
    os.makedirs('mail', exist_ok=True)
    # L'écriture de fichier sera faite de manière non bloquante
    loop = asyncio.get_running_loop()
    with open("mail/mail.json", "w") as f:
        await loop.run_in_executor(None, json.dump, data, f, 4)

def lire_mail():
    os.makedirs('mail', exist_ok=True)
    with open("mail/mail.json", "r") as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    print(lire_mail())