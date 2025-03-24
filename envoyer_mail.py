import os
import base64
import pickle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://mail.google.com/']
CREDENTIALS_FILE = 'token.pkl'

def get_credentials():
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

# Fonction pour générer l'authentification OAuth2
def generate_oauth2_string(username, access_token):
    auth_string = f"user={username}\1auth=Bearer {access_token}\1\1"
    return base64.b64encode(auth_string.encode("ascii")).decode("ascii")

# Fonction pour envoyer un e-mail
def send_email(subject, body, sender, recipients):
    creds = get_credentials()  # Récupérer les credentials
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
    recipients = ['ugo.bernard@reseau.eseo.fr']
    subject = "salut"
    body = "gourmand"

    # Envoyer l'e-mail
    send_email(subject, body, sender, recipients)
