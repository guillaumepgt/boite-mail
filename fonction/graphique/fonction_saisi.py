def vider_saisi_entry(event, entry):
    if entry.get() == "Recherche des mails":
        entry.delete(0, END)

def vider_saisi_text(event, widget):
    contenu = widget.get("1.0", "end-1c").strip()
    if contenu in ["Ecrire un mail", "Ecrire un objet", "Ecrire une adresse mail"]:
        widget.delete("1.0", "end")

def afficher_message(canvas, expediteur, destinataire, sujet, contenu, y_offset, largeur_ecran, hauteur_ecran):
    align = "e" if expediteur == destinataire else "w"

    bulle_width = largeur_ecran * 0.6
    bulle_bords = 20

    x_offset = 20 if align == "w" else largeur_ecran * 0.8 - bulle_width - 20

    font = ("Courier", 14)
    text = sujet + "\n" + contenu
    text_height = get_text_height(canvas, text, font, bulle_width)
    bulle_height = text_height + 3 * bulle_bords

    # Dessiner l'ombre
    rectangle_arrondi(canvas,
                      x_offset + 10,
                      y_offset + 10,
                      x_offset + bulle_width + 10,
                      y_offset + bulle_height + 10,
                      radius=15,
                      fill="gray", outline="gray", width=2)

    # Dessiner la bulle
    rectangle_arrondi(canvas,
                      x_offset,
                      y_offset,
                      x_offset + bulle_width,
                      y_offset + bulle_height,
                      radius=15,
                      fill="#e1f5fe", outline="black", width=2)

    # Ajouter le texte
    canvas.create_text(x_offset + bulle_bords,
                       y_offset + bulle_bords,
                       text=sujet + "\n\n   " + contenu,
                       font=font,
                       anchor="nw",
                       fill="black",
                       width=bulle_width - 2 * bulle_bords)

    # Retourner la nouvelle position Y pour le prochain message
    return y_offset + bulle_height + 30  # 30 = espace entre deux bulles

try:
    from fonction.graphique.fonction_design import *
except ModuleNotFoundError:
    if __name__ == "__main__":
        from fonction_design import *