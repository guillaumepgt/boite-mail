import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ✅ Scopes nécessaires pour récupérer les infos utilisateur
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid"
]

CREDENTIALS_FILE = "../token.pkl"
CLIENT_SECRET_FILE = "client_secret.json"

def get_credentials():
    """ Authentifie l'utilisateur et gère les credentials OAuth2. """
    creds = None
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid or not creds.refresh_token:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=5000)

        with open(CREDENTIALS_FILE, "wb") as token:
            pickle.dump(creds, token)

    return creds


def get_user_info():
    """ Récupère les informations de l'utilisateur connecté. """
    creds = get_credentials()
    service = build("oauth2", "v2", credentials=creds)

    user_info = service.userinfo().get().execute()
    return user_info

# 🔥 Exécuter la récupération des infos utilisateur
if __name__ == "__main__":
    user_info = get_user_info()
    print("✅ Informations de l'utilisateur connecté :")
    print(f"📧 Email      : {user_info['email']}")
    print(f"👤 Nom        : {user_info.get('name', 'Inconnu')}")
    print(f"🖼️ Photo URL  : {user_info.get('picture', 'Aucune photo disponible')}")
