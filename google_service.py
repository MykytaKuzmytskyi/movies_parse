import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from pandas import DataFrame

from imbd.settings import SERVICE_ACCOUNT_FILE_NAME

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_DIR, SERVICE_ACCOUNT_FILE_NAME)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def write_google_sheet(df: DataFrame, spreadsheet_id: str, range_name: str) -> None:
    data = [df.columns.values.tolist()] + df.values.tolist()

    body = {"values": data}
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("sheets", "v4", credentials=credentials)

    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body,
        )
        .execute()
    )

    print(f"{result.get('updatedCells')} cell updated.")
