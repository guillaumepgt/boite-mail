import base64
import smtplib
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.utils import parseaddr

def recevoir_envoyes():
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    # Récupérer les mails envoyés
    results = service.users().messages().list(
        userId="me",
        labelIds=["SENT"],
        maxResults=1000
    ).execute()

    messages = results.get("messages", [])

    envoyes = []
    for msg in messages:
        message_id = msg["id"]
        msg_data = service.users().messages().get(userId="me", id=message_id, format="full").execute()
        headers = msg_data["payload"]["headers"]

        sender = parseaddr(next((h["value"] for h in headers if h["name"] == "From"), "Inconnu"))[1]
        recipient = next((h["value"] for h in headers if h["name"] == "To"), "Inconnu")
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "Sans Sujet")

        def get_body(payload):
            if "parts" in payload:
                for part in payload["parts"]:
                    if part["mimeType"] == "text/plain" and "data" in part["body"]:
                        data = part["body"]["data"]
                        return base64.urlsafe_b64decode(data).decode("utf-8")
            elif payload.get("mimeType") == "text/plain" and "data" in payload.get("body", {}):
                data = payload["body"]["data"]
                return base64.urlsafe_b64decode(data).decode("utf-8")
            return "Aucun contenu trouvé."

        body = get_body(msg_data["payload"])

        envoyes.append({
            "id": message_id,
            "Expediteur": sender,
            "Destinataire": recipient,
            "Sujet": subject,
            "Contenu": body
        })

    print("✅ Mails envoyés récupérés avec succès !")
    return envoyes

# Fonction pour générer l'authentification OAuth2
def generate_oauth2_string(username, access_token):
    auth_string = f"user={username}\1auth=Bearer {access_token}\1\1"
    return base64.b64encode(auth_string.encode("ascii")).decode("ascii")

# Fonction pour envoyer un e-mail
def envoyer_email(subject, body, sender, recipients):
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
try:
    from fonction.get_tokens import *
except ImportError:
    from get_tokens import *
    if __name__ == '__main__':
        # Définir les informations nécessaires
        sender = 'mailboite07@gmail.com'
        recipients = ['mailboite07@gmail.com']
        subject = "salo"
        body = "zabiubfyzayufazb"
        envoyer_email(subject, body, sender, recipients)
