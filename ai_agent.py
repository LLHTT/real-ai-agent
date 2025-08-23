import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from utils.config import *
from utils.data_loader import load_data

# Load env
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Load và xử lý dữ liệu
def load_and_process_data(source_type='sample', sheet_url=None, credentials_path=None):
    """
    Load and process data from different sources
    
    Args:
        source_type: 'sample', 'csv', or 'gsheet'
        sheet_url: Required for 'gsheet' type
        credentials_path: Path to Google credentials (optional, uses default if None)
    """
    try:
        # Load data from source
        if source_type == 'gsheet':
            if not sheet_url:
                raise ValueError("Sheet URL is required for Google Sheets source")
            creds_path = credentials_path or str(GOOGLE_CREDENTIALS_PATH)
            df = load_data(source_type='gsheet', sheet_url=sheet_url, credentials_path=creds_path)
        else:
            df = load_data(source_type=source_type)
        
        # Validate required columns
        required_columns = ['id', 'type', 'district', 'ward', 'address', 'price', 'area', 'bedrooms', 'direction', 'legal_status', 'amenities', 'description']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Tạo text embedding cho mỗi sản phẩm
        df['text'] = df.apply(lambda row: f"""
        Mã SP: {row['id']}
        Loại hình: {row['type']}
        Vị trí: {row['district']}, {row['ward']}
        Địa chỉ: {row['address']}
        Giá: {row['price']:,.0f} VND
        Diện tích: {row['area']}m²
        Phòng ngủ: {row['bedrooms']}
        Hướng: {row['direction']}
        Pháp lý: {row['legal_status']}
        Tiện ích: {row['amenities']}
        Mô tả: {row['description']}
        """, axis=1)
        
        return df
        
    except Exception as e:
        raise Exception(f"Error loading data from {source_type}: {str(e)}")

# Khởi tạo vector store
def init_vector_store(df, source_type='sample'):
    """
    Initialize vector store with data
    
    Args:
        df: Processed DataFrame
        source_type: Source type for cache management
    """
    try:
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
        raise Exception(f"Error initializing vector store: {str(e)}")

# Tạo AI chain
def create_agent(source_type='sample', sheet_url=None, credentials_path=None):
    """
    Create AI agent with specified data source
    
    Args:
        source_type: Data source type ('sample', 'csv', 'gsheet')
        sheet_url: Google Sheet URL (required for 'gsheet')
        credentials_path: Path to Google credentials (optional)
    """
    try:
        # Load and process data
        df = load_and_process_data(source_type, sheet_url, credentials_path)
        
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
    try:
        agent, df = create_agent(source_type='sample')
        return agent
    except Exception as e:
        print(f"Warning: Could not create default agent: {e}")
        return None

# Global agent instance (will be updated based on user selection)
real_estate_agent = get_default_agent()