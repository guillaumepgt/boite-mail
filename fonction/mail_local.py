import json
import os
import asyncio
import threading
import queue


async def enregistrer_mail(fonction, chemin, nom_fichier):
    data = fonction
    os.makedirs(chemin, exist_ok=True)
    with open(os.path.join(chemin, f"{nom_fichier}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


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
    try:
        loop.run_until_complete(asyncio.gather(
            enregistrer_mail(recevoir_email("messages", 100), "private/mail/", "mail"),
            enregistrer_mail(recevoir_info(), "private/mail/", "full_name_list"),
            enregistrer_mail(recevoir_email("drafts", 10), "private/mail/", "brouillon_list"),
            enregistrer_mail(recevoir_corbeille(), "private/mail/", "corbeille_list"),
            enregistrer_mail(recevoir_info(label="TRASH", recipient_field="From"), "private/mail/", "full_name_list_corbeille"),
            enregistrer_mail(recevoir_envoyes(), "private/mail/", "envoye_list"),
            enregistrer_mail(recevoir_info(label="SENT", recipient_field="To"), "private/mail/", "envoye_name_list")
        ))
    except httplib2.error.ServerNotFoundError:
        print("aucune connexion")

try:
    from fonction.contact import *
    from fonction.recevoir_mail import *
    from fonction.corbeille import *
    from fonction.envoyer_mail import *
except ModuleNotFoundError:
    from recevoir_mail import *
    from contact import *
    from corbeille import *
    from envoyer_mail import *
    if __name__ == '__main__':
        print(lire_mail("mail"))