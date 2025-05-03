import json
import os
import asyncio
from recevoir_mail import *

def enregistrer_mail(fonction,chemin):
    data = fonction()  # On attend que recevoir_email soit aussi async
    os.makedirs('mail', exist_ok=True)
    with open(f"mail/{chemin}.json", "w") as f:
        json.dump(data, f)

def lire_mail(chemin):
    os.makedirs('mail', exist_ok=True)
    with open(f"mail/{chemin}.json", "r") as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    print(lire_mail())