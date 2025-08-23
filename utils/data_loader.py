import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from utils.config import SAMPLE_DATA_PATH, PRODUCTION_DATA_PATH, EXCEL_DATA_PATH
import os

def load_data(source_type='sample', sheet_url=None, credentials_path='credentials.json', file_path=None):
    """
    Load real estate data from different sources
    
    Args:
        source_type: 'sample' | 'csv' | 'excel' | 'gsheet'
        sheet_url: Required for 'gsheet' type
        credentials_path: Path to Google Service Account credentials
        file_path: Optional custom file path for csv/excel
        
    Returns:
        pandas.DataFrame
    """
    if source_type == 'sample':
        return pd.read_csv(SAMPLE_DATA_PATH)
    
    elif source_type == 'csv':
        file_to_read = file_path or PRODUCTION_DATA_PATH
        return pd.read_csv(file_to_read)
    
    elif source_type == 'excel':
        file_to_read = file_path or EXCEL_DATA_PATH
        return load_excel_file(file_to_read)
    
    elif source_type == 'gsheet':
        return load_google_sheet(sheet_url, credentials_path)
    
    else:
        raise ValueError(f"Invalid source type: {source_type}")

def load_excel_file(file_path):
    """Load data from Excel file (.xls or .xlsx)"""
    try:
        # Try to read the Excel file
        df = pd.read_excel(file_path)
        
        # Basic validation
        if df.empty:
            raise ValueError("Excel file is empty")
        
        print(f"✅ Successfully loaded Excel file: {file_path}")
        print(f" File contains {len(df)} rows and {len(df.columns)} columns")
        print(f"📋 Columns: {list(df.columns)}")
        
        return df
        
    except ImportError as e:
        if "xlrd" in str(e):
            raise ImportError(
                "xlrd library not found. Install with: pip install xlrd"
            )
        elif "openpyxl" in str(e):
            raise ImportError(
                "openpyxl library not found. Install with: pip install openpyxl"
            )
        else:
            raise ImportError(f"Excel reading library not found: {e}")
    
    except Exception as e:
        raise Exception(f"Error reading Excel file {file_path}: {str(e)}")

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

def analyze_data_structure(df, source_type):
    """Analyze and report data structure"""
    print(f"\n📊 Data Structure Analysis for {source_type}:")
    print("=" * 50)
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Columns: {list(df.columns)}")
    
    # Check for required columns
    required_columns = ['id', 'type', 'district', 'ward', 'address', 'price', 'area', 'bedrooms', 'direction', 'legal_status', 'amenities', 'description']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"\n⚠️ Missing required columns: {missing_columns}")
        print("💡 You may need to map your Excel columns to the expected format")
    else:
        print(f"\n✅ All required columns found!")
    
    return missing_columns