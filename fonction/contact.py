import os
import base64
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.utils import parseaddr
import re

def deviner_nom_prenom_depuis_email(email):
    # Ex : "john.doe@gmail.com" → "John", "Doe"
    local_part = email.split("@")[0]
    local_part = re.sub(r"\d+", "", local_part)  # Supprimer tous les chiffres
    parts = local_part.replace(".", " ").replace("_", " ").split()

    if len(parts) == 0:
        return "", ""
    elif len(parts) == 1:
        return parts[0].capitalize(), ""
    else:
        return parts[0].capitalize(), parts[1].capitalize()

def recevoir_email2():
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    # Récupérer les 10 derniers messages
    results = service.users().messages().list(userId="me", maxResults=1000).execute()
    messages = results.get("messages", [])

    full_email_list = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = msg_data["payload"]["headers"]

        # Extraire les champs
        raw_sender = next((h["value"] for h in headers if h["name"] == "From"), "Inconnu")

        # Parser l'expéditeur
        name, email_address = parseaddr(raw_sender)

        if name:
            first_name, last_name = (name.split(" ", 1) + [""])[:2]
        else:
            first_name, last_name = deviner_nom_prenom_depuis_email(email_address)

        body = msg_data.get("snippet", "Aucun contenu trouvé.")

        full_email_list.append({
            "Nom": name if name else f"{first_name} {last_name}".strip(),
            "Email": email_address
        })

    return full_email_list

try:
    # Si le module est utilisé dans un projet structuré avec sous-dossiers
    from fonction.get_tokens import *
except ImportError:
    # Si le fichier est lancé directement, en standalone
    from get_tokens import *
    print("✅ Emails récupérés avec succès !\n", recevoir_email2())
