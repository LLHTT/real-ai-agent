import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from utils.config import *
from utils.data_loader import load_data, analyze_data_structure, process_landsoft_data, process_google_sheets_data

# Load env
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Load và xử lý dữ liệu
def load_and_process_data(source_type='sample', sheet_url=None, credentials_path=None, file_path=None):
    """
    Load and process data from different sources
    
    Args:
        source_type: 'sample', 'csv', 'excel', or 'gsheet'
        sheet_url: Required for 'gsheet' type
        credentials_path: Path to Google credentials (optional, uses default if None)
        file_path: Optional custom file path for csv/excel
    """
    try:
        # Load data from source
        if source_type == 'gsheet':
            if not sheet_url:
                raise ValueError("Sheet URL is required for Google Sheets source")
            # Only pass credentials_path if explicitly provided (for local development)
            # In deployment, let load_data use environment variable
            if credentials_path:
                df = load_data(source_type='gsheet', sheet_url=sheet_url, credentials_path=credentials_path)
            else:
                df = load_data(source_type='gsheet', sheet_url=sheet_url)
        else:
            df = load_data(source_type=source_type, file_path=file_path)
        
        # For Excel files, process LandSoft data
        if source_type == 'excel':
            df = process_landsoft_data(df)
        # For Google Sheets, process data to ensure required columns
        elif source_type == 'gsheet':
            df = process_google_sheets_data(df)
        
        # Analyze data structure
        missing_columns = analyze_data_structure(df, source_type)
        
        # If missing required columns, try to map them (for non-Excel, non-GSheet sources)
        if missing_columns and source_type not in ['excel', 'gsheet']:
            df = map_excel_columns(df)
        
        # Validate required columns after processing
        required_columns = ['id', 'type', 'district', 'ward', 'address', 'price', 'area', 'bedrooms', 'direction', 'legal_status', 'amenities', 'description']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns after processing: {missing_columns}")
        
        # Tạo text embedding cho mỗi sản phẩm với thông tin chi tiết hơn
        df['text'] = df.apply(create_detailed_text_embedding, axis=1)
        
        return df
        
    except Exception as e:
        raise Exception(f"Error loading data from {source_type}: {str(e)}")

def create_detailed_text_embedding(row):
    """
    Create detailed text embedding for LandSoft data
    """
    # Format price
    price_display = "Thương lượng" if row['price'] == 0 else f"{row['price']:,.0f} VND"
    
    # Format area with dimensions if available
    area_info = f"{row['area']}m²"
    if 'width' in row and 'length' in row and pd.notna(row['width']) and pd.notna(row['length']):
        area_info += f" ({row['width']}m x {row['length']}m)"
    
    # Format transaction type
    transaction_type = row.get('transaction_type', 'Cần bán')
    
    # Format owner and agent info
    owner_info = f"Chủ nhà: {row.get('owner', 'N/A')}" if pd.notna(row.get('owner')) else ""
    agent_info = f"Môi giới: {row.get('agent_name', 'N/A')}" if pd.notna(row.get('agent_name')) else ""
    
    # Format phone
    phone_info = f"ĐT: {row.get('phone', 'N/A')}" if pd.notna(row.get('phone')) else ""
    
    # Create comprehensive text
    # Show both Gallery ID and Product ID if available
    id_display = f"Mã SP: {row['id']}"
    if 'product_id' in row and pd.notna(row['product_id']):
        id_display += f" (Mã sản phẩm: {row['product_id']})"
    
    text = f"""
    {id_display}
    Loại giao dịch: {transaction_type}
    Loại hình: {row['type']}
    Vị trí: {row['district']}, {row['ward']}
    Địa chỉ: {row['address']}
    Giá: {price_display}
    Diện tích: {area_info}
    Phòng ngủ: {row['bedrooms']}
    Hướng: {row['direction']}
    Pháp lý: {row['legal_status']}
    Tiện ích: {row['amenities']}
    {owner_info}
    {agent_info}
    {phone_info}
    Mô tả: {row['description']}
    """
    
    return text.strip()

def map_excel_columns(df):
    """Map Excel columns to expected format"""
    print("\n🔄 Attempting to map Excel columns to expected format...")
    
    # Common column mappings
    column_mappings = {
        # ID mappings
        'mã': 'id', 'mã sp': 'id', 'mã sản phẩm': 'id', 'product_id': 'id', 'id': 'id',
        
        # Type mappings
        'loại hình': 'type', 'loại': 'type', 'property_type': 'type', 'type': 'type',
        
        # Location mappings
        'quận': 'district', 'district': 'district',
        'phường': 'ward', 'ward': 'ward',
        'địa chỉ': 'address', 'address': 'address', 'địa chỉ đầy đủ': 'address',
        
        # Price mappings
        'giá': 'price', 'price': 'price', 'giá bán': 'price', 'sale_price': 'price',
        
        # Area mappings
        'diện tích': 'area', 'area': 'area', 'diện tích m2': 'area', 'square_meters': 'area',
        
        # Bedroom mappings
        'phòng ngủ': 'bedrooms', 'bedrooms': 'bedrooms', 'số phòng ngủ': 'bedrooms',
        
        # Direction mappings
        'hướng': 'direction', 'direction': 'direction', 'hướng nhà': 'direction',
        
        # Legal status mappings
        'pháp lý': 'legal_status', 'legal_status': 'legal_status', 'tình trạng pháp lý': 'legal_status',
        
        # Amenities mappings
        'tiện ích': 'amenities', 'amenities': 'amenities', 'facilities': 'amenities',
        
        # Description mappings
        'mô tả': 'description', 'description': 'description', 'chi tiết': 'description'
    }
    
    # Create a copy of the dataframe
    mapped_df = df.copy()
    
    # Try to map columns
    mapped_columns = {}
    for excel_col in df.columns:
        excel_col_lower = str(excel_col).lower().strip()
        
        # Check for exact matches first
        if excel_col_lower in column_mappings:
            mapped_columns[excel_col] = column_mappings[excel_col_lower]
            print(f"  ✅ Mapped '{excel_col}' → '{column_mappings[excel_col_lower]}'")
            continue
        
        # Check for partial matches
        for key, value in column_mappings.items():
            if key in excel_col_lower or excel_col_lower in key:
                mapped_columns[excel_col] = value
                print(f"  ✅ Mapped '{excel_col}' → '{value}' (partial match)")
                break
    
    # Rename columns
    if mapped_columns:
        mapped_df = mapped_df.rename(columns=mapped_columns)
        print(f"  📊 Successfully mapped {len(mapped_columns)} columns")
    else:
        print("  ⚠️ No columns could be automatically mapped")
    
    return mapped_df

# Khởi tạo vector store
def init_vector_store(df, source_type='sample'):
    """
    Initialize vector store with data
    
    Args:
        df: Processed DataFrame
        source_type: Source type for cache management
    """
    try:
        # Check if API key is set
        current_api_key = os.getenv('OPENAI_API_KEY')
        if not current_api_key or current_api_key == 'your_openai_api_key_here':
            raise ValueError("OpenAI API key is not set. Please enter your API key in the sidebar.")
        
        texts = df['text'].tolist()
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        
        # Create unique collection name based on source type
        collection_name = f"real_estate_{source_type}"
        
        vector_store = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            persist_directory=str(VECTOR_DB_DIR),
            collection_name=collection_name
        )
        
        return vector_store.as_retriever(search_kwargs={"k": TOP_K_RESULTS})
        
    except Exception as e:
        if "api_key" in str(e).lower():
            raise ValueError("OpenAI API key is not set or invalid. Please check your API key in the sidebar.")
        else:
            raise Exception(f"Error initializing vector store: {str(e)}")

# Tạo AI chain
def create_agent(source_type='sample', sheet_url=None, credentials_path=None, file_path=None):
    """
    Create AI agent with specified data source
    
    Args:
        source_type: Data source type ('sample', 'csv', 'excel', 'gsheet')
        sheet_url: Google Sheet URL (required for 'gsheet')
        credentials_path: Path to Google credentials (optional)
        file_path: Optional custom file path for csv/excel
    """
    try:
        # Check if API key is set
        current_api_key = os.getenv('OPENAI_API_KEY')
        if not current_api_key or current_api_key == 'your_openai_api_key_here':
            raise ValueError("OpenAI API key is not set. Please enter your API key in the sidebar.")
        
        # Load and process data
        df = load_and_process_data(source_type, sheet_url, credentials_path, file_path)
        
        # Initialize vector store
        retriever = init_vector_store(df, source_type)
        
        # Create prompt and LLM
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        llm = ChatOpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)
        
        # Create chain
        chain = (
            {"context": retriever, "question": RunnablePassthrough()} 
            | prompt 
            | llm 
            | StrOutputParser()
        )
        
        return chain, df
        
    except Exception as e:
        raise Exception(f"Error creating agent: {str(e)}")

# Khởi tạo default agent (for backward compatibility)
def get_default_agent():
    """Get default agent using sample data"""
    return create_agent(source_type='sample')