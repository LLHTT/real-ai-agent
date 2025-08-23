import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from utils.config import SAMPLE_DATA_PATH, PRODUCTION_DATA_PATH
import os

def load_data(source_type='sample', sheet_url=None, credentials_path='credentials.json'):
    """
    Load real estate data from different sources
    
    Args:
        source_type: 'sample' | 'csv' | 'gsheet'
        sheet_url: Required for 'gsheet' type
        credentials_path: Path to Google Service Account credentials
        
    Returns:
        pandas.DataFrame
    """
    if source_type == 'sample':
        return pd.read_csv(SAMPLE_DATA_PATH)
    
    elif source_type == 'csv':
        return pd.read_csv(PRODUCTION_DATA_PATH)
    
    elif source_type == 'gsheet':
        return load_google_sheet(sheet_url, credentials_path)
    
    else:
        raise ValueError(f"Invalid source type: {source_type}")

def load_google_sheet(sheet_url, credentials_path='credentials.json'):
    """Load data from Google Sheet using service account credentials"""
    # Set up authentication
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"Google credentials file not found at {credentials_path}. "
            "Please download from Google Cloud Console"
        )
    
    creds = Credentials.from_service_account_file(
        credentials_path,
        scopes=scopes
    )
    
    # Connect to Google Sheets
    client = gspread.authorize(creds)
    
    try:
        # Open the spreadsheet
        spreadsheet = client.open_by_url(sheet_url)
        
        # Get the first worksheet
        worksheet = spreadsheet.get_worksheet(0)
        
        # Get all records as a list of dictionaries
        records = worksheet.get_all_records()
        
        # Convert to DataFrame
        return pd.DataFrame(records)
        
    except Exception as e:
        raise ConnectionError(
            f"Failed to access Google Sheet: {str(e)}\n"
            "Ensure: \n"
            "1. Sheet URL is correct\n"
            "2. Service account has been granted access\n"
            "3. Sheet structure matches expected format"
        )