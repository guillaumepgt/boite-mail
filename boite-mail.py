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

# Charger l'image (uniquement PNG ou GIF)
chemin_image_mail = r"C:\Users\Maxime\Desktop\Cours\Informatique\Année 2\S2\Projet\boite-mail\mail.png"
photo = PhotoImage(file=chemin_image_mail)

# Empêcher la suppression de l’image
photo.image = photo

# Création des fonctions du programme

# Fonction pour chaque bouton

def boite_de_reception():

    # Création d'une nouvelle fenêtre (évite les conflits avec Tk)
    fenetre_boite = Toplevel(fenetre)
    fenetre_boite.title("Boite de réception")
    fenetre_boite.attributes("-fullscreen", True)
    fenetre_boite.iconbitmap("logo.ico")

    # Affichage du logo
    label_logo = Label(fenetre_boite, image=photo)
    label_logo.place(x=largeur_ecran * 0.05, y=hauteur_ecran * 0.05, width=largeur_ecran * 0.2, height=hauteur_ecran * 0.2)
    label_logo.image = photo

    j = 0

    for i in range(3):
        Button(fenetre_boite, text="Personne "+str(i+1+j), font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black").place(x=largeur_ecran*0.1, y=hauteur_ecran*(0.15 + 0.3*i), width=largeur_ecran*0.2, height=hauteur_ecran*0.2)
        Button(fenetre_boite, text="Personne "+str(i+2+j), font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black").place(x=largeur_ecran*0.4, y=hauteur_ecran*(0.15 + 0.3*i), width=largeur_ecran*0.2, height=hauteur_ecran*0.2)
        Button(fenetre_boite, text="Personne "+str(i+3+j), font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black").place(x=largeur_ecran*0.7, y=hauteur_ecran*(0.15 + 0.3*i), width=largeur_ecran*0.2, height=hauteur_ecran*0.2)
        j += 1







def ecrire_mail():
    pass


def categories():
    pass


def corbeille():
    pass



# Création des 4 rectangles de menu


bouton_boite_de_reception = Button(fenetre, text="Boite de réception", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", command=boite_de_reception)
bouton_boite_de_reception.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.2, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


bouton_ecrire_mail = Button(fenetre, text="Ecrire un mail", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
bouton_ecrire_mail.place(x=largeur_ecran*0.55, y=hauteur_ecran*0.2, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


bouton_categories = Button(fenetre, text="Categories", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
bouton_categories.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.6, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


bouton_corbeille = Button(fenetre, text="Corbeille", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
bouton_corbeille.place(x=largeur_ecran*0.55, y=hauteur_ecran*0.6, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)










fenetre.mainloop()