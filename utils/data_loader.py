import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from utils.config import SAMPLE_DATA_PATH, PRODUCTION_DATA_PATH, EXCEL_DATA_PATH
import os
import re
from datetime import datetime

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
        print(f"📊 File contains {len(df)} rows and {len(df.columns)} columns")
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

def process_landsoft_data(df):
    """
    Process LandSoft Excel data to match expected format
    """
    print("🔄 Processing LandSoft data...")
    
    # Create a copy for processing
    processed_df = df.copy()
    
    # Map LandSoft columns to expected format
    column_mapping = {
        'Gallery': 'id',
        'Mã sản phẩm': 'product_id',
        'Nhu cầu': 'transaction_type',
        'Số nhà': 'house_number',
        'Loại đường': 'street_type',
        'Tên đường': 'street_name',
        'Xã/Phường': 'ward',
        'Quận/huyện': 'district',
        'Ngang XD': 'width',
        'Dài XD': 'length',
        'Diện tích': 'area',
        'Tổng giá text': 'price_text',
        'Hướng': 'direction',
        'Chủ nhà': 'owner',
        'Điện thoại': 'phone',
        'Diễn giải': 'description',
        'Ngày ĐK': 'registration_date',
        'Ngày cập nhật': 'update_date',
        'Tỷ lệ MG': 'commission_rate',
        'CV môi giới': 'agent_name',
        'CV đăng tin': 'posted_by'
    }
    
    # Rename columns
    processed_df = processed_df.rename(columns=column_mapping)
    
    # Generate unique ID if not exists
    if 'id' not in processed_df.columns:
        if 'product_id' in processed_df.columns:
            processed_df['id'] = processed_df['product_id'].fillna('SP') + '_' + processed_df.index.astype(str)
        else:
            processed_df['id'] = 'SP_' + processed_df.index.astype(str)
    
    # Process address
    processed_df['address'] = processed_df.apply(
        lambda row: f"{row.get('house_number', '')} {row.get('street_name', '')}, {row.get('ward', '')}, {row.get('district', '')}".strip(),
        axis=1
    )
    
    # If address is empty or just commas, use a default
    processed_df['address'] = processed_df['address'].apply(
        lambda x: 'N/A' if not x or x.strip() in [',', ''] else x
    )
    
    # Process price
    if 'price_text' in processed_df.columns:
        processed_df['price'] = processed_df['price_text'].apply(parse_price_text)
    elif 'price' not in processed_df.columns:
        processed_df['price'] = 0
    
    # Process property type based on transaction type and description
    processed_df['type'] = processed_df.apply(determine_property_type, axis=1)
    
    # Extract bedrooms from description
    processed_df['bedrooms'] = processed_df['description'].apply(extract_bedrooms)
    
    # Process legal status (default to available)
    processed_df['legal_status'] = 'Sổ hồng'  # Default value
    
    # Process amenities from description
    processed_df['amenities'] = processed_df['description'].apply(extract_amenities)
    
    # Process status based on transaction type
    if 'transaction_type' in processed_df.columns:
        processed_df['status'] = processed_df['transaction_type'].apply(
            lambda x: 'available' if x == 'Cần bán' else 'for_rent' if x == 'Cho thuê' else 'available'
        )
    else:
        processed_df['status'] = 'available'
    
    # Add posted_date
    processed_df['posted_date'] = processed_df['registration_date'].apply(
        lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) and hasattr(x, 'strftime') else 
                 (x if pd.notna(x) and isinstance(x, str) else datetime.now().strftime('%Y-%m-%d'))
    )
    
    print(f"✅ Processed {len(processed_df)} records")
    return processed_df

def parse_price_text(price_text):
    """
    Parse price text to numeric value
    Examples: "50 triệu" -> 50000000, "6 tỷ 900 triệu" -> 6900000000
    """
    if pd.isna(price_text) or price_text == 'Thương lượng':
        return 0
    
    price_text = str(price_text).strip()
    
    # Handle "Thương lượng" or empty
    if 'thương lượng' in price_text.lower() or price_text == '':
        return 0
    
    total_price = 0
    
    # Extract billions (tỷ)
    billion_match = re.search(r'(\d+(?:\.\d+)?)\s*tỷ', price_text, re.IGNORECASE)
    if billion_match:
        total_price += float(billion_match.group(1)) * 1000000000
    
    # Extract millions (triệu)
    million_match = re.search(r'(\d+(?:\.\d+)?)\s*triệu', price_text, re.IGNORECASE)
    if million_match:
        total_price += float(million_match.group(1)) * 1000000
    
    # Extract thousands (nghìn)
    thousand_match = re.search(r'(\d+(?:\.\d+)?)\s*nghìn', price_text, re.IGNORECASE)
    if thousand_match:
        total_price += float(thousand_match.group(1)) * 1000
    
    return int(total_price) if total_price > 0 else 0

def determine_property_type(row):
    """
    Determine property type based on transaction type and description
    """
    description = str(row.get('description', '')).lower()
    transaction_type = str(row.get('transaction_type', '')).lower()
    
    # Check for specific keywords in description
    if any(word in description for word in ['căn hộ', 'apartment', 'chung cư']):
        return 'Căn hộ'
    elif any(word in description for word in ['nhà phố', 'shophouse', 'nhà mặt tiền']):
        return 'Nhà phố'
    elif any(word in description for word in ['biệt thự', 'villa']):
        return 'Biệt thự'
    elif any(word in description for word in ['văn phòng', 'office']):
        return 'Văn phòng'
    elif any(word in description for word in ['đất nền', 'đất thổ cư']):
        return 'Đất nền'
    else:
        # Default based on transaction type
        if 'cho thuê' in transaction_type:
            return 'Căn hộ'  # Most common for rental
        else:
            return 'Nhà phố'  # Most common for sale

def extract_bedrooms(description):
    """
    Extract number of bedrooms from description
    """
    if pd.isna(description):
        return 0
    
    description = str(description).lower()
    
    # Look for bedroom patterns
    patterns = [
        r'(\d+)\s*phòng\s*ngủ',
        r'(\d+)\s*pn',
        r'(\d+)\s*bedroom',
        r'(\d+)\s*br'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, description)
        if match:
            return int(match.group(1))
    
    return 0

def extract_amenities(description):
    """
    Extract amenities from description
    """
    if pd.isna(description):
        return ''
    
    description = str(description).lower()
    amenities = []
    
    # Common amenities to look for
    amenity_keywords = {
        'hồ bơi': 'Hồ bơi',
        'gym': 'Gym',
        'thang máy': 'Thang máy',
        'bãi xe': 'Bãi xe',
        'an ninh': 'An ninh 24/7',
        'sân chơi': 'Sân chơi trẻ em',
        'vườn': 'Vườn',
        'sân thượng': 'Sân thượng',
        'ban công': 'Ban công',
        'nhà bếp': 'Nhà bếp',
        'phòng khách': 'Phòng khách',
        'wc': 'WC riêng',
        'điều hòa': 'Điều hòa',
        'nóng lạnh': 'Nóng lạnh',
        'internet': 'Internet',
        'truyền hình': 'Truyền hình cáp'
    }
    
    for keyword, amenity in amenity_keywords.items():
        if keyword in description:
            amenities.append(amenity)
    
    return ', '.join(amenities) if amenities else 'Cơ bản'

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

def process_google_sheets_data(df):
    """
    Process Google Sheets data to ensure all required columns are present
    """
    print("🔄 Processing Google Sheets data...")
    
    # Create a copy for processing
    processed_df = df.copy()
    
    # Ensure required columns exist with default values
    required_columns = {
        'id': lambda df: df.index.astype(str) if 'id' not in df.columns else df['id'],
        'type': lambda df: ['Nhà phố'] * len(df) if 'type' not in df.columns else df['type'],
        'district': lambda df: ['Quận 1'] * len(df) if 'district' not in df.columns else df['district'],
        'ward': lambda df: ['Bến Nghé'] * len(df) if 'ward' not in df.columns else df['ward'],
        'address': lambda df: df['address'] if 'address' in df.columns else 
                             (df['district'] + ', ' + df['ward'] if 'district' in df.columns and 'ward' in df.columns else ['N/A'] * len(df)),
        'price': lambda df: [0] * len(df) if 'price' not in df.columns else df['price'],
        'area': lambda df: [0] * len(df) if 'area' not in df.columns else df['area'],
        'bedrooms': lambda df: [0] * len(df) if 'bedrooms' not in df.columns else df['bedrooms'],
        'direction': lambda df: ['N/A'] * len(df) if 'direction' not in df.columns else df['direction'],
        'legal_status': lambda df: ['Sổ hồng'] * len(df) if 'legal_status' not in df.columns else df['legal_status'],
        'amenities': lambda df: ['Cơ bản'] * len(df) if 'amenities' not in df.columns else df['amenities'],
        'description': lambda df: ['N/A'] * len(df) if 'description' not in df.columns else df['description']
    }
    
    # Add missing columns with default values
    for col, default_func in required_columns.items():
        if col not in processed_df.columns:
            processed_df[col] = default_func(processed_df)
            print(f"  ✅ Added missing column '{col}' with default values")
    
    # Ensure numeric columns are properly formatted
    numeric_columns = ['price', 'area', 'bedrooms']
    for col in numeric_columns:
        if col in processed_df.columns:
            processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce').fillna(0)
    
    print(f"✅ Processed {len(processed_df)} records")
    return processed_df

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