# 🚀 Real Estate AI Agent - Setup Guide

## Quick Start

### 1. **Activate Virtual Environment**

```bash
source venv/bin/activate
```

### 2. **Install Dependencies** (if not already installed)

```bash
pip install -r requirements.txt
```

### 3. **Set OpenAI API Key**

You have two options:

**Option A: Set in terminal**

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

**Option B: Set in .env file**
Create a `.env` file in the project root:

```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

### 4. **Run the Application**

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🎯 Using the App

### **Step 1: Select Data Source**

In the sidebar, choose:

- **"Production Excel (LandSoft)"** - for your real data
- **"Sample Data (CSV)"** - for testing

### **Step 2: Initialize Agent**

Click **"🔄 Khởi tạo Agent"** button

### **Step 3: Start Chatting**

Ask questions like:

- "Tìm nhà phố cần bán ở Quận 1"
- "Có căn hộ cho thuê nào ở Quận Bình Thạnh không?"
- "Tìm biệt thự giá dưới 10 tỷ"
- "Nhà nào có diện tích trên 100m²?"

## 📊 Your Data Overview

**LandSoft Data Statistics:**

- **100 properties** total
- **Price range:** 0 - 98,000,000,000 VND
- **Area range:** 0 - 467 m²
- **Property types:** 90 Nhà phố, 6 Căn hộ, 4 Biệt thự
- **Transaction types:** 98 Cần bán, 2 Cho thuê

**Top Districts:**

- Quận Bình Thạnh: 19 properties
- Quận Phú Nhuận: 14 properties
- Quận Bình Tân: 13 properties
- Quận 1: 12 properties

## 🔧 Troubleshooting

### **Issue: "ModuleNotFoundError: No module named 'streamlit.cli'"**

**Solution:**

```bash
pip install streamlit --upgrade
```

### **Issue: "The api_key client option must be set"**

**Solution:**
Set your OpenAI API key as shown in Step 3 above.

### **Issue: "Missing library: xlrd"**

**Solution:**

```bash
pip install xlrd openpyxl
```

### **Issue: App not loading**

**Solution:**

1. Make sure virtual environment is activated
2. Check if port 8501 is available
3. Try: `streamlit run app.py --server.port 8502`

## 🧪 Testing

### **Test Data Processing**

```bash
python test_excel_loading.py
```

### **Test LandSoft Analysis**

```bash
python analyze_landsoft_data.py
```

## 📁 File Structure

```
realestate-ai/
├── app.py                    # Main Streamlit application
├── ai_agent.py              # AI agent logic
├── utils/
│   ├── config.py            # Configuration
│   └── data_loader.py       # Data loading & LandSoft processing
├── data/
│   ├── sample_landsoft.xls  # Your real data
│   └── sample_real_estate.csv
├── venv/                    # Virtual environment
└── requirements.txt         # Dependencies
```

## 🎉 Success Indicators

✅ **App loads without errors**
✅ **"Production Excel (LandSoft)" option available**
✅ **Agent initializes successfully**
✅ **Can ask questions and get responses**
✅ **Responses include real property data**

## 💡 Tips

1. **First time:** Use "Sample Data" to test the interface
2. **Production:** Switch to "Production Excel (LandSoft)" for real data
3. **Questions:** Ask in Vietnamese for best results
4. **Specific queries:** Include district, price range, or property type
5. **Updates:** The app will automatically process your Excel file

## 🔄 Updating Data

To use new data:

1. Replace `data/sample_landsoft.xls` with your new file
2. Restart the app
3. Re-initialize the agent

The system will automatically process the new data and update the AI responses.
