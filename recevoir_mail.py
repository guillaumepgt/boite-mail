import asyncio
from get_tokens import *
import os
import base64
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.utils import parseaddr

async def recevoir_email():
    loop = asyncio.get_running_loop()
    creds = await loop.run_in_executor(None, get_credentials)
    service = build("gmail", "v1", credentials=creds)

    # Récupérer les 10 derniers messages de manière asynchrone
    results = await loop.run_in_executor(None, service.users().messages().list, "me", {"maxResults": 1000})
    messages = results.get("messages", [])

    full_email_list = []
    for msg in messages:
        msg_data = await loop.run_in_executor(None, service.users().messages().get, "me", msg["id"])

        headers = msg_data["payload"]["headers"]

        # Extraire l'expéditeur, le destinataire et le sujet
        sender = parseaddr(next((h["value"] for h in headers if h["name"] == "From"), "Inconnu"))[1]
        recipient = next((h["value"] for h in headers if h["name"] == "To"), "Inconnu")
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "Sans Sujet")

        # Récupérer le corps du message (si présent)
        body = "Aucun contenu trouvé."
        if msg_data["snippet"]:
            body = msg_data["snippet"]

        # Ajouter l'e-mail complet à la liste
        full_email_list.append({
            "Expéditeur": sender,
            "Destinataire": recipient,
            "Sujet": subject,
            "Contenu": body
        })

    print("✅ Emails récupérés avec succès !")
    return full_email_list

if __name__ == "__main__":
    emails = asyncio.run(recevoir_email())
    print(len(emails))
