import os
from pathlib import Path

# ---------- Path Config ----------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
VECTOR_DB_DIR = BASE_DIR / 'chroma_db'

# File paths
SAMPLE_DATA_PATH = DATA_DIR / 'sample_real_estate.csv'
PRODUCTION_DATA_PATH = DATA_DIR / 'production_data.csv'  # Cho giai đoạn sau
EXCEL_DATA_PATH = DATA_DIR / 'sample_landsoft.xls'  # Excel file path

# ---------- Google Sheets Config ----------
GOOGLE_CREDENTIALS_PATH = BASE_DIR / 'credentials.json'
DEFAULT_SHEET_URL = os.getenv('GOOGLE_SHEET_URL', '')  # Set via environment variable

# ---------- Database Sources ----------
DATABASE_SOURCES = {
    'sample': {
        'name': 'Sample Data (CSV)',
        'type': 'sample',
        'description': 'Local sample data for testing'
    },
    'csv': {
        'name': 'Production CSV',
        'type': 'csv', 
        'description': 'Local production CSV file'
    },
    'excel': {
        'name': 'Production Excel',
        'type': 'excel',
        'description': 'Local production Excel file (.xls/.xlsx)'
    },
    'gsheet': {
        'name': 'Google Sheets',
        'type': 'gsheet',
        'description': 'Live data from Google Sheets',
        'requires_url': True
    }
}

# ---------- AI Model Config ----------
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.1  # Độ sáng tạo của AI

# ---------- Application Config ----------
TOP_K_RESULTS = 3  # Số lượng sản phẩm trả về
MAX_INPUT_LENGTH = 500  # Độ dài tối đa của câu hỏi

# ---------- Prompt Templates ----------
PROMPT_TEMPLATE = """
    Bạn là chuyên gia bất động sản tại TP.HCM. Hãy sử dụng thông tin sau để trả lời câu hỏi:
    {context}
    
    Câu hỏi: {question}
    
    **Nguyên tắc đề xuất:**
    - Chỉ đề xuất tối đa 3 sản phẩm phù hợp nhất
    - Luôn hiển thị Mã SP, Giá, Diện tích và Vị trí
    - Giải thích ngắn gọn lý do phù hợp
    - Nếu không có sản phẩm phù hợp, hãy đề xuất tiêu chí thay thế
    """

# ---------- District Mapping ----------
DISTRICT_ALIASES = {
    "q1": "Quận 1",
    "q3": "Quận 3",
    "thuduc": "Quận Thủ Đức",
    "binhthanh": "Quận Bình Thạnh",
    "govap": "Quận Gò Vấp",
    "trungtam": ["Quận 1", "Quận 3", "Quận 4"]
}

# ---------- Security Config ----------
ALLOWED_DOMAINS = ["company-domain.com"]  # Cho giai đoạn sau