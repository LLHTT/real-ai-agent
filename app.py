import os
import streamlit as st
from ai_agent import create_agent, get_default_agent
from utils.config import DATABASE_SOURCES, DEFAULT_SHEET_URL
import time

# Cấu hình trang
st.set_page_config(page_title="RealEstate AI Agent", layout="wide")
st.title("🏠 AI Trợ lý Bất động sản TP.HCM")
st.subheader("Tìm sản phẩm phù hợp trong 3 giây")

# Sidebar
with st.sidebar:
    st.header("Cài đặt")
    
    # OpenAI API Key
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    
    st.divider()
    
    # Database Source Selection
    st.subheader("📊 Nguồn dữ liệu")
    
    # Create source options for selectbox
    source_options = {f"{key} - {value['name']}": key for key, value in DATABASE_SOURCES.items()}
    selected_source_display = st.selectbox(
        "Chọn nguồn dữ liệu:",
        options=list(source_options.keys()),
        index=0
    )
    selected_source = source_options[selected_source_display]
    
    # Show source description
    source_info = DATABASE_SOURCES[selected_source]
    st.info(f"**{source_info['name']}**\n{source_info['description']}")
    
    # Google Sheets specific settings
    sheet_url = None
    if selected_source == 'gsheet':
        st.subheader("🔗 Google Sheets")
        sheet_url = st.text_input(
            "Google Sheet URL:",
            value=DEFAULT_SHEET_URL,
            help="Paste the full URL of your Google Sheet"
        )
        
        if not sheet_url:
            st.warning("⚠️ Vui lòng nhập Google Sheet URL để sử dụng dữ liệu từ Google Sheets")
        
        # Check for credentials file
        credentials_path = "credentials.json"
        if not os.path.exists(credentials_path):
            st.error("❌ Không tìm thấy file credentials.json")
            st.info("""
            **Để sử dụng Google Sheets:**
            1. Tạo Service Account trong Google Cloud Console
            2. Tải file credentials.json
            3. Đặt file vào thư mục gốc của dự án
            4. Chia sẻ Google Sheet với email của Service Account
            """)
    
    st.divider()
    
    # Initialize/Update Agent Button
    if st.button("🔄 Khởi tạo Agent", type="primary"):
        if selected_source == 'gsheet' and not sheet_url:
            st.error("Vui lòng nhập Google Sheet URL")
        else:
            with st.spinner("Đang khởi tạo AI Agent..."):
                try:
                    # Create new agent
                    agent, df = create_agent(
                        source_type=selected_source,
                        sheet_url=sheet_url
                    )
                    
                    # Store in session state
                    st.session_state.agent = agent
                    st.session_state.data_source = selected_source
                    st.session_state.dataframe = df
                    
                    st.success(f"✅ Agent đã được khởi tạo với {len(df)} sản phẩm từ {source_info['name']}")
                    
                except Exception as e:
                    st.error(f"❌ Lỗi khởi tạo agent: {str(e)}")
    
    st.divider()
    
    # Usage Instructions
    st.info("""
    **Hướng dẫn sử dụng:**
    - Chọn nguồn dữ liệu phù hợp
    - Nhấn "Khởi tạo Agent" để cập nhật
    - Nhập nhu cầu khách hàng bằng tiếng Việt tự nhiên
    - Ví dụ: 
      "Cần nhà phố Quận 7 giá dưới 20 tỷ, 3 phòng ngủ"
      "Tìm căn hộ trung tâm có hồ bơi, giá 5-8 tỷ"
    """)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = get_default_agent()
if "data_source" not in st.session_state:
    st.session_state.data_source = 'sample'

# Display current data source
try:
    if st.session_state.data_source and st.session_state.data_source in DATABASE_SOURCES:
        source_info = DATABASE_SOURCES[st.session_state.data_source]
        st.info(f"📊 **Nguồn dữ liệu hiện tại:** {source_info['name']}")
except:
    pass  # Ignore session state errors when not running in Streamlit

# Chat interface
try:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Nhập nhu cầu khách hàng..."):
        # Check if agent is available
        if st.session_state.agent is None:
            st.error("❌ Agent chưa được khởi tạo. Vui lòng chọn nguồn dữ liệu và nhấn 'Khởi tạo Agent'")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Xử lý với AI agent
                try:
                    start_time = time.time()
                    response = st.session_state.agent.invoke(prompt)
                    processing_time = time.time() - start_time
                    
                    # Hiển thị từng từ với hiệu ứng gõ
                    for chunk in response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                    st.caption(f"⏱️ Thời gian xử lý: {processing_time:.2f}s")
                    
                except Exception as e:
                    st.error(f"Lỗi: {str(e)}")
                    full_response = f"Xin lỗi, có lỗi xảy ra: {str(e)}"
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
except:
    pass  # Ignore session state errors when not running in Streamlit