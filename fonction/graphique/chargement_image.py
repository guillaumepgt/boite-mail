from tkinter import PhotoImage
import shutil
import threading
import asyncio

def charger_images(fenetre):
    # Icônes classiques
    chemin_image_mail = r"img/mail.png"
    photo_mail = PhotoImage(file=chemin_image_mail)

    chemin_image_ecrire = r"img/ecrire.png"
    photo_ecrire = PhotoImage(file=chemin_image_ecrire)

    chemin_image_label = r"img/label.png"
    photo_label = PhotoImage(file=chemin_image_label)

    chemin_image_poubelle = r"img/poubelle.png"
    photo_poubelle = PhotoImage(file=chemin_image_poubelle)

    chemin_image_settings = r"img/settings.png"
    photo_settings = PhotoImage(file=chemin_image_settings)

    chemin_image_home = r"img/home.png"
    photo_home = PhotoImage(file=chemin_image_home)

    chemin_image_exit = r"img/exit.png"
    photo_exit = PhotoImage(file=chemin_image_exit)

    chemin_image_line = r"img/line.png"
    photo_line = PhotoImage(file=chemin_image_line)

    # Image de profil
    chemin_image_profil = r"img/profil.png"
    if connecter():
        threading.Thread(target=start_async_loop, daemon=True).start()
        chemin_image_profil = download_profil_img(get_user_info()["picture"])

    photo_profil = PhotoImage(file=chemin_image_profil)

    # Empêcher la suppression des images
    for img in [photo_mail, photo_ecrire, photo_label, photo_poubelle, photo_settings,
                photo_home, photo_exit, photo_line, photo_profil]:
        img.image = img

    # Retourner un dictionnaire
    return {
        "mail": photo_mail,
        "ecrire": photo_ecrire,
        "label": photo_label,
        "poubelle": photo_poubelle,
        "settings": photo_settings,
        "profil": photo_profil,
        "home": photo_home,
        "exit": photo_exit,
        "line": photo_line,
        "cache_image": {}
    }

try:
    from fonction.recevoir_information import *
    from fonction.mail_local import *
except ModuleNotFoundError:
    import sys
    sys.path.append("..")
    from mail_local import *
    from recevoir_information import *