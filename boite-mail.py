from tkinter import *

fenetre = Tk()
fenetre.title("Boite Mail")
fenetre.attributes("-fullscreen", True)  # Active le mode plein écran
fenetre.iconbitmap("logo.ico")  # Vérifiez que "logo.ico" existe

# Quitter le plein écran avec Échap
fenetre.bind("<Escape>", lambda event: fenetre.attributes("-fullscreen", False))


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
chemin_image_profil = r"C:\Users\Maxime\Desktop\Cours\Informatique\Année 2\S2\Projet\boite-mail\profil.png"
photo_profil = PhotoImage(file=chemin_image_profil)

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
photo_profil.image = photo_profil


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

def envoyer_mail():
    import base64
    import smtplib
    from email.mime.text import MIMEText

    SCOPES = ['https://mail.google.com/']
    CREDENTIALS_FILE = 'token.pkl'

    # Fonction pour générer l'authentification OAuth2
    def generate_oauth2_string(username, access_token):
        auth_string = f"user={username}\1auth=Bearer {access_token}\1\1"
        return base64.b64encode(auth_string.encode("ascii")).decode("ascii")

    # Fonction pour envoyer un e-mail
    def send_email(subject, body, sender, recipients):
        creds = connexion()  # Récupérer les credentials
        access_token = creds.token  # Accéder au token d'accès

        # Générer la chaîne d'authentification
        auth_string = generate_oauth2_string(sender, access_token)

        # Créer le message
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)

        # Configuration du serveur SMTP
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()  # Démarrer la connexion TLS
            server.docmd('AUTH', "XOAUTH2 " + auth_string)  # Authentification via OAuth2
            server.sendmail(sender, recipients, msg.as_string())  # Envoyer le mail
            server.quit()  # Fermer la connexion
            print("E-mail envoyé avec succès !")
        except Exception as e:
            print(f"Une erreur est survenue : {e}")

    # Exécution du programme principal
    if __name__ == '__main__':
        # Définir les informations nécessaires
        sender = 'mailboite07@gmail.com'
        recipients = ['mailboite07@gmail.com']
        subject = ecriture_objet.get("1.0", "end-1c")
        body = ecriture_mail.get("1.0", "end-1c")

        # Envoyer l'e-mail 
        send_email(subject, body, sender, recipients)



def connexion():
    SCOPES = ['https://mail.google.com/']
    CREDENTIALS_FILE = 'token.pkl'

    import os
    import pickle
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    # Si un token existe déjà
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'rb') as token:
            creds = pickle.load(token)

    # Si les credentials sont invalides ou expirés
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=5000)

        # Sauvegarde des nouveaux credentials
        with open(CREDENTIALS_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds



# Définition des couleurs et styles
menu_bg = "lightblue"  # Fond du menu
menu_fg = "#23272A"  # Texte du menu
menu_hover = "#7289DA"  # Couleur de survol
font_style = ("Arial", 12, "bold")  # Police et taille du menu

def parametre(event=None):
    choix = Menu(fenetre, tearoff=0, bg=menu_bg, fg=menu_fg, font=font_style, activebackground=menu_hover, activeforeground="white", relief="raised", borderwidth=3)
    
    # Ajout des options avec des icônes (si tu en as)
    choix.add_command(label="👤 Connexion", command=connexion)
    choix.add_command(label="❓ Aide", command=lambda: print("Aide"))
    choix.add_separator()
    choix.add_command(label="❌ Quitter", command=fenetre.quit)
    
    # Position du menu sous le bouton
    if bouton_settings:
        choix.post(bouton_settings.winfo_rootx(), bouton_settings.winfo_rooty() + bouton_settings.winfo_height())



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

    my_scrollbar = Scrollbar(fenetre_boite, orient=VERTICAL)
    my_scrollbar.pack(side=RIGHT, fill=Y)



def ecrire_mail():
    global fenetre_ecriture
    global ecriture_mail
    global ecriture_objet

    # Création d'une nouvelle fenêtre (évite les conflits avec Tk)
    fenetre_ecriture = Toplevel(fenetre)
    fenetre_ecriture.title("Ecrire un mail")
    fenetre_ecriture.attributes("-fullscreen", True)
    fenetre_ecriture.iconbitmap("logo.ico")

    ecriture_mail = Text(fenetre_ecriture, bg="white", fg="black", font=("Courier", 14), bd=2)
    ecriture_mail.insert("1.0", "Ecrire un mail")  # Insère à la première ligne, colonne 0
    ecriture_mail.place(x=largeur_ecran*0.05, y=hauteur_ecran*0.6, width=largeur_ecran*0.8, height=hauteur_ecran*0.35)

    ecriture_objet = Text(fenetre_ecriture, bg="white", fg="black", font=("Courier", 14), bd=2)
    ecriture_objet.insert("1.0", "Ecrire un objet")  # Insère à la première ligne, colonne 0
    ecriture_objet.place(x=largeur_ecran*0.05, y=hauteur_ecran*0.55, width=largeur_ecran*0.8, height=hauteur_ecran*0.03)

    envoyer = Button(fenetre_ecriture, text="Envoyer", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", command=envoyer_mail)
    envoyer.place(x=largeur_ecran*0.875, y=hauteur_ecran*0.55, width=largeur_ecran*0.1, height=hauteur_ecran*0.4)
        
    # Lier l’événement du clic à la suppression du texte par défaut
    ecriture_mail.bind("<FocusIn>", lambda event: vider_saisi_text(event, ecriture_mail))
    ecriture_objet.bind("<FocusIn>", lambda event: vider_saisi_text(event, ecriture_objet))

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
    # Création d'une nouvelle fenêtre (évite les conflits avec Tk)
    fenetre_label = Toplevel(fenetre)
    fenetre_label.title("Ecrire un mail")
    fenetre_label.attributes("-fullscreen", True)
    fenetre_label.iconbitmap("logo.ico")

    bouton_home = Button(fenetre_label, image=photo_home, relief="flat", command=lambda: home("ecriture")).place(x=largeur_ecran*0.05, y=hauteur_ecran*0.05)
    bouton_exit = Button(fenetre_label, image=photo_exit, relief="flat", command=fenetre.quit).place(x=largeur_ecran*0.95, y=hauteur_ecran*0.05)

    bouton_creation_label = Button(fenetre_label, text="Création d'un nouvelle catégorie", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
    bouton_creation_label.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.05, width=largeur_ecran*0.6, height=hauteur_ecran*0.065)


def corbeille():
    pass



"""def menu():
    pass


menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=menu)
menu1.add_command(label="Editer", command=menu)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Couper", command=menu)
menu2.add_command(label="Copier", command=menu)
menu2.add_command(label="Coller", command=menu)
menubar.add_cascade(label="Editer", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="A propos", command=menu)
menubar.add_cascade(label="Aide", menu=menu3)

fenetre.config(menu=menubar)"""



# Création des 4 rectangles de menu


bouton_boite_de_reception = Button(fenetre, text="Boite de réception", image=photo_mail, font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20, command=boite_de_reception)
bouton_boite_de_reception.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.2, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


bouton_ecrire_mail = Button(fenetre, text="Ecrire un mail", image=photo_ecrire, font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20, command=ecrire_mail)
bouton_ecrire_mail.place(x=largeur_ecran*0.55, y=hauteur_ecran*0.2, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


bouton_label = Button(fenetre, text="Categories", image=photo_label, font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20, command=label)
bouton_label.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.6, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


bouton_corbeille = Button(fenetre, text="Corbeille", image=photo_poubelle, font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20)
bouton_corbeille.place(x=largeur_ecran*0.55, y=hauteur_ecran*0.6, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


bouton_settings = Button(fenetre, image=photo_profil, relief="flat", command=parametre)
bouton_settings.place(x=largeur_ecran*0.05, y=hauteur_ecran*0.05)

bouton_exit = Button(fenetre, image=photo_exit, relief="flat", command=fenetre.quit).place(x=largeur_ecran*0.95, y=hauteur_ecran*0.05)












fenetre.mainloop()