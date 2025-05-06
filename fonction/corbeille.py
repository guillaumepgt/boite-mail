import base64
from email.utils import parseaddr
from googleapiclient.discovery import build

def recevoir_corbeille():
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    # Récupérer les messages de la corbeille
    results = service.users().messages().list(
        userId="me",
        labelIds=["TRASH"],
        includeSpamTrash=True,
        maxResults=1000
    ).execute()

    messages = results.get("messages", [])

    corbeille = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"], format="full").execute()
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

        corbeille.append({
            "Expéditeur": sender,
            "Destinataire": recipient,
            "Sujet": subject,
            "Contenu": body
        })

    print("🗑️ Corbeille récupérée avec succès !")
    return corbeille

try:
    # Si le module est utilisé dans un projet structuré avec sous-dossiers
    from fonction.get_tokens import *
except ImportError:
    # Si le fichier est lancé directement, en standalone
    from get_tokens import *
    print(recevoir_corbeille())