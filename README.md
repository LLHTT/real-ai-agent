# 🏠 Real Estate AI Agent

An intelligent AI assistant for real estate property search in Ho Chi Minh City, Vietnam. The system can work with multiple data sources including local CSV files and Google Sheets.

## ✨ Features

- **Multi-Source Data Support**: Choose from sample data, local CSV files, or live Google Sheets
- **Intelligent Property Search**: Natural language queries in Vietnamese
- **Real-time Recommendations**: AI-powered property suggestions based on user requirements
- **Modern Web Interface**: Beautiful Streamlit-based UI with chat interface
- **Vector Search**: Advanced semantic search using OpenAI embeddings

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 2. Set Up Environment

Create a `.env` file in the project root:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional - for Google Sheets integration
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit
```

### 3. Run the Application

```bash
streamlit run app.py
```

## 📊 Data Sources

The application supports three data sources:

### 1. Sample Data (Default)

- Pre-loaded sample data for testing
- No additional setup required
- Good for initial testing and development

### 2. Local CSV Files

- Place your CSV file in the `data/` directory
- Ensure it has the required columns (see Data Format section)
- Select "Production CSV" in the app

### 3. Google Sheets (Recommended for Production)

- Live data from Google Sheets
- Real-time updates
- Collaborative editing
- See [Google Sheets Setup Guide](GOOGLE_SHEETS_SETUP.md) for detailed instructions

## 📋 Data Format

Your data source must include these columns:

| Column         | Type    | Description                    | Example             |
| -------------- | ------- | ------------------------------ | ------------------- |
| `id`           | string  | Gallery ID (sequential number) | "1", "2", "3"       |
| `product_id`   | string  | Product ID (Mã sản phẩm)       | "SP001", "NH002"    |
| `type`         | string  | Property type                  | "Căn hộ", "Nhà phố" |
| `district`     | string  | District name                  | "Quận 7"            |
| `ward`         | string  | Ward name                      | "Phú Mỹ Hưng"       |
| `address`      | string  | Full address                   | "123 ABC Street"    |
| `price`        | numeric | Price in VND                   | 5000000000          |
| `area`         | numeric | Area in m²                     | 80                  |
| `bedrooms`     | numeric | Number of bedrooms             | 2                   |
| `direction`    | string  | Direction                      | "Đông", "Tây"       |
| `legal_status` | string  | Legal status                   | "Sổ hồng"           |
| `amenities`    | string  | Amenities list                 | "Hồ bơi, Gym"       |
| `description`  | string  | Property description           | "Căn hộ cao cấp..." |

## 🔧 Configuration

### AI Models

- **Embedding Model**: `text-embedding-3-small` (OpenAI)
- **LLM Model**: `gpt-4o-mini` (OpenAI)
- **Temperature**: 0.1 (for consistent responses)

### Search Settings

- **Top K Results**: 3 properties per query
- **Max Input Length**: 500 characters

## 🧪 Testing

Run the integration test to verify your setup:

```bash
python test_integration.py
```

This will test:

- ✅ All imports and dependencies
- ✅ Configuration settings
- ✅ Sample data loading
- ✅ Google Sheets setup (if configured)

## 📁 Project Structure

```
realestate-ai/
├── app.py                 # Main Streamlit application
├── ai_agent.py           # AI agent and vector store logic
├── utils/
│   ├── config.py         # Configuration settings
│   └── data_loader.py    # Data loading utilities
├── data/                 # Local data files
├── chroma_db/           # Vector database storage
├── credentials.json     # Google Sheets credentials (if using)
├── requirements.txt     # Python dependencies
├── GOOGLE_SHEETS_SETUP.md # Google Sheets setup guide
└── test_integration.py  # Integration test script
```

## 🔐 Security

- Never commit `credentials.json` to version control
- Use environment variables for sensitive data
- Regularly rotate API keys and service account credentials
- The `.gitignore` file is configured to exclude sensitive files

## 🆘 Troubleshooting

### Common Issues

1. **"Agent not initialized" error**

   - Select a data source in the sidebar
   - Click "Khởi tạo Agent" button

2. **Google Sheets connection failed**

   - Verify credentials.json exists and is valid
   - Check that the sheet is shared with your service account
   - Ensure the sheet has the required columns

3. **Missing columns error**

   - Verify your data source has all required columns
   - Check column names match exactly (case-sensitive)

4. **OpenAI API errors**
   - Verify your API key is correct and has sufficient credits
   - Check your OpenAI account status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section above
2. Review the Google Sheets setup guide
3. Run the integration test script
4. Create an issue in the repository

---

**Happy property hunting! 🏠✨**
