
def get_agents(pages,posts,index):
    """
    Return the unique agents of a certain channel as a set list
    """
    site = pages.loc[index]
    agents = posts[ (posts['linkEntityId'] == site['linkEntityId']) & (posts['linkType'] == site['channelType']) ]['fromProfile']
    return set(list(agents))

def shared_audience(pages,posts,site_ind1,site_ind2,threshold=0):
    """
    Returns the if two channels have a shared audience greater than the threshold,
    as well as how many common agents they have
    """
    agents1 = get_agents(pages,posts,site_ind1)
    agents2 = get_agents(pages,posts,site_ind2)
    common_agents = agents1.intersection(agents2)

    if len(common_agents) >= threshold:
        return {"shared": True, "commons": len(common_agents) }
    else:
        return {"shared": False, "commons": len(common_agents) }

def authorize_api(token_file = "token.json"):
    """
    Authorizes you to use Google APIs directly
    Upload the token.json file to this google colab first
    """
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    
    SCOPES = [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/documents',
        'https://www.googleapis.com/auth/youtube'
    ]
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    drive = build('drive', 'v3', credentials=creds)
    sheets = build('sheets', 'v4', credentials=creds)
    docs = build('docs','v1', credentials=creds)
    calendar = build('calendar', 'v3', credentials=creds)
    youtube = build('youtube', 'v3', credentials=creds)

    return {'drive': drive, 'sheets': sheets, 'docs': docs, 'calendar': calendar, 'youtube': youtube}

def download_from_gsheets(link,sheet = 'Sheet1'):
    """
    Retrieves a google sheet to be used as a pandas dataframe
    """
    import pandas as pd
    sheets = authorize_api()['sheets']
    spreadsheet_id = link.split('/')[5]

    result = sheets.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet
    ).execute()
    
    return pd.DataFrame(result['values'][1:], columns=result['values'][0])

def export_to_sheet(df, link, sheet_name):
    """
    Updates google sheet data with the given pandas dataframe
    """
    sheets = authorize_api()['sheets']
    spreadsheet_id = link.split('/')[5]
    
    to_export = [list(df.columns)]
    to_export.extend(df.values.tolist())
    body = {'values': to_export}

    updated_sheet = sheets.spreadsheets().values().update(
        spreadsheetId = spreadsheet_id,
        range = sheet_name,
        valueInputOption = "RAW",
        body = body
    ).execute()