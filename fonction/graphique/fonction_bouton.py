from tkinter import *

def deconnexion():
    os.remove("private/token.pkl")
    shutil.rmtree("private/icones")
    os.remove("private/mail/mail.json")
    chemin_image_profil = r"img/profil.png"
    photo_profil = PhotoImage(file=chemin_image_profil)
    photo_profil.image = photo_profil
    page_accueil()


def parametre(fenetre, bouton_settings):
    choix = Menu(fenetre, tearoff=0, bg="lightblue", fg="#23272A", font=("Arial", 12, "bold"), activebackground="#7289DA", activeforeground="white", relief="raised", borderwidth=3)
    if connecter() :
        # Ajout des options avec des icônes (si tu en as)
        choix.add_command(label="👤 Deconnexion", command=deconnexion)

    elif not connecter() :
        choix.add_command(label="👤 Connexion", command=get_credentials)

    choix.add_command(label="⚙️ Paramètres", command=lambda: print("Paramètres"))
    choix.add_separator()
    choix.add_command(label="❌ Quitter", command=fenetre.quit)
    # Position du menu sous le bouton
    if bouton_settings:
        choix.post(bouton_settings.winfo_rootx(), bouton_settings.winfo_rooty() + bouton_settings.winfo_height())

try:
    from fonction.recevoir_information import *
except ModuleNotFoundError:
    import sys
    sys.path.append("..")
    from recevoir_information import *