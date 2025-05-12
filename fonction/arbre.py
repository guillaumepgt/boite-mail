import json

class Arbre:
    def __init__(self, nom):
        self.nom = nom
        self.enfants = {}  # clé : nom (ex: sujet), valeur : Arbre
        self.mails = []    # seulement pour les feuilles

    def ajouter_mail(self, expediteur, sujet, mail):
        # Ajoute ou récupère le nœud de l'expéditeur
        if expediteur not in self.enfants:
            self.enfants[expediteur] = Arbre(expediteur)
        noeud_expediteur = self.enfants[expediteur]

        # Ajoute ou récupère le nœud du sujet
        if sujet not in noeud_expediteur.enfants:
            noeud_expediteur.enfants[sujet] = Arbre(sujet)
        noeud_sujet = noeud_expediteur.enfants[sujet]

        # Ajoute le mail à la feuille
        noeud_sujet.mails.append(mail)

    def afficher(self, niveau=0):
        indent = "  " * niveau
        if self.mails:
            print(f"{indent}- {self.nom} ({len(self.mails)} mails)")
        else:
            print(f"{indent}- {self.nom}")
            for enfant in self.enfants.values():
                enfant.afficher(niveau + 1)

# Exemple d'utilisation
if __name__ == "__main__":
    from mail_local import *
    mails = lire_mail("mail")

    arbre = Arbre("Boîte mail")

    for mail in mails:
        expediteur = mail.get("Expediteur", "Inconnu")
        sujet = mail.get("Sujet", "Sans sujet")
        arbre.ajouter_mail(expediteur, sujet, mail)

    arbre.afficher()
