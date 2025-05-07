from tkinter import *
import platform

def start():

    fenetre = Tk()
    fenetre.title("Boite Mail")
    fenetre.attributes("-fullscreen", True)  # Active le mode plein écran
    fenetre.bind("<Escape>", lambda event: fenetre.attributes("-fullscreen", False)) # Quitter le plein écran avec Échap

    largeur_ecran = fenetre.winfo_screenwidth()
    hauteur_ecran = fenetre.winfo_screenheight()
    return fenetre, largeur_ecran, hauteur_ecran

def discussion(fenetre, adresse_mail, page, images, largeur_ecran, hauteur_ecran):
    global fenetre_discussion
    # Création d'une nouvelle fenêtre (évite les conflits avec Tk)
    fenetre_discussion = Toplevel(fenetre)
    fenetre_discussion.title("Discuter")
    fenetre_discussion.attributes("-fullscreen", True)

    Button(fenetre_discussion, image=images["home"], relief="flat", command=lambda: fenetre_discussion.destroy()).place(x=largeur_ecran * 0.05, y=hauteur_ecran * 0.05)
    Button(fenetre_discussion, image=images["exit"], relief="flat", command=fenetre.quit).place(x=largeur_ecran * 0.95, y=hauteur_ecran * 0.05)

    canvas = Canvas(fenetre_discussion, bg="white", bd=1)
    canvas.place(x=largeur_ecran * 0.1, y=hauteur_ecran * 0.1, width=largeur_ecran * 0.8, height=hauteur_ecran * 0.8)

    # Scrollbar liée au Canvas
    my_scrollbar = Scrollbar(fenetre_discussion, orient=VERTICAL, command=canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=my_scrollbar.set)

    # Calculer les mails à afficher
    mails = lire_mail({"boite_principal":"mail", "envoye":"envoye_list", "corbeille": "corbeille_list"}[page])
    liste_mails = [m for m in mails if m[{"boite_principal": "Expéditeur", "envoye": "Destinataire", "corbeille": "Expéditeur"}[page]] == adresse_mail]
    # Inverser l’ordre pour avoir du plus ancien au plus récent
    liste_mails = liste_mails[::-1]

    # Étape 1 : Mesurer la hauteur totale des messages (sans les afficher)
    font = ("Courier", 14)
    bulle_width = largeur_ecran * 0.6
    bulle_bords = 20
    total_height = 0
    for mail in liste_mails:
        text = mail["Sujet"] + "\n" + mail["Contenu"]
        text_height = get_text_height(canvas, text, font, bulle_width)
        bulle_height = text_height + 3 * bulle_bords
        total_height += bulle_height + 30  # espacement

    # Étape 2 : Démarrer plus bas si le contenu ne remplit pas le canvas
    visible_height = hauteur_ecran * 0.8
    y_offset_total = max(20, visible_height - total_height)

    for mail in liste_mails:
        expediteur = mail["Expéditeur"]
        destinataire = mail["Destinataire"]
        sujet = mail["Sujet"]
        contenu = mail["Contenu"]

        # Appeler la fonction pour afficher le message
        y_offset_total = afficher_message(canvas, expediteur, destinataire, sujet, contenu, y_offset_total, largeur_ecran, hauteur_ecran)

    canvas.configure(scrollregion=(0, 0, largeur_ecran * 0.8, y_offset_total))
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

    if platform.system() in ['Windows', 'Darwin']:
        canvas.bind_all("<MouseWheel>", lambda e: scroll_canvas(canvas, e))
    else:
        canvas.bind_all("<Button-4>", lambda e: scroll_canvas(canvas, e))
        canvas.bind_all("<Button-5>", lambda e: scroll_canvas(canvas, e))

try:
    from fonction.mail_local import *
    from fonction.graphique.fonction_design import *
    from fonction.graphique.fonction_saisi import *
    from fonction.graphique.scroll import *
except ModuleNotFoundError:
    if __name__ == "__main__":
        import sys
        from fonction_design import *
        from fonction_saisi import *
        from scroll import *
        sys.path.append("..")
        from mail_local import *
        fenetre = start()[0]
        fenetre.mainloop()