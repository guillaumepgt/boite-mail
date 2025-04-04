import os
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Les scopes nécessaires pour Admin SDK API et Gmail API
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user.readonly']

# Fichier où les credentials sont sauvegardés
CREDENTIALS_FILE = 'token.pkl'

# Fonction pour récupérer les credentials OAuth2
def get_credentials():
    creds = None
    # Vérifie si un fichier token existe déjà
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'rb') as token:
            creds = pickle.load(token)

    # Si les credentials sont invalides ou expirés
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Sauvegarder les credentials
        with open(CREDENTIALS_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds

# Fonction pour récupérer la photo d'un utilisateur via Admin SDK
def get_user_photo(user_email):
    creds = get_credentials()
    service = build('admin', 'directory_v1', credentials=creds)

    try:
        # Récupérer la photo de l'utilisateur
        photo = service.users().photos().get(userKey=user_email).execute()
        photo_url = photo.get('photoUrl', 'Aucune photo disponible')
        return photo_url
    except Exception as e:
        return f"Erreur lors de la récupération de la photo : {e}"

# Exemple d'utilisation
if __name__ == "__main__":
    user_email = 'mailboite07@gmail.com'  # Remplace par l'email de l'utilisateur
    photo_url = get_user_photo(user_email)
    print(f"Photo de profil de {user_email} : {photo_url}")
