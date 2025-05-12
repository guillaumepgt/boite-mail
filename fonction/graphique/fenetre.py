from tkinter import *
import platform

def start():
    win = create_fullscreen("Boite Mail")
    return win, win.winfo_screenwidth(), win.winfo_screenheight()

def discussion(fenetre, adresse_mail, page, images, largeur_ecran, hauteur_ecran):
    fenetre_discussion = create_fullscreen("Discuter", fenetre)
    add_nav_buttons(fenetre_discussion, images, largeur_ecran, hauteur_ecran, fenetre.quit)

    canvas = create_canvas_with_scrollbar(fenetre_discussion, largeur_ecran, hauteur_ecran)
    bind_scroll_events(canvas)

    mails = lire_mail({"boite_principal": "mail", "envoye": "envoye_list", "corbeille": "corbeille_list"}[page])
    field = {"boite_principal": "Expediteur", "envoye": "Destinataire", "corbeille": "Expediteur"}[page]
    liste_mails = [m for m in reversed(mails) if m[field] == adresse_mail]

    font, bulle_width, bulle_bords = ("Courier", 14), largeur_ecran * 0.6, 20
    total_height = sum(get_text_height(canvas, m["Sujet"] + "\n" + m["Contenu"], font, bulle_width) + 3 * bulle_bords + 30 for m in liste_mails)
    y_offset = max(20, hauteur_ecran * 0.8 - total_height)

    for mail in liste_mails:
        y_offset = afficher_message(canvas, mail["Expediteur"], mail["Destinataire"], mail["Sujet"], mail["Contenu"], y_offset, largeur_ecran, hauteur_ecran)

    canvas.configure(scrollregion=(0, 0, largeur_ecran * 0.8, y_offset))
    canvas.yview_moveto(1.0)


def reception(fenetre, images, largeur_ecran, hauteur_ecran, page, type, canvas=None, ecriture_objet=None, ecriture_mail=None):
    if page == 1 :
        # Création d'une nouvelle fenêtre
        fenetre_boite = create_fullscreen("Discuter", fenetre)

        # Canvas pour permettre le scroll
        canvas = Canvas(fenetre_boite)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        recherche_mail = Entry(fenetre_boite, bg="white", fg="black", font="Courier", bd=2, justify=LEFT)
        recherche_mail.insert(0, "Recherche des mails")
        recherche_mail.place(x=largeur_ecran * 0.1, y=hauteur_ecran * 0.055,width=largeur_ecran * 0.3, height=hauteur_ecran * 0.05)

        recherche_mail.bind("<FocusIn>", lambda event: vider_saisi_entry(event, recherche_mail))
        add_nav_buttons(fenetre_boite, images, largeur_ecran, hauteur_ecran, fenetre_boite.quit)

        # Scrollbar liée au Canvas
        my_scrollbar = Scrollbar(fenetre_boite, orient=VERTICAL, command=canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=my_scrollbar.set)

    elif page == 2:
        canvas.delete("all")  # vide le contenu précédent du canvas
        canvas.yview_moveto(0) # remettre le canvas en haut

        # Frame dans le canvas pour contenir tous les boutons
    frame_boite = Frame(canvas)
    frame_boite.bind("<Configure>",lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    # Créer une fenêtre dans le canvas
    canvas_frame = canvas.create_window((0, 0), window=frame_boite, anchor="nw")

    contact = lire_mail({"boite_de_reception" : "full_name_list", "corbeille": "full_name_list_corbeille", "envoye_mail": "envoye_name_list", "ecrire_mail_brouillon" : "brouillon_list"}[type])
    compteur = 0

    frame_boite.config(width=largeur_ecran, height=hauteur_ecran*3)
    if type == "ecrire_mail_brouillon":
        for brouillon in contact:
            sujet = brouillon["Sujet"]
            apercu_sujet = sujet[:10] + "..." if len(sujet) > 10 else sujet
            contenu = brouillon["Contenu"]
            apercu_contenu = contenu[:10] + "..." if len(contenu) > 10 else contenu
            Button(frame_boite, text=f"\n{apercu_sujet}\n\n{apercu_contenu}", font=("Arial", 20), bg="lightblue", fg="black",
                   relief="flat", activebackground="white", activeforeground="black", command=lambda b=brouillon: modifier_brouillon(b, ecriture_objet, ecriture_mail)).place(
                x=largeur_ecran * [0.05, 0.35, 0.65][compteur % 3],
                y=hauteur_ecran * (0.3 * (compteur // 3)),
                width=largeur_ecran * 0.2,
                height=hauteur_ecran * 0.2)
            compteur += 1
    else:
        for i in range(len(contact)):
            use = 0
            for j in range(i):
                if contact[i]["Nom"] == contact[j]["Nom"]:
                    use = 1
            if use == 0:
                if contact[i]["Email"] not in images["cache_image"] :
                    images["cache_image"] = enregistrer_icone_tkinter(contact)
                icone = images["cache_image"][contact[i]["Email"]]
                Button(frame_boite, compound="top", text=contact[i]["Nom"], image=icone, font=("Arial", 20),bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black",command=lambda email=contact[i]["Email"]: discussion(fenetre, email, {"boite_de_reception" : "boite_principal", "corbeille": "corbeille", "envoye_mail": "envoye"}[type], images, largeur_ecran, hauteur_ecran)).place(
                    x=largeur_ecran * [[0.1, 0.4, 0.7][compteur % 3], [0.05, 0.35, 0.65][compteur % 3]][page-1],
                    y=hauteur_ecran * [(0.15 + 0.3 * (compteur // 3)), (0.3 * (compteur // 3))][page-1],
                    width=largeur_ecran * 0.2,
                    height=hauteur_ecran * 0.2
                )
                compteur += 1

    bind_scroll_events(canvas)



def ecrire_mail(fenetre, images, largeur_ecran, hauteur_ecran):
    global fenetre_ecriture, ecriture_mail, ecriture_objet, canvas, brouillon

    # Création d'une nouvelle fenêtre (évite les conflits avec Tk)
    fenetre_ecriture = Toplevel(fenetre)
    fenetre_ecriture.title("Ecrire un mail")
    fenetre_ecriture.attributes("-fullscreen", True)

    canvas = Canvas(fenetre_ecriture)
    canvas.place(x=largeur_ecran*0.05, y=hauteur_ecran*0.2, width=largeur_ecran*0.926, height=hauteur_ecran*0.3)

    # Scrollbar liée au Canvas
    my_scrollbar = Scrollbar(fenetre_ecriture, orient=VERTICAL, command=canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=my_scrollbar.set)

    bind_scroll_events(canvas)



    ecriture_mail = Text(fenetre_ecriture, bg="white", fg="black", font=("Courier", 14), bd=2)
    ecriture_mail.insert("1.0", "Ecrire un mail")  # Insère à la première ligne, colonne 0
    ecriture_mail.place(x=largeur_ecran*0.05, y=hauteur_ecran*0.65, width=largeur_ecran*0.8, height=hauteur_ecran*0.3)

    ecriture_objet = Text(fenetre_ecriture, bg="white", fg="black", font=("Courier", 14), bd=2)
    ecriture_objet.insert("1.0", "Ecrire un objet")  # Insère à la première ligne, colonne 0
    ecriture_objet.place(x=largeur_ecran*0.05, y=hauteur_ecran*0.6, width=largeur_ecran*0.8, height=hauteur_ecran*0.03)

    ecriture_adresse = Text(fenetre_ecriture, bg="white", fg="black", font=("Courier", 14), bd=2)
    ecriture_adresse.insert("1.0", "Ecrire une adresse mail")  # Insère à la première ligne, colonne 0
    ecriture_adresse.place(x=largeur_ecran*0.05, y=hauteur_ecran*0.55, width=largeur_ecran*0.8, height=hauteur_ecran*0.03)

    envoyer = Button(fenetre_ecriture, text="Envoyer", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", command=lambda: envoyer_email(ecriture_objet.get("1.0","end-1c"),ecriture_mail.get("1.0","end-1c"), get_user_info()["email"], [ecriture_adresse.get("1.0","end-1c")]))
    envoyer.place(x=largeur_ecran*0.875, y=hauteur_ecran*0.55, width=largeur_ecran*0.1, height=hauteur_ecran*0.4)

    # Lier l’événement du clic à la suppression du texte par défaut
    ecriture_mail.bind("<FocusIn>", lambda event: vider_saisi_text(event, ecriture_mail))
    ecriture_objet.bind("<FocusIn>", lambda event: vider_saisi_text(event, ecriture_objet))
    ecriture_adresse.bind("<FocusIn>", lambda event: vider_saisi_text(event, ecriture_adresse))

    Label(fenetre_ecriture, image=images["line"], relief="flat").place(x=largeur_ecran*0.05, y=hauteur_ecran*0.03, width=largeur_ecran*0.1, height=hauteur_ecran*0.1)
    Button(fenetre_ecriture, image=images["home"], relief="flat", command=lambda: fenetre_ecriture.destroy()).place(x=largeur_ecran*0.05, y=hauteur_ecran*0.05)
    Button(fenetre_ecriture, image=images["exit"], relief="flat", command=fenetre.quit).place(x=largeur_ecran * 0.95,y=hauteur_ecran * 0.05)

    bouton_boite_de_reception = Button(fenetre_ecriture, text="Boite de réception", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", command=lambda: reception(fenetre, images, largeur_ecran, hauteur_ecran, 2, "boite_de_reception", canvas))
    bouton_boite_de_reception.place(x=largeur_ecran*0.12, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)

    bouton_brouillon = Button(fenetre_ecriture, text="Brouillon", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", command =lambda: reception(fenetre, images, largeur_ecran, hauteur_ecran, 2, "ecrire_mail_brouillon", canvas, ecriture_objet, ecriture_mail))
    bouton_brouillon.place(x=largeur_ecran*0.32, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)

    bouton_mails_envoyes = Button(fenetre_ecriture, text="Mails envoyés", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", command= lambda: reception(fenetre, images, largeur_ecran, hauteur_ecran, 2, "envoye_mail", canvas))
    bouton_mails_envoyes.place(x=largeur_ecran*0.52, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)

    bouton_corbeille = Button(fenetre_ecriture, text="Corbeille", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", command=lambda: reception(fenetre, images, largeur_ecran, hauteur_ecran, 2, "corbeille", canvas))
    bouton_corbeille.place(x=largeur_ecran*0.72, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)

def label(fenetre, images, largeur_ecran, hauteur_ecran):
    # Création d'une nouvelle fenêtre (évite les conflits avec Tk)
    fenetre_label = Toplevel(fenetre)
    fenetre_label.title("Ecrire un mail")
    fenetre_label.attributes("-fullscreen", True)

    add_nav_buttons(fenetre_label, images, largeur_ecran, hauteur_ecran, fenetre.quit, fenetre_label.destroy)

    bouton_creation_label = Button(fenetre_label, text="Création d'une nouvelle catégorie", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
    bouton_creation_label.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.05, width=largeur_ecran*0.6, height=hauteur_ecran*0.065)

def page_accueil(fenetre, images, largeur_ecran, hauteur_ecran):
    creer_bouton(fenetre, images, largeur_ecran, hauteur_ecran, 0.2, 0.2, "mail", "Boite de réception", lambda: reception(fenetre, images, largeur_ecran, hauteur_ecran, 1, "boite_de_reception"))
    creer_bouton(fenetre, images, largeur_ecran, hauteur_ecran, 0.55, 0.2, "ecrire", "Ecrire un mail", lambda: ecrire_mail(fenetre, images, largeur_ecran, hauteur_ecran))
    creer_bouton(fenetre, images, largeur_ecran, hauteur_ecran, 0.2, 0.6, "label", "Categories", lambda: label(fenetre, images, largeur_ecran, hauteur_ecran))
    creer_bouton(fenetre, images, largeur_ecran, hauteur_ecran, 0.55, 0.6, "poubelle", "Corbeille", lambda: reception(fenetre, images, largeur_ecran, hauteur_ecran, 1, "corbeille"))

    bouton_settings = Button(fenetre, image=images["profil"], relief="flat", command=lambda: parametre(fenetre, bouton_settings))
    bouton_settings.place(x=largeur_ecran*0.05, y=hauteur_ecran*0.05)
    Button(fenetre, image=images["exit"], relief="flat", command=fenetre.quit).place(x=largeur_ecran*0.95, y=hauteur_ecran*0.05)


def create_fullscreen(title, root=None):
    win = Toplevel(root) if root else Tk()
    win.title(title)
    win.attributes("-fullscreen", True)
    win.bind("<Escape>", lambda e: win.attributes("-fullscreen", False))
    return win


try:
    from fonction.mail_local import *
    from fonction.graphique.fonction_design import *
    from fonction.graphique.fonction_saisi import *
    from fonction.icone_contacts import *
    from fonction.graphique.fonction_bouton import *
except ModuleNotFoundError:
    if __name__ == "__main__":
        import sys
        from fonction_design import *
        from fonction_saisi import *
        from fonction_bouton import *
        sys.path.append("..")
        from mail_local import *
        from icone_contacts import *
        fenetre = start()[0]
        fenetre.mainloop()