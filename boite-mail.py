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


# Création des 4 rectangles de menu


bouton_boite_de_reception = Button(fenetre, text="Boite de réception", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
bouton_boite_de_reception.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.2, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


bouton_ecrire_mail = Button(fenetre, text="Ecrire un mail", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
bouton_ecrire_mail.place(x=largeur_ecran*0.55, y=hauteur_ecran*0.2, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


bouton_categories = Button(fenetre, text="Categories", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
bouton_categories.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.55, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


bouton_corbeille = Button(fenetre, text="Corbeille", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
bouton_corbeille.place(x=largeur_ecran*0.55, y=hauteur_ecran*0.55, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)








fenetre.mainloop()