from boite_mail_Backend.get_tokens import *
import os
import base64
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def recevoir_mails():
    SCOPES = ["https://mail.google.com/"]
    CREDENTIALS_FILE = "../token.pkl"

    creds = get_credentials(CREDENTIALS_FILE, SCOPES)
    service = build("gmail", "v1", credentials=creds)

    # Récupérer les 10 derniers messages
    results = service.users().messages().list(userId="me", maxResults=10).execute()
    messages = results.get("messages", [])

    full_email_list = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()

        headers = msg_data["payload"]["headers"]

        # Extraire l'expéditeur, le destinataire et le sujet
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Inconnu")
        recipient = next((h["value"] for h in headers if h["name"] == "To"), "Inconnu")
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "Sans Sujet")

        # Récupérer le corps du message (si présent)
        body = "Aucun contenu trouvé."
        if msg_data["snippet"] :
            body = msg_data["snippet"]

        # Ajouter l'e-mail complet à la liste
        full_email_list.append({
            "Expéditeur": sender,
            "Destinataire": recipient,
            "Sujet": subject,
            "Contenu": body
        })
    print(full_email_list)
    return full_email_list
