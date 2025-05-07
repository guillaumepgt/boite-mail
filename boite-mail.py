import time
from tkinter import *
import asyncio
import shutil
import platform

from fonction.envoyer_mail import *
from fonction.recevoir_mail import *
from fonction.recevoir_information import *
from fonction.contact import *
from fonction.icone_contacts import *
from fonction.mail_local import *

from fonction.graphique.fenetre import *
from fonction.graphique.chargement_image import *
from fonction.graphique.corbeille import *
from fonction.graphique.scroll import *
from fonction.graphique.fonction_bouton import *
from fonction.graphique.fonction_saisi import *

fenetre, largeur_ecran, hauteur_ecran = start()
images = charger_images(fenetre)

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
    global fenetre_boite, canvas
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
                if contact[i]["Email"] not in images["cache_image"] :
                    images["cache_image"] = enregistrer_icone_tkinter(contact)
                icone = images["cache_image"][contact[i]["Email"]]
                Button(frame_boite, compound="top", text=contact[i]["Nom"], image=icone, font=("Arial", 20),bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black",command=lambda email=contact[i]["Email"]: discussion(fenetre, email, "boite_principal", images, largeur_ecran, hauteur_ecran)).place(
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

        bouton_home = Button(fenetre_boite, image=images["home"], relief="flat", command=lambda: fenetre_boite.destroy())
        bouton_home.place(x=largeur_ecran * 0.05, y=hauteur_ecran * 0.05)

        bouton_exit = Button(fenetre_boite, image=images["exit"], relief="flat", command=fenetre.quit)
        bouton_exit.place(x=largeur_ecran * 0.95, y=hauteur_ecran * 0.05)

        if platform.system() in ['Windows', 'Darwin']:
            canvas.bind_all("<MouseWheel>", lambda e: scroll_canvas(canvas, e))
        else:
            canvas.bind_all("<Button-4>", lambda e: scroll_canvas(canvas, e))
            canvas.bind_all("<Button-5>", lambda e: scroll_canvas(canvas, e))


    elif page == 2 :

        canvas.delete("all")  # vide le contenu précédent du canvas
        canvas.yview_moveto(0) # remettre le canvas en haut

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
                if contact[i]["Email"] not in images["cache_image"] :
                    images["cache_image"] = enregistrer_icone_tkinter(contact)
                icone = images["cache_image"][contact[i]["Email"]]
                Button(frame_boite, compound="top", text=contact[i]["Nom"], image=icone, font=("Arial", 20),bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black",command=lambda email=contact[i]["Email"]: discussion(fenetre, email, "boite_principal", images, largeur_ecran, hauteur_ecran)).place(
                    x=largeur_ecran * [0.05, 0.35, 0.65][compteur % 3],
                    y=hauteur_ecran * (0.3 * (compteur // 3)),
                    width=largeur_ecran * 0.2,
                    height=hauteur_ecran * 0.2
                )
                compteur += 1


        if platform.system() in ['Windows', 'Darwin']:
            canvas.bind_all("<MouseWheel>", lambda e: scroll_canvas(canvas, e))
        else:
            canvas.bind_all("<Button-4>", lambda e: scroll_canvas(canvas, e))
            canvas.bind_all("<Button-5>", lambda e: scroll_canvas(canvas, e))




def ecrire_mail():
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

    if platform.system() in ['Windows', 'Darwin']:
        canvas.bind_all("<MouseWheel>", lambda e: scroll_canvas(canvas, e))
    else:
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")
        canvas.bind_all("<Button-4>", lambda e: scroll_canvas(canvas, e))
        canvas.bind_all("<Button-5>", lambda e: scroll_canvas(canvas, e))



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

    bouton_boite_de_reception = Button(fenetre_ecriture, text="Boite de réception", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", command=lambda: boite_de_reception(2))
    bouton_boite_de_reception.place(x=largeur_ecran*0.12, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)

    bouton_brouillon = Button(fenetre_ecriture, text="Brouillon", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", command =lambda: ecrire_mail_brouillon())
    bouton_brouillon.place(x=largeur_ecran*0.32, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)

    bouton_mails_envoyes = Button(fenetre_ecriture, text="Mails envoyés", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", command=envoye_mail)
    bouton_mails_envoyes.place(x=largeur_ecran*0.52, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)

    bouton_corbeille = Button(fenetre_ecriture, text="Corbeille", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", command=lambda: corbeille(2))
    bouton_corbeille.place(x=largeur_ecran*0.72, y=hauteur_ecran*0.055, width=largeur_ecran*0.18, height=hauteur_ecran*0.05)

def envoye_mail():
    global fenetre_boite, canvas
    canvas.delete("all")  # vide le contenu précédent du canvas
    canvas.yview_moveto(0) # remettre le canvas en haut

    # Frame dans le canvas pour contenir tous les boutons
    frame_boite = Frame(canvas)
    frame_boite.bind("<Configure>",lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    # Créer une fenêtre dans le canvas
    canvas_frame = canvas.create_window((0, 0), window=frame_boite, anchor="nw")

    contact = lire_mail("envoye_name_list")
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
            Button(frame_boite, compound="top", text=contact[i]["Nom"], image=icone, font=("Arial", 20),bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black",command=lambda email=contact[i]["Email"]: discussion(fenetre, email, "envoye", images, largeur_ecran, hauteur_ecran)).place(
                x=largeur_ecran * [0.05, 0.35, 0.65][compteur % 3],
                y=hauteur_ecran * (0.3 * (compteur // 3)),
                width=largeur_ecran * 0.2,
                height=hauteur_ecran * 0.2
            )
            compteur += 1

    if platform.system() in ['Windows', 'Darwin']:
        canvas.bind_all("<MouseWheel>", lambda e: scroll_canvas(canvas, e))
    else:
        canvas.bind_all("<Button-4>", lambda e: scroll_canvas(canvas, e))
        canvas.bind_all("<Button-5>", lambda e: scroll_canvas(canvas, e))

def ecrire_mail_brouillon():
    global canvas, brouillon

    canvas.delete("all")  # vide le contenu précédent du canvas
    canvas.yview_moveto(0) # remettre le canvas en haut


    # Créer un nouveau frame à insérer dans le canvas
    frame_brouillon = Frame(canvas)
    frame_brouillon.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame_brouillon, anchor="nw")

    compteur = 0

    # Afficher les brouillons
    different_brouillon = lire_mail("brouillon_list")
    frame_brouillon.config(width=largeur_ecran, height=hauteur_ecran * 3)

    for i, brouillon in enumerate(different_brouillon):
        sujet = brouillon["Sujet"]
        apercu_sujet = sujet[:10] + "..." if len(sujet) > 10 else sujet
        contenu = brouillon["Contenu"]
        apercu_contenu = contenu[:10] + "..." if len(contenu) > 10 else contenu
        Button(frame_brouillon, text=f"\n{apercu_sujet}\n\n{apercu_contenu}", font=("Arial", 20), bg="lightblue", fg="black",
               relief="flat", activebackground="white", activeforeground="black", command=lambda b=brouillon: modifier_brouillon(b)).place(
                x=largeur_ecran * [0.05, 0.35, 0.65][compteur % 3],
                y=hauteur_ecran * (0.3 * (compteur // 3)),
                width=largeur_ecran * 0.2,
                height=hauteur_ecran * 0.2
        )
        compteur += 1



    if platform.system() in ['Windows', 'Darwin']:
        canvas.bind_all("<MouseWheel>", lambda e: scroll_canvas(canvas, e))
    else:
        canvas.bind_all("<Button-4>", lambda e: scroll_canvas(canvas, e))
        canvas.bind_all("<Button-5>", lambda e: scroll_canvas(canvas, e))

def modifier_brouillon(brouillon):
    ecriture_objet.delete("1.0", "end")
    ecriture_mail.delete("1.0", "end")
     # Remplir l'objet si le champ est encore vide ou inchangé
    if ecriture_objet.get("1.0", "end-1c").strip() in ["", "Ecrire un objet"]:
        ecriture_objet.delete("1.0", "end")
        ecriture_objet.insert("1.0", brouillon["Sujet"])

    # Remplir le contenu si le champ est encore vide ou inchangé
    if ecriture_mail.get("1.0", "end-1c").strip() in ["", "Ecrire un mail"]:
        ecriture_mail.delete("1.0", "end")
        ecriture_mail.insert("1.0", brouillon["Contenu"])


def label():
    global fenetre_label
    # Création d'une nouvelle fenêtre (évite les conflits avec Tk)
    fenetre_label = Toplevel(fenetre)
    fenetre_label.title("Ecrire un mail")
    fenetre_label.attributes("-fullscreen", True)

    Button(fenetre_label, image=images["home"], relief="flat", command=lambda: fenetre_label.destroy()).place(x=largeur_ecran * 0.05, y=hauteur_ecran * 0.05)
    Button(fenetre_label, image=images["exit"], relief="flat", command=fenetre.quit).place(x=largeur_ecran * 0.95, y=hauteur_ecran * 0.05)

    bouton_creation_label = Button(fenetre_label, text="Création d'un nouvelle catégorie", font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black")
    bouton_creation_label.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.05, width=largeur_ecran*0.6, height=hauteur_ecran*0.065)



def corbeille(page):
    global fenetre_boite, canvas
    if page == 1 :
        # Création d'une nouvelle fenêtre
        fenetre_boite = Toplevel(fenetre)
        fenetre_boite.title("Corbeille")
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

        contact = lire_mail("full_name_list_corbeille")
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
                Button(frame_boite, compound="top", text=contact[i]["Nom"], image=icone, font=("Arial", 20),bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black",command=lambda email=contact[i]["Email"]: discussion(fenetre, email, "corbeille", images, largeur_ecran, hauteur_ecran)).place(
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

        bouton_home = Button(fenetre_boite, image=images["home"], relief="flat", command=lambda: fenetre_boite.destroy())
        bouton_home.place(x=largeur_ecran * 0.05, y=hauteur_ecran * 0.05)

        bouton_exit = Button(fenetre_boite, image=images["exit"], relief="flat", command=fenetre.quit)
        bouton_exit.place(x=largeur_ecran * 0.95, y=hauteur_ecran * 0.05)



        if platform.system() in ['Windows', 'Darwin']:
            canvas.bind_all("<MouseWheel>", lambda e: scroll_canvas(canvas, e))
        else:
            canvas.bind_all("<Button-4>", lambda e: scroll_canvas(canvas, e))
            canvas.bind_all("<Button-5>", lambda e: scroll_canvas(canvas, e))


    elif page == 2 :

        canvas.delete("all")  # vide le contenu précédent du canvas
        canvas.yview_moveto(0) # remettre le canvas en haut

        # Frame dans le canvas pour contenir tous les boutons
        frame_boite = Frame(canvas)
        frame_boite.bind("<Configure>",lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

        # Créer une fenêtre dans le canvas
        canvas_frame = canvas.create_window((0, 0), window=frame_boite, anchor="nw")

        contact = lire_mail("full_name_list_corbeille")
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
                Button(frame_boite, compound="top", text=contact[i]["Nom"], image=icone, font=("Arial", 20),bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black",command=lambda email=contact[i]["Email"]: discussion(fenetre, email, "corbeille", images, largeur_ecran, hauteur_ecran)).place(
                    x=largeur_ecran * [0.05, 0.35, 0.65][compteur % 3],
                    y=hauteur_ecran * (0.3 * (compteur // 3)),
                    width=largeur_ecran * 0.2,
                    height=hauteur_ecran * 0.2
                )
                compteur += 1


        if platform.system() in ['Windows', 'Darwin']:
            canvas.bind_all("<MouseWheel>", lambda e: scroll_canvas(canvas, e))
        else:
            canvas.bind_all("<Button-4>", lambda e: scroll_canvas(canvas, e))
            canvas.bind_all("<Button-5>", lambda e: scroll_canvas(canvas, e))

# Création des 4 rectangles de menu

def page_accueil():

    global bouton_boite_de_reception
    global bouton_ecrire_mail
    global bouton_label
    global bouton_corbeille
    global bouton_settings
    global bouton_exit

    bouton_boite_de_reception = Button(fenetre, text="Boite de réception", image=images["mail"], font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20, command=lambda: boite_de_reception(1))
    bouton_boite_de_reception.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.2, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


    bouton_ecrire_mail = Button(fenetre, text="Ecrire un mail", image=images["ecrire"], font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20, command=ecrire_mail)
    bouton_ecrire_mail.place(x=largeur_ecran*0.55, y=hauteur_ecran*0.2, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


    bouton_label = Button(fenetre, text="Categories", image=images["label"], font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20, command=label)
    bouton_label.place(x=largeur_ecran*0.2, y=hauteur_ecran*0.6, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


    bouton_corbeille = Button(fenetre, text="Corbeille", image=images["poubelle"], font=("Arial", 20), bg="lightblue", fg="black", relief="flat", activebackground="white", activeforeground="black", compound="bottom", pady=20, command=lambda: corbeille(1))
    bouton_corbeille.place(x=largeur_ecran*0.55, y=hauteur_ecran*0.6, width=largeur_ecran*0.25, height=hauteur_ecran*0.25)


    bouton_settings = Button(fenetre, image=images["profil"], relief="flat", command=parametre)
    bouton_settings.place(x=largeur_ecran*0.05, y=hauteur_ecran*0.05)
    Button(fenetre, image=images["exit"], relief="flat", command=fenetre.quit).place(x=largeur_ecran*0.95, y=hauteur_ecran*0.05)

page_accueil()
fenetre.mainloop()