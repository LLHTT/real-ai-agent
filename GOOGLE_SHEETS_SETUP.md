# Google Sheets Integration Setup

## Overview

This guide will help you set up Google Sheets as a data source for the Real Estate AI Agent.

## Prerequisites

- Google Cloud Platform account
- Google Sheets with real estate data
- Python environment with required packages

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

## Step 2: Create Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in service account details:
   - Name: `real-estate-ai-agent`
   - Description: `Service account for Real Estate AI Agent`
4. Click "Create and Continue"
5. Skip role assignment (click "Continue")
6. Click "Done"

## Step 3: Generate Credentials

1. Click on your newly created service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create new key"
4. Select "JSON" format
5. Click "Create"
6. Download the JSON file and rename it to `credentials.json`
7. Place it in the root directory of this project

## Step 4: Prepare Google Sheet

Your Google Sheet should have the following columns:

- `id` - Gallery ID (sequential number: 1, 2, 3, ...)
- `product_id` - Product ID (Mã sản phẩm, e.g., "SP001", "NH002")
- `type` - Property type (e.g., "Căn hộ", "Nhà phố")
- `district` - District name
- `ward` - Ward name
- `address` - Full address
- `price` - Price in VND (numeric)
- `area` - Area in m² (numeric)
- `bedrooms` - Number of bedrooms (numeric)
- `direction` - Direction (e.g., "Đông", "Tây")
- `legal_status` - Legal status
- `amenities` - Amenities list
- `description` - Property description

## Step 5: Share Google Sheet

1. Open your Google Sheet
2. Click "Share" button
3. Add your service account email (found in credentials.json)
4. Give "Editor" permissions
5. Copy the sheet URL

## Step 6: Configure Environment

1. Set the Google Sheet URL as environment variable:

   ```bash
   export GOOGLE_SHEET_URL="https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
   ```

2. Or add to your `.env` file:
   ```
   GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit
   ```

## Step 7: Test Integration

1. Run the application:

   ```bash
   streamlit run app.py
   ```

2. In the sidebar:
   - Select "Google Sheets" as data source
   - Enter your Google Sheet URL
   - Click "Khởi tạo Agent"

## Troubleshooting

### Common Issues:

1. **"File not found" error for credentials.json**

   - Ensure credentials.json is in the project root directory
   - Check file permissions

2. **"Access denied" error**

   - Verify service account email has access to the sheet
   - Check sheet sharing permissions

3. **"Missing columns" error**

   - Ensure your sheet has all required columns
   - Check column names match exactly

4. **"Invalid URL" error**
   - Use the full Google Sheets URL
   - Ensure the sheet is shared with service account

### Security Notes:

- Never commit credentials.json to version control
- Add `credentials.json` to your `.gitignore` file
- Use environment variables for sensitive data
- Regularly rotate service account keys

## Example Google Sheet Structure

| id  | product_id | type    | district | ward        | address        | price       | area | bedrooms | direction | legal_status | amenities   | description         |
| --- | ---------- | ------- | -------- | ----------- | -------------- | ----------- | ---- | -------- | --------- | ------------ | ----------- | ------------------- |
| 1   | SP001      | Căn hộ  | Quận 7   | Phú Mỹ Hưng | 123 ABC Street | 5000000000  | 80   | 2        | Đông      | Sổ hồng      | Hồ bơi, Gym | Căn hộ cao cấp...   |
| 2   | NH002      | Nhà phố | Quận 1   | Bến Nghé    | 456 XYZ Street | 15000000000 | 120  | 4        | Tây       | Sổ hồng      | Sân thượng  | Nhà phố mặt tiền... |
