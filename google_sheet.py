from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_sheet_data(spreadsheet_id, range_name):
    creds = Credentials.from_authorized_user_file("token.json")
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result.get("values", [])
