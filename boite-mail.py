from tkinter import *

fenetre = Tk()
fenetre.title("Boite Mail")
fenetre.attributes("-fullscreen", True)  # Active le mode plein écran
fenetre.iconbitmap("logo.ico")  # Vérifiez que "logo.ico" existe

"""# Quitter le plein écran avec Échap
fenetre.bind("<Escape>", lambda event: fenetre.attributes("-fullscreen", False))"""





# Création des 4 rectangles de menu


can = Canvas(fenetre, width=200, height=800, bg="blue")
can.place(x=100, y=100)













fenetre.mainloop()