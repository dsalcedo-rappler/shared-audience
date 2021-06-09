import io
import pandas as pd
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def authorize_api(token_file = "token.json"):
    """
    Authorizes you to use Google APIs directly
    Upload the token.json file to this google colab first
    """

    
    SCOPES = [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/youtube'
    ]
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    drive = build('drive', 'v3', credentials=creds)
    sheets = build('sheets', 'v4', credentials=creds)
    calendar = build('calendar', 'v3', credentials=creds)
    youtube = build('youtube', 'v3', credentials=creds)

    return {'drive': drive, 'sheets': sheets, 'calendar': calendar, 'youtube': youtube}

def download_from_gsheets(link,sheet = 'Sheet1'):
    """
    Retrieves a google sheet to be used as a pandas dataframe
    """
    sheets = authorize_api()['sheets']
    spreadsheet_id = link.split('/')[5]

    result = sheets.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet
    ).execute()
    
    return pd.DataFrame(result['values'][1:], columns=result['values'][0])

def download_from_gdrive(link, colab_filename = 'Filename.csv'):
    """
    Downloads a csv form google drive and reutrns it as a pandas dataframe
    """
    drive = authorize_api()['drive']
    gdrive_id = link.split('/')[5]

    request = drive.files().get_media(fileId = gdrive_id) 
    fh = io.FileIO(colab_filename,'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    
    return pd.read_csv(colab_filename)

df = download_from_gdrive(
    link = "https://drive.google.com/file/d/1OVmeGIuw-ZrSbWI2moJU_ihuGhTKhdLu/view?usp=sharing",
    colab_filename = "sharktank-db-202104.csv"
)
print(df.head())