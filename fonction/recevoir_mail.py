import base64
from email import errors
from email.utils import parseaddr
from googleapiclient.discovery import build

def get_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
                return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
    elif payload.get("mimeType") == "text/plain" and "data" in payload.get("body", {}):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
    return "Aucun contenu trouvé."

def recevoir_email(type, nombre):
    user_email = get_user_info()["email"]
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)
    type2 = {
        "messages": service.users().messages(),
        "drafts": service.users().drafts()
    }
    params = {
        "userId": "me",
        "maxResults": nombre,
        "includeSpamTrash": True
    }
    full_email_list = []
    if type == "messages":
        params["labelIds"] = "INBOX"
    try:
        results = type2[type].list(**params).execute()
        messages = results.get("messages" if type == "messages" else "drafts", [])
    except errors.HttpError as error:
        print(f"Erreur lors de la récupération des {type} : {error}")
        return []

    for msg in messages:
        if type == "messages":
            msg_data = type2[type].get(userId="me", id=msg["id"], format="full").execute()
            payload = msg_data.get("payload", {})
            headers = payload.get("headers", [])
        elif type == "drafts":
            draft = type2[type].get(userId="me", id=msg["id"]).execute()
            msg_data = draft.get("message", {})
            payload = msg_data.get("payload", {})
            headers = payload.get("headers", [])

        sender = parseaddr(next((h["value"] for h in headers if h["name"] == "From"), "Inconnu"))[1]
        recipient = next((h["value"] for h in headers if h["name"] == "To"), "Inconnu")
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "Sans Sujet")
        body = get_body(payload)

        # if (recipient == user_email and type == "messages") or type == "drafts":
        full_email_list.append({
                "id": msg["id"],
                "Expéditeur": sender,
                "Destinataire": recipient,
                "Sujet": subject,
                "Contenu": body
            })
    if type == "messages":
        print("✅ Emails récupérés avec succès !")
    else:
        print("Brouillon récupérer avec succès")
    return full_email_list

try:
    # Si le module est utilisé dans un projet structuré avec sous-dossiers
    from fonction.get_tokens import *
    from fonction.recevoir_information import *
except ImportError:
    # Si le fichier est lancé directement, en standalone
    from get_tokens import *
    from recevoir_information import *
    if __name__ == "__main__":
        print(recevoir_email("messages", 100))

