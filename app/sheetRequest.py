import gspread
from google.oauth2.service_account import Credentials
from ..config import settings

def get_google_sheet():
    creds = Credentials.from_service_account_file(
        "service_account.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    print("Google: success obtained creds")
    gc = gspread.authorize(credentials=creds)
    sheet = gc.open_by_url(settings.g_dock)
    return sheet
