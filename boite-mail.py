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


# Création des fonctions du programme

# Fonction pour chaque bouton

def boite_de_reception():
    fenetre = Tk()
    fenetre.title("Boite de réception")
    fenetre.attributes("-fullscreen", True)  
    fenetre.iconbitmap("logo.ico")

    j = 0

    for i in range(3):
        Button(fenetre, text="Personne "+str(i+1+j), font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black").place(x=largeur_ecran*0.1, y=hauteur_ecran*(0.15 + 0.3*i), width=largeur_ecran*0.2, height=hauteur_ecran*0.2)
        Button(fenetre, text="Personne "+str(i+2+j), font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black").place(x=largeur_ecran*0.4, y=hauteur_ecran*(0.15 + 0.3*i), width=largeur_ecran*0.2, height=hauteur_ecran*0.2)
        Button(fenetre, text="Personne "+str(i+3+j), font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black").place(x=largeur_ecran*0.7, y=hauteur_ecran*(0.15 + 0.3*i), width=largeur_ecran*0.2, height=hauteur_ecran*0.2)
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