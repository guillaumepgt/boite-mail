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

def reception(fenetre, images, largeur_ecran, hauteur_ecran, page, type, canvas=None):
    global fenetre_boite
    if page == 1 :
        # Création d'une nouvelle fenêtre
        fenetre_boite = Toplevel(fenetre)
        fenetre_boite.title("Boite de réception")
        fenetre_boite.attributes("-fullscreen", True)

        # Canvas pour permettre le scroll
        canvas = Canvas(fenetre_boite)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        recherche_mail = Entry(fenetre_boite, bg="white", fg="black", font="Courier", bd=2, justify=LEFT)
        recherche_mail.insert(0, "Recherche des mails")
        recherche_mail.place(x=largeur_ecran * 0.1, y=hauteur_ecran * 0.055,width=largeur_ecran * 0.3, height=hauteur_ecran * 0.05)

        recherche_mail.bind("<FocusIn>", lambda event: vider_saisi_entry(event, recherche_mail))

        bouton_home = Button(fenetre_boite, image=images["home"], relief="flat", command=lambda: fenetre_boite.destroy())
        bouton_home.place(x=largeur_ecran * 0.05, y=hauteur_ecran * 0.05)

        bouton_exit = Button(fenetre_boite, image=images["exit"], relief="flat", command=fenetre.quit)
        bouton_exit.place(x=largeur_ecran * 0.95, y=hauteur_ecran * 0.05)

        # Scrollbar liée au Canvas
        my_scrollbar = Scrollbar(fenetre_boite, orient=VERTICAL, command=canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=my_scrollbar.set)
    elif page == 2 :
        canvas.delete("all")  # vide le contenu précédent du canvas
        canvas.yview_moveto(0) # remettre le canvas en haut

        # Frame dans le canvas pour contenir tous les boutons
    frame_boite = Frame(canvas)
    frame_boite.bind("<Configure>",lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    # Créer une fenêtre dans le canvas
    canvas_frame = canvas.create_window((0, 0), window=frame_boite, anchor="nw")

    contact = lire_mail({"boite_de_reception" : "full_name_list", "corbeille": "full_name_list_corbeille"}[type])
    compteur = 0

    frame_boite.config(width=largeur_ecran, height=hauteur_ecran*3)
    for i in range(len(contact)):
        use = 0
        for j in range(i):
            if contact[i]["Nom"] == contact[j]["Nom"]:
                use = 1
        if use == 0:
            if contact[i]["Email"] not in images["cache_image"] :
                images["cache_image"] = enregistrer_icone_tkinter(contact)
            icone = images["cache_image"][contact[i]["Email"]]
            Button(frame_boite, compound="top", text=contact[i]["Nom"], image=icone, font=("Arial", 20),bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black",command=lambda email=contact[i]["Email"]: discussion(fenetre, email, {"boite_de_reception" : "boite_principal", "corbeille": "corbeille"}[type], images, largeur_ecran, hauteur_ecran)).place(
                x=largeur_ecran * [[0.1, 0.4, 0.7][compteur % 3], [0.05, 0.35, 0.65][compteur % 3]][page-1],
                y=hauteur_ecran * [(0.15 + 0.3 * (compteur // 3)), (0.3 * (compteur // 3))][page-1],
                width=largeur_ecran * 0.2,
                height=hauteur_ecran * 0.2
            )
            compteur += 1

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
    from fonction.icone_contacts import *
except ModuleNotFoundError:
    if __name__ == "__main__":
        import sys
        from fonction_design import *
        from fonction_saisi import *
        from scroll import *
        sys.path.append("..")
        from mail_local import *
        from icone_contacts import *
        fenetre = start()[0]
        fenetre.mainloop()