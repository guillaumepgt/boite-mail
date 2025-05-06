import json
import os
import asyncio
import threading
import queue


async def enregistrer_mail(fonction,chemin, nom_fichier):
    data = fonction()
    os.makedirs(chemin, exist_ok=True)
    # Écriture fichier de manière "bloquante" dans un thread séparé
    json.dump(data, open(f"{chemin}{nom_fichier}.json", "w"))

def lire_mail(chemin):
    if os.path.exists(f"../private/mail/{chemin}.json"):
        chemin = f"../private/mail/{chemin}.json"
    elif os.path.exists(f"private/mail/{chemin}.json"):
        chemin = f"private/mail/{chemin}.json"
    else:
        return []
    with open(chemin, "r") as f:
        data = json.load(f)
    return data

def start_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(
        enregistrer_mail(recevoir_email, "private/mail/", "mail"),
        enregistrer_mail(recevoir_email2, "private/mail/", "full_name_list"),
        enregistrer_mail(recevoir_brouillons, "private/mail/", "brouillon_list"),
        enregistrer_mail(recevoir_corbeille, "private/mail/", "corbeille_list"),
        enregistrer_mail(recevoir_corbeille2, "private/mail/", "full_name_list_corbeille"),
        enregistrer_mail(recevoir_envoyes, "private/mail/", "envoye_list"),
        enregistrer_mail(recevoir_envoyes2, "private/mail/", "envoye_name_list")
    ))

if __name__ == '__main__':
    from recevoir_mail import *
    from contact import *
    from brouillon import *
    from corbeille import *
    from envoyer_mail import *
    print(lire_mail("mail"))
else:
    from fonction.contact import *
    from fonction.recevoir_mail import *
    from fonction.brouillon import *
    from fonction.corbeille import *
    from fonction.envoyer_mail import *