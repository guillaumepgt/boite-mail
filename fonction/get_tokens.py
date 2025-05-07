import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_credentials():
    if os.path.exists("./private"):
        CREDENTIALS_FILE = "private/token.pkl"
        client_secrets_file = "private/client_secret.json"
    elif os.path.exists("../../private"):
        CREDENTIALS_FILE = "../../private/token.pkl"
        client_secrets_file = "../../private/client_secret.json"
    elif os.path.exists("../private"):
        CREDENTIALS_FILE = "../private/token.pkl"
        client_secrets_file = "../private/client_secret.json"
    else:
        return error

    SCOPES = ["https://mail.google.com/", "https://www.googleapis.com/auth/userinfo.profile",
              "https://www.googleapis.com/auth/userinfo.email",
              "openid"]
    creds = None
    # Si un token existe déjà
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'rb') as token:
            creds = pickle.load(token)

    # Si les credentials sont invalides ou expirés
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=5000)

        # Sauvegarde des nouveaux credentials
        with open(CREDENTIALS_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds