import time
from tkinter import *
import asyncio
import shutil
import platform

# fichier parti gestion des mails
from fonction.envoyer_mail import *
from fonction.recevoir_mail import *
from fonction.recevoir_information import *
from fonction.contact import *
from fonction.icone_contacts import *
from fonction.mail_local import *

# fichier parti graphique
from fonction.graphique.fenetre import *
from fonction.graphique.chargement_image import *
from fonction.graphique.scroll import *
from fonction.graphique.fonction_bouton import *
from fonction.graphique.fonction_saisi import *

fenetre, largeur_ecran, hauteur_ecran = start() # chargement de la fenêtre
images = charger_images(fenetre) # chargement des images

# Création des 4 rectangles de menu
def page_accueil():
    bouton_boite_de_reception = Button(fenetre, text="Boite de réception", image=images["mail"], font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20, command=lambda: reception(fenetre, images, largeur_ecran, hauteur_ecran, 1, "boite_de_reception"))
    bouton_boite_de_reception.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.2, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)

    bouton_ecrire_mail = Button(fenetre, text="Ecrire un mail", image=images["ecrire"], font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20, command=lambda: ecrire_mail(fenetre, images, largeur_ecran, hauteur_ecran,))
    bouton_ecrire_mail.place(x=largeur_ecran*0.55, y=hauteur_ecran*0.2, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)

    bouton_label = Button(fenetre, text="Categories", image=images["label"], font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20, command=lambda: label(fenetre, images, largeur_ecran, hauteur_ecran))
    bouton_label.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.6, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)

    bouton_corbeille = Button(fenetre, text="Corbeille", image=images["poubelle"], font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20, command=lambda: reception(fenetre, images, largeur_ecran, hauteur_ecran, 1, "corbeille"))
    bouton_corbeille.place(x=largeur_ecran*0.55, y=hauteur_ecran*0.6, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)

    bouton_settings = Button(fenetre, image=images["profil"], relief="flat", command=lambda: parametre(fenetre, bouton_settings))
    bouton_settings.place(x=largeur_ecran*0.05, y=hauteur_ecran*0.05)
    Button(fenetre, image=images["exit"], relief="flat", command=fenetre.quit).place(x=largeur_ecran*0.95, y=hauteur_ecran*0.05)

page_accueil()
fenetre.mainloop()