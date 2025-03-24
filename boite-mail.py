from tkinter import *

fenetre = Tk()
fenetre.title("Boite Mail")
fenetre.attributes("-fullscreen", True)  # Active le mode plein écran
fenetre.iconbitmap("logo.ico")  # Vérifiez que "logo.ico" existe

"""# Quitter le plein écran avec Échap
fenetre.bind("<Escape>", lambda event: fenetre.attributes("-fullscreen", False))"""


# Récupération des dimensions de l'écran
largeur_ecran = fenetre.winfo_screenwidth()
hauteur_ecran = fenetre.winfo_screenheight()


# Charger les images pour la fenêtre principale
chemin_image_mail = r"C:\Users\Maxime\Desktop\Cours\Informatique\Année 2\S2\Projet\boite-mail\mail.png"
photo_mail = PhotoImage(file=chemin_image_mail)
chemin_image_ecrire = r"C:\Users\Maxime\Desktop\Cours\Informatique\Année 2\S2\Projet\boite-mail\ecrire.png"
photo_ecrire = PhotoImage(file=chemin_image_ecrire)
chemin_image_label = r"C:\Users\Maxime\Desktop\Cours\Informatique\Année 2\S2\Projet\boite-mail\label.png"
photo_label = PhotoImage(file=chemin_image_label)
chemin_image_poubelle = r"C:\Users\Maxime\Desktop\Cours\Informatique\Année 2\S2\Projet\boite-mail\poubelle.png"
photo_poubelle = PhotoImage(file=chemin_image_poubelle)
chemin_image_settings = r"C:\Users\Maxime\Desktop\Cours\Informatique\Année 2\S2\Projet\boite-mail\settings.png"
photo_settings = PhotoImage(file=chemin_image_settings)

# Charger les images pour les différentes fenêtres
chemin_image_home = r"C:\Users\Maxime\Desktop\Cours\Informatique\Année 2\S2\Projet\boite-mail\home.png"
photo_home = PhotoImage(file=chemin_image_home)
chemin_image_exit = r"C:\Users\Maxime\Desktop\Cours\Informatique\Année 2\S2\Projet\boite-mail\exit.png"
photo_exit = PhotoImage(file=chemin_image_exit)
chemin_image_line = r"C:\Users\Maxime\Desktop\Cours\Informatique\Année 2\S2\Projet\boite-mail\line.png"
photo_line = PhotoImage(file=chemin_image_line)




# Empêcher la suppression des images
photo_mail.image = photo_mail
photo_ecrire.image = photo_ecrire
photo_label.image = photo_label
photo_poubelle.image = photo_poubelle
photo_home.image = photo_home
photo_exit.image = photo_exit
photo_settings.image = photo_settings
photo_line.image = photo_line


# Création des fonctions du programme

def vider_saisi_entry(event, entry):
    if entry.get() == "Recherche des mails":
        entry.delete(0, END)

def vider_saisi_text(event, widget):
    widget.delete("1.0", END)


def home(fenetres):
    if fenetres == "boite" and "fenetre_boite" in globals():
        fenetre_boite.destroy()
    elif fenetres == "ecriture" and "fenetre_ecriture" in globals():
        fenetre_ecriture.destroy()




# Fonction pour chaque bouton

def boite_de_reception():
    global fenetre_boite
    # Création d'une nouvelle fenêtre (évite les conflits avec Tk)
    fenetre_boite = Toplevel(fenetre)
    fenetre_boite.title("Boite de réception")
    fenetre_boite.attributes("-fullscreen", True)
    fenetre_boite.iconbitmap("logo.ico")

    j = 0

    for i in range(3):
        Button(fenetre_boite, text="Personne "+str(i+1+j), font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black").place(x=largeur_ecran*0.1, y=hauteur_ecran*(0.15 + 0.3*i), width=largeur_ecran*0.2, height=hauteur_ecran*0.2)
        Button(fenetre_boite, text="Personne "+str(i+2+j), font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black").place(x=largeur_ecran*0.4, y=hauteur_ecran*(0.15 + 0.3*i), width=largeur_ecran*0.2, height=hauteur_ecran*0.2)
        Button(fenetre_boite, text="Personne "+str(i+3+j), font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black").place(x=largeur_ecran*0.7, y=hauteur_ecran*(0.15 + 0.3*i), width=largeur_ecran*0.2, height=hauteur_ecran*0.2)
        j += 1


    recherche_mail = Entry(fenetre_boite, bg="white", fg="black", font="Courier", bd=2, justify=LEFT)
    recherche_mail.insert(0, "Recherche des mails")
    recherche_mail.place(x=largeur_ecran*0.1, y=hauteur_ecran*0.055, width=largeur_ecran*0.3, height=hauteur_ecran*0.05)

    # Lier l’événement du clic à la suppression du texte par défaut
    recherche_mail.bind("<FocusIn>", lambda event: vider_saisi_entry(event, recherche_mail))

    bouton_home = Button(fenetre_boite, image=photo_home, relief="flat", command=lambda: home("boite")).place(x=largeur_ecran*0.05, y=hauteur_ecran*0.05)
    bouton_exit = Button(fenetre_boite, image=photo_exit, relief="flat", command=fenetre.quit).place(x=largeur_ecran*0.95, y=hauteur_ecran*0.05)





def ecrire_mail():
    global fenetre_ecriture
    global ecriture_mail

    # Création d'une nouvelle fenêtre (évite les conflits avec Tk)
    fenetre_ecriture = Toplevel(fenetre)
    fenetre_ecriture.title("Ecrire un mail")
    fenetre_ecriture.attributes("-fullscreen", True)
    fenetre_ecriture.iconbitmap("logo.ico")

    ecriture_mail = Text(fenetre_ecriture, bg="white", fg="black", font=("Courier", 14), bd=2)
    ecriture_mail.insert("1.0", "Ecrire un mail")  # Insère à la première ligne, colonne 0
    ecriture_mail.place(x=largeur_ecran*0.1, y=hauteur_ecran*0.55, width=largeur_ecran*0.8, height=hauteur_ecran*0.4)
        
    # Lier l’événement du clic à la suppression du texte par défaut
    ecriture_mail.bind("<FocusIn>", lambda event: vider_saisi_text(event, ecriture_mail))

    Label(fenetre_ecriture, image=photo_line, relief="flat").place(x=largeur_ecran*0.05, y=hauteur_ecran*0.03, width=largeur_ecran*0.1, height=hauteur_ecran*0.1)
    bouton_home = Button(fenetre_ecriture, image=photo_home, relief="flat", command=lambda: home("ecriture")).place(x=largeur_ecran*0.05, y=hauteur_ecran*0.05)
    bouton_exit = Button(fenetre_ecriture, image=photo_exit, relief="flat", command=fenetre.quit).place(x=largeur_ecran*0.95, y=hauteur_ecran*0.05)

    bouton_boite_de_reception = Button(fenetre_ecriture, text="Boite de réception", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
    bouton_boite_de_reception.place(x=largeur_ecran*0.12, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)

    bouton_brouillon = Button(fenetre_ecriture, text="Brouillon", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
    bouton_brouillon.place(x=largeur_ecran*0.32, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)

    bouton_mails_envoyés = Button(fenetre_ecriture, text="Mails envoyés", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
    bouton_mails_envoyés.place(x=largeur_ecran*0.52, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)

    bouton_corbeille = Button(fenetre_ecriture, text="Corbeille", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
    bouton_corbeille.place(x=largeur_ecran*0.72, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)



def label():
    pass


def corbeille():
    pass







# Création des 4 rectangles de menu


bouton_boite_de_reception = Button(fenetre, text="Boite de réception", image=photo_mail, font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20, command=boite_de_reception)
bouton_boite_de_reception.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.2, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


bouton_ecrire_mail = Button(fenetre, text="Ecrire un mail", image=photo_ecrire, font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20, command=ecrire_mail)
bouton_ecrire_mail.place(x=largeur_ecran*0.55, y=hauteur_ecran*0.2, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


bouton_label = Button(fenetre, text="Categories", image=photo_label, font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20)
bouton_label.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.6, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


bouton_corbeille = Button(fenetre, text="Corbeille", image=photo_poubelle, font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20)
bouton_corbeille.place(x=largeur_ecran*0.55, y=hauteur_ecran*0.6, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


bouton_settings = Button(fenetre, image=photo_settings, relief="flat").place(x=largeur_ecran*0.95, y=hauteur_ecran*0.05)












fenetre.mainloop()