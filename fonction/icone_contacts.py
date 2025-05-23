from PIL import Image, ImageDraw, ImageFont
import random
import os
from tkinter import PhotoImage

def generer_couleur_fond():
    couleurs = [
        "#E57373", "#F06292", "#BA68C8", "#64B5F6",
        "#4DB6AC", "#81C784", "#FFD54F", "#FFB74D",
        "#A1887F", "#90A4AE"
    ]
    return random.choice(couleurs)

def lettres(name):
    lettre = name[0]
    for i in range(len(name)):
        if name[i] == " ":
            lettre += name[i+1].upper()
    return lettre

def creer_icone_initiales(name, mail, taille=100, dossier="private/icones"):
    if os.path.isfile(f"private/icones/{mail}.png"):
        return f"private/icones/{mail}.png"
    os.makedirs(dossier, exist_ok=True)

    couleur_fond = generer_couleur_fond()
    image = Image.new("RGB", (taille, taille), couleur_fond)
    masque = Image.new("L", (taille, taille), 0)
    draw_masque = ImageDraw.Draw(masque)
    draw_masque.ellipse((0, 0, taille, taille), fill=255)
    image.putalpha(masque)

    draw = ImageDraw.Draw(image)

    taille_police = int(taille * 0.5)

    try:
        font = ImageFont.truetype("fonts/Poppins-SemiBold.ttf", taille_police)
    except Exception as e:
        print("❌ ERREUR : Impossible de charger la police personnalisée.")
        print(str(e))
        return
    lettre = lettres(name)
    # Calculer les dimensions du texte
    bbox = draw.textbbox((0, 0), lettre.upper(), font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Centrer le texte dans l'image
    position = ((taille - text_width) / 2, (taille - text_height) / 3)

    # Dessiner le texte
    draw.text(position, lettre.upper(), font=font, fill="white")

    chemin_fichier = os.path.join(dossier, f"{mail}.png")
    image.save(chemin_fichier)

    return chemin_fichier

def enregistrer_icone_tkinter(contact):
    cache_images = {}
    for i in contact:
        cache_images[i["Email"]] = PhotoImage(file=creer_icone_initiales(i["Nom"], i["Email"]))
    return cache_images

if __name__ == "__main__":
    creer_icone_initiales("t t", "test")
