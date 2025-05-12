import base64
from email.utils import parseaddr
from googleapiclient.discovery import build

def mettre_a_la_corbeille(message_id):
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    try:
        service.users().messages().trash(userId="me", id=message_id).execute()
        print(f"🗑️ Message {message_id} déplacé vers la corbeille.")
    except Exception as e:
        print(f"❌ Erreur lors de la suppression du message {message_id} : {e}")


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

        id = msg["id"]
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
            "id": id,
            "Expediteur": sender,
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
    if __name__ == "__main__":
        print(recevoir_corbeille())