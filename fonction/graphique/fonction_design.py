from tkinter import *

def rectangle_arrondi(canvas, x1, y1, x2, y2, radius, **kwargs):
    # Dessiner un rectangle avec des coins arrondis en utilisant des arcs de cercle
    return canvas.create_polygon(
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        fill=kwargs.get('fill', 'white'),
        outline=kwargs.get('outline', 'black'),
        width=kwargs.get('width', 1),
        smooth=True
    )

# Fonction pour ajuster la hauteur de la bulle en fonction du texte
def get_text_height(canvas, text, font, width):
    # Créer un texte temporaire pour mesurer la hauteur
    text_id = canvas.create_text(0, 0, text=text, font=font, width=width)
    bbox = canvas.bbox(text_id)  # Récupérer la bounding box du texte
    height = bbox[3] - bbox[1]  # Calculer la hauteur
    canvas.delete(text_id)  # Supprimer le texte temporaire
    return height

def creer_bouton(fenetre, images, largeur_ecran, hauteur_ecran, x, y, image, texte, commande):
    return Button(
        fenetre, text=texte, image=images[image], font=("Arial", 20),
        bg="lightblue", fg="black", relief="flat",
        activebackground="white", activeforeground="black",
        compound="bottom", pady=20, command=commande
    ).place(x=largeur_ecran*x, y=hauteur_ecran*y, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)

def create_canvas_with_scrollbar(fenetre, largeur, hauteur):
    canvas = Canvas(fenetre, bg="white", bd=1)
    canvas.place(x=largeur * 0.1, y=hauteur * 0.1, width=largeur * 0.8, height=hauteur * 0.8)
    scrollbar = Scrollbar(fenetre, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    return canvas