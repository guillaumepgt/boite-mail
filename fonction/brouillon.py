import base64
from email.utils import parseaddr
from googleapiclient.discovery import build

def recevoir_brouillons():
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    # Récupérer les brouillons
    results = service.users().drafts().list(userId="me", maxResults=1000).execute()
    drafts = results.get("drafts", [])

    brouillons = []
    for draft in drafts:
        draft_id = draft["id"]
        draft_data = service.users().drafts().get(userId="me", id=draft_id, format="full").execute()
        message = draft_data.get("message", {})
        headers = message.get("payload", {}).get("headers", [])

        # Extraire les informations principales
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

        body = get_body(message.get("payload", {}))

        brouillons.append({
            "Expéditeur": sender,
            "Destinataire": recipient,
            "Sujet": subject,
            "Contenu": body
        })

    print("✅ Brouillons récupérés avec succès !")
    return brouillons

try:
    # Si le module est utilisé dans un projet structuré avec sous-dossiers
    from fonction.get_tokens import *
except ImportError:
    # Si le fichier est lancé directement, en standalone
    from get_tokens import *
    print(recevoir_brouillons())