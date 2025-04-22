import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from get_tokens import *

# ✅ Scopes nécessaires pour récupérer les infos utilisateur
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid"
]

CREDENTIALS_FILE = "token.pkl"
CLIENT_SECRET_FILE = "client_secret.json"


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