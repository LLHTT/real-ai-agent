import os
import streamlit as st
from ai_agent import create_agent
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
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key to enable AI features")
    
    # Set API key in environment if provided
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.success("✅ API Key set successfully!")
    else:
        st.warning("⚠️ Please enter your OpenAI API key to use the AI agent")
    
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
    
    # File upload for CSV/Excel
    file_path = None
    if selected_source in ['csv', 'excel']:
        st.subheader("📁 Upload File")
        uploaded_file = st.file_uploader(
            f"Upload {selected_source.upper()} file:",
            type=['csv', 'xls', 'xlsx'] if selected_source == 'excel' else ['csv'],
            help=f"Upload your {selected_source.upper()} file here"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{selected_source}') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                file_path = tmp_file.name
            
            st.success(f"✅ File uploaded: {uploaded_file.name}")
    
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
        # Check if API key is provided
        if not api_key:
            st.error("❌ Vui lòng nhập OpenAI API Key trước khi khởi tạo Agent")
        elif selected_source == 'gsheet' and not sheet_url:
            st.error("Vui lòng nhập Google Sheet URL")
        elif selected_source in ['csv', 'excel'] and not file_path:
            st.error(f"Vui lòng upload file {selected_source.upper()}")
        else:
            with st.spinner("Đang khởi tạo AI Agent..."):
                try:
                    # Create new agent
                    agent, df = create_agent(
                        source_type=selected_source,
                        sheet_url=sheet_url,
                        file_path=file_path
                    )
                    
                    # Store in session state
                    st.session_state.agent = agent
                    st.session_state.data_source = selected_source
                    st.session_state.dataframe = df
                    st.session_state.api_key_set = True
                    
                    st.success(f"✅ Agent đã được khởi tạo với {len(df)} sản phẩm từ {source_info['name']}")
                    
                except Exception as e:
                    st.error(f"❌ Lỗi khởi tạo agent: {str(e)}")
                    if "api_key" in str(e).lower():
                        st.info("💡 Hãy kiểm tra lại OpenAI API Key của bạn")
    
    st.divider()
    
    # Usage Instructions
    st.info("""
    **💡 Cách sử dụng:**
    1. Nhập OpenAI API Key
    2. Chọn nguồn dữ liệu phù hợp
    3. Upload file hoặc nhập URL Google Sheets
    4. Nhấn "Khởi tạo Agent"
    5. Bắt đầu chat với AI
    """)

# Main chat interface
if 'agent' not in st.session_state or not st.session_state.get('api_key_set', False):
    st.info("""
    🚀 **Chào mừng đến với AI Trợ lý Bất động sản!**
    
    **Để bắt đầu:**
    1. Nhập **OpenAI API Key** ở sidebar bên trái
    2. Chọn **nguồn dữ liệu** (khuyến nghị: "Production Excel (LandSoft)")
    3. Nhấn **"🔄 Khởi tạo Agent"**
    4. Bắt đầu **chat** với AI!
    
    **💡 Không có API Key?**
    - Đăng ký tại [OpenAI Platform](https://platform.openai.com/)
    - Tạo API key mới
    - Copy và paste vào ô "OpenAI API Key"
    """)
else:
    # Chat interface
    st.subheader("💬 Chat với AI")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Get response from agent
                response = st.session_state.agent.invoke(prompt)
                
                # Simulate streaming response
                for chunk in response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
            except Exception as e:
                message_placeholder.error(f"❌ Lỗi: {str(e)}")
                full_response = f"Xin lỗi, có lỗi xảy ra: {str(e)}"
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🏠 Real Estate AI Agent - Powered by OpenAI & LangChain</p>
</div>
""", unsafe_allow_html=True)