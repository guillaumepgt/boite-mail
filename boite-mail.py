import time
from tkinter import *
import asyncio
import shutil
from fonction.envoyer_mail import *
from fonction.recevoir_mail import *
from fonction.recevoir_information import *
from fonction.contact import *
from fonction.icone_contacts import *
from fonction.mail_local import *

fenetre = Tk()
fenetre.title("Boite Mail")
fenetre.attributes("-fullscreen", True)  # Active le mode plein écran

# Quitter le plein écran avec Échap
fenetre.bind("<Escape>", lambda event: fenetre.attributes("-fullscreen", False))

largeur_ecran = fenetre.winfo_screenwidth()
hauteur_ecran = fenetre.winfo_screenheight()


# Charger les images pour la fenêtre principale
chemin_image_mail = r"img/mail.png"
photo_mail = PhotoImage(file=chemin_image_mail)
chemin_image_ecrire = r"img/ecrire.png"
photo_ecrire = PhotoImage(file=chemin_image_ecrire)
chemin_image_label = r"img/label.png"
photo_label = PhotoImage(file=chemin_image_label)
chemin_image_poubelle = r"img/poubelle.png"
photo_poubelle = PhotoImage(file=chemin_image_poubelle)
chemin_image_settings = r"img/settings.png"
photo_settings = PhotoImage(file=chemin_image_settings)
chemin_image_profil = r"img/profil.png"
if connecter():
    threading.Thread(target=start_async_loop, daemon=True).start()
    chemin_image_profil = download_profil_img(get_user_info()["picture"])
else:
    chemin_image_profil = r"img/profil.png"

photo_profil = PhotoImage(file=chemin_image_profil)
# Charger les images pour les différentes fenêtres
chemin_image_home = r"img/home.png"
photo_home = PhotoImage(file=chemin_image_home)
chemin_image_exit = r"img/exit.png"
photo_exit = PhotoImage(file=chemin_image_exit)
chemin_image_line = r"img/line.png"
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
cache_images = {}

# Création des fonctions du programme

def vider_saisi_entry(event, entry):
    if entry.get() == "Recherche des mails":
        entry.delete(0, END)

def vider_saisi_text(event, widget):
    widget.delete("1.0", END)


def home(fenetres):
    if fenetres == "boite" and "fenetre_boite" in globals():
        fenetre_boite.destroy()
    elif fenetres == "discussion" and "fenetre_discussion" in globals():
        fenetre_discussion.destroy()
    elif fenetres == "ecriture" and "fenetre_ecriture" in globals():
        fenetre_ecriture.destroy()
    elif fenetres == "label" and "fenetre_label" in globals():
        fenetre_label.destroy()


def rectangle_arrondi(canvas, x1, y1, x2, y2, radius, **kwargs):
    # Dessiner un rectangle avec des coins arrondis en utilisant des arcs de cercle
    return canvas.create_polygon(
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        fill=kwargs.get('fill', 'white'),
        outline=kwargs.get('outline', 'black'),
        width=kwargs.get('width', 1),
        smooth=True
    )

# Fonction pour ajuster la hauteur de la bulle en fonction du texte
def get_text_height(canvas, text, font, width):
    # Créer un texte temporaire pour mesurer la hauteur
    text_id = canvas.create_text(0, 0, text=text, font=font, width=width)
    bbox = canvas.bbox(text_id)  # Récupérer la bounding box du texte
    height = bbox[3] - bbox[1]  # Calculer la hauteur
    canvas.delete(text_id)  # Supprimer le texte temporaire
    return height


def discussion(adresse_mail):
    global fenetre_discussion
    # Création d'une nouvelle fenêtre (évite les conflits avec Tk)
    fenetre_discussion = Toplevel(fenetre)
    fenetre_discussion.title("Discuter")
    fenetre_discussion.attributes("-fullscreen", True)

    bouton_home = Button(fenetre_discussion, image=photo_home, relief="flat", command=lambda: home("discussion")).place(x=largeur_ecran*0.05, y=hauteur_ecran*0.05)
    bouton_exit = Button(fenetre_discussion, image=photo_exit, relief="flat", command=fenetre.quit).place(x=largeur_ecran*0.95, y=hauteur_ecran*0.05)

    canvas = Canvas(fenetre_discussion, bg="white", bd=1)
    canvas.place(x=largeur_ecran * 0.1, y=hauteur_ecran * 0.1, width=largeur_ecran * 0.8, height=hauteur_ecran * 0.8)

    # Scrollbar liée au Canvas
    my_scrollbar = Scrollbar(fenetre_discussion, orient=VERTICAL, command=canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=my_scrollbar.set)

    y_offset_total = 20  # point de départ des messages

    mails = lire_mail("mail")
    liste_mails = []
    for i in range(len(mails)):
        if mails[i]["Expéditeur"] == adresse_mail :
            personne = mails[i]
            liste_mails.append(personne)
    for mail in liste_mails:
        expéditeur = mail["Expéditeur"]
        destinataire = mail["Destinataire"]
        sujet = mail["Sujet"]
        contenu = mail["Contenu"]

        # Appeler la fonction pour afficher le message
        y_offset_total = afficher_message(canvas, expéditeur, destinataire, sujet, contenu, y_offset_total)

<<<<<<< HEAD
    canvas.configure(scrollregion=(0, 0, largeur_ecran * 0.8, y_offset_total))
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
=======
    import platform
>>>>>>> 0c76a39b94e91c301a23f2b9dfe424eac3f2f8f9


    def _on_mousewheel(event):
        if platform.system() == 'Windows':
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == 'Darwin':  # macOS
            canvas.yview_scroll(int(-1 * (event.delta)), "units")
        else:  # Linux
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

        # Bind selon la plateforme
    if platform.system() in ['Windows', 'Darwin']:
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    else:  # Linux
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)


def afficher_message(canvas, expéditeur, destinataire, sujet, contenu, y_offset):
    align = "e" if expéditeur == destinataire else "w"

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

# Définition des couleurs et styles
menu_bg = "lightblue"  # Fond du menu
menu_fg = "#23272A"  # Texte du menu
menu_hover = "#7289DA"  # Couleur de survol
font_style = ("Arial", 12, "bold")  # Police et taille du menu

def deconnexion():
    os.remove("private/token.pkl")
    shutil.rmtree("private/icones")
    os.remove("private/mail/mail.json")
    chemin_image_profil = r"img/profil.png"
    photo_profil = PhotoImage(file=chemin_image_profil)
    photo_profil.image = photo_profil
    page_accueil()

def parametre(event=None):
    choix = Menu(fenetre, tearoff=0, bg=menu_bg, fg=menu_fg, font=font_style, activebackground=menu_hover, activeforeground="white", relief="raised", borderwidth=3)
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


def boite_de_reception(page):
    global fenetre_boite, cache_images
    threading.Thread(target=start_async_loop, daemon=True).start()
    if page == 1 :
        # Création d'une nouvelle fenêtre
        fenetre_boite = Toplevel(fenetre)
        fenetre_boite.title("Boite de réception")
        fenetre_boite.attributes("-fullscreen", True)

        # Canvas pour permettre le scroll
        canvas = Canvas(fenetre_boite)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Scrollbar liée au Canvas
        my_scrollbar = Scrollbar(fenetre_boite, orient=VERTICAL, command=canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=my_scrollbar.set)

        # Frame dans le canvas pour contenir tous les boutons
        frame_boite = Frame(canvas)
        frame_boite.bind("<Configure>",lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

        # Créer une fenêtre dans le canvas
        canvas_frame = canvas.create_window((0, 0), window=frame_boite, anchor="nw")

        contact = lire_mail("full_name_list")
        compteur = 0

        frame_boite.config(width=largeur_ecran, height=hauteur_ecran*3)
        for i in range(len(contact)):
            use = 0
            for j in range(i):
                if contact[i]["Nom"] == contact[j]["Nom"]:
                    use = 1
            if use == 0:
                if contact[i]["Email"] not in cache_images :
                    cache_images = enregistrer_icone_tkinter(contact)
                icone = cache_images[contact[i]["Email"]]
                Button(frame_boite, compound="top", text=contact[i]["Nom"], image=icone, font=("Arial", 20),bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black",command=lambda email=contact[i]["Email"]: discussion(email)).place(
                    x=largeur_ecran * [0.1, 0.4, 0.7][compteur % 3],
                    y=hauteur_ecran * (0.15 + 0.3 * (compteur // 3)),
                    width=largeur_ecran * 0.2,
                    height=hauteur_ecran * 0.2
                )
                compteur += 1

        recherche_mail = Entry(fenetre_boite, bg="white", fg="black", font="Courier", bd=2, justify=LEFT)
        recherche_mail.insert(0, "Recherche des mails")
        recherche_mail.place(x=largeur_ecran * 0.1, y=hauteur_ecran * 0.055,width=largeur_ecran * 0.3, height=hauteur_ecran * 0.05)

        recherche_mail.bind("<FocusIn>", lambda event: vider_saisi_entry(event, recherche_mail))

        bouton_home = Button(fenetre_boite, image=photo_home, relief="flat", command=lambda: home("boite"))
        bouton_home.place(x=largeur_ecran * 0.05, y=hauteur_ecran * 0.05)

        bouton_exit = Button(fenetre_boite, image=photo_exit, relief="flat", command=fenetre.quit)
        bouton_exit.place(x=largeur_ecran * 0.95, y=hauteur_ecran * 0.05)

        import platform

        def _on_mousewheel(event):
            if platform.system() == 'Windows':
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif platform.system() == 'Darwin':  # macOS
                canvas.yview_scroll(int(-1 * (event.delta)), "units")
            else:  # Linux
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")

        # Bind selon la plateforme
        if platform.system() in ['Windows', 'Darwin']:
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        else:  # Linux
            canvas.bind_all("<Button-4>", _on_mousewheel)
            canvas.bind_all("<Button-5>", _on_mousewheel)


    elif page == 2 :
        # Canvas pour permettre le scroll
        canvas = Canvas(fenetre_ecriture)
        canvas.place(x=largeur_ecran*0.05, y=hauteur_ecran*0.2, width=largeur_ecran*0.926, height=hauteur_ecran*0.3)

        # Scrollbar liée au Canvas
        my_scrollbar = Scrollbar(fenetre_ecriture, orient=VERTICAL, command=canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=my_scrollbar.set)

        # Frame dans le canvas pour contenir tous les boutons
        frame_boite = Frame(canvas)
        frame_boite.bind("<Configure>",lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

        # Créer une fenêtre dans le canvas
        canvas_frame = canvas.create_window((0, 0), window=frame_boite, anchor="nw")

        contact = lire_mail("full_name_list")
        compteur = 0

        frame_boite.config(width=largeur_ecran, height=hauteur_ecran*3)

        for i in range(len(contact)):
            use = 0
            for j in range(i):
                if contact[i]["Nom"] == contact[j]["Nom"]:
                    use = 1
            if use == 0:
                if contact[i]["Email"] not in cache_images :
                    cache_images = enregistrer_icone_tkinter(contact)
                icone = cache_images[contact[i]["Email"]]
                Button(frame_boite, compound="top", text=contact[i]["Nom"], image=icone, font=("Arial", 20),bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black",command=lambda email=contact[i]["Email"]: discussion(email)).place(
                    x=largeur_ecran * [0.05, 0.35, 0.65][compteur % 3],
                    y=hauteur_ecran * (0.3 * (compteur // 3)),
                    width=largeur_ecran * 0.2,
                    height=hauteur_ecran * 0.2
                )
                compteur += 1

        def _on_mousewheel(event):
            if platform.system() == 'Windows':
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif platform.system() == 'Darwin':  # macOS
                canvas.yview_scroll(int(-1 * (event.delta)), "units")
            else:  # Linux
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")

        # Bind selon la plateforme
        if platform.system() in ['Windows', 'Darwin']:
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        else:  # Linux
            canvas.bind_all("<Button-4>", _on_mousewheel)
            canvas.bind_all("<Button-5>", _on_mousewheel)




def ecrire_mail():
    global fenetre_ecriture
    global ecriture_mail
    global ecriture_objet

    # Création d'une nouvelle fenêtre (évite les conflits avec Tk)
    fenetre_ecriture = Toplevel(fenetre)
    fenetre_ecriture.title("Ecrire un mail")
    fenetre_ecriture.attributes("-fullscreen", True)

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

    Label(fenetre_ecriture, image=photo_line, relief="flat").place(x=largeur_ecran*0.05, y=hauteur_ecran*0.03, width=largeur_ecran*0.1, height=hauteur_ecran*0.1)
    bouton_home = Button(fenetre_ecriture, image=photo_home, relief="flat", command=lambda: home("ecriture")).place(x=largeur_ecran*0.05, y=hauteur_ecran*0.05)
    bouton_exit = Button(fenetre_ecriture, image=photo_exit, relief="flat", command=fenetre.quit).place(x=largeur_ecran*0.95, y=hauteur_ecran*0.05)

    bouton_boite_de_reception = Button(fenetre_ecriture, text="Boite de réception", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", command=lambda: boite_de_reception(2))
    bouton_boite_de_reception.place(x=largeur_ecran*0.12, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)

    bouton_brouillon = Button(fenetre_ecriture, text="Brouillon", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", command =lambda: ecrire_mail_brouillon())
    bouton_brouillon.place(x=largeur_ecran*0.32, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)

    bouton_mails_envoyés = Button(fenetre_ecriture, text="Mails envoyés", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
    bouton_mails_envoyés.place(x=largeur_ecran*0.52, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)

    bouton_corbeille = Button(fenetre_ecriture, text="Corbeille", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
    bouton_corbeille.place(x=largeur_ecran*0.72, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)


def ecrire_mail_brouillon():

    pass


def label(page):
    global fenetre_label
    if page == 1 :
        # Création d'une nouvelle fenêtre (évite les conflits avec Tk)
        fenetre_label = Toplevel(fenetre)
        fenetre_label.title("Ecrire un mail")
        fenetre_label.attributes("-fullscreen", True)

        bouton_home = Button(fenetre_label, image=photo_home, relief="flat", command=lambda: home("label")).place(x=largeur_ecran*0.05, y=hauteur_ecran*0.05)
        bouton_exit = Button(fenetre_label, image=photo_exit, relief="flat", command=fenetre.quit).place(x=largeur_ecran*0.95, y=hauteur_ecran*0.05)

        bouton_creation_label = Button(fenetre_label, text="Création d'un nouvelle catégorie", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
        bouton_creation_label.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.05, width=largeur_ecran*0.6, height=hauteur_ecran*0.065)
    elif page == 2 :
        pass


def corbeille():
    pass





# Création des 4 rectangles de menu

def page_accueil():

    global bouton_boite_de_reception
    global bouton_ecrire_mail
    global bouton_label
    global bouton_corbeille
    global bouton_settings
    global bouton_exit

    bouton_boite_de_reception = Button(fenetre, text="Boite de réception", image=photo_mail, font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20, command=lambda: boite_de_reception(1))
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






page_accueil()
fenetre.mainloop()