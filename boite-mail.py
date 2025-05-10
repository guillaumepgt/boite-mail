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
from fonction.graphique.fonction_bouton import *
from fonction.graphique.fonction_saisi import *

fenetre, largeur, hauteur = start() # chargement de la fenêtre
images = charger_images(fenetre) # chargement des images

# Création des 4 rectangles de menu
page_accueil(fenetre, images, largeur, hauteur)
fenetre.mainloop()