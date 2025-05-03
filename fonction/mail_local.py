import json
import os
import asyncio

def enregistrer_mail(fonction,chemin):
    data = fonction()  # On attend que recevoir_email soit aussi async
    os.makedirs('../mail', exist_ok=True)
    with open(f"mail/{chemin}.json", "w") as f:
        json.dump(data, f)

def lire_mail(chemin):
    os.makedirs('../mail', exist_ok=True)
    with open(f"mail/{chemin}.json", "r") as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    from recevoir_mail import *
    print(lire_mail())
else:
    from fonction.recevoir_mail import *