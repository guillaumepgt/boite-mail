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


def get_user_info():
    """ Récupère les informations de l'utilisateur connecté. """
    creds = get_credentials()
    service = build("oauth2", "v2", credentials=creds)
    try:
        user_info = service.userinfo().get().execute()
    except:
        print("aucune connexion")
    return user_info

def connecter():
    if os.path.exists(CREDENTIALS_FILE):
        return True
    return False

def download_profil_img(url):
    import urllib.request
    from PIL import Image
    import io
    os.makedirs('private/icones', exist_ok=True)
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()
    image = Image.open(io.BytesIO(raw_data))
    chemin_sauvegarde = os.path.join('private/icones', 'profil.png')
    image.save(chemin_sauvegarde, format="PNG")
    return chemin_sauvegarde

try:
    from fonction.get_tokens import *
    CREDENTIALS_FILE = "private/token.pkl"
    CLIENT_SECRET_FILE = "private/client_secret.json"
except ImportError:
    CREDENTIALS_FILE = "../private/token.pkl"
    CLIENT_SECRET_FILE = "../private/client_secret.json"
    from get_tokens import *
    if connecter():
        if __name__ == "__main__":
            user_info = get_user_info()
            print("✅ Informations de l'utilisateur connecté :")
            print(f"📧 Email      : {user_info['email']}")
            print(f"👤 Nom        : {user_info.get('name', 'Inconnu')}")
            print(f"🖼️ Photo URL  : {user_info.get('picture', 'Aucune photo disponible')}")