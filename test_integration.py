#!/usr/bin/env python3
"""
Test script for Real Estate AI Agent integration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from ai_agent import create_agent, get_default_agent
        print("✅ AI Agent imports successful")
    except Exception as e:
        print(f"❌ AI Agent import failed: {e}")
        return False
    
    try:
        from utils.config import DATABASE_SOURCES, GOOGLE_CREDENTIALS_PATH
        print("✅ Config imports successful")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from utils.data_loader import load_data
        print("✅ Data loader imports successful")
    except Exception as e:
        print(f"❌ Data loader import failed: {e}")
        return False
    
    return True

def test_sample_data():
    """Test loading sample data"""
    print("\nTesting sample data loading...")
    
    try:
        from ai_agent import create_agent
        agent, df = create_agent(source_type='sample')
        print(f"✅ Sample data loaded successfully: {len(df)} records")
        print(f"   Columns: {list(df.columns)}")
        return True
    except Exception as e:
        print(f"❌ Sample data loading failed: {e}")
        return False

def test_google_sheets_setup():
    """Test Google Sheets setup (without actual connection)"""
    print("\nTesting Google Sheets setup...")
    
    # Check if credentials file exists
    creds_path = "credentials.json"
    if os.path.exists(creds_path):
        print(f"✅ Google credentials file found: {creds_path}")
    else:
        print(f"⚠️  Google credentials file not found: {creds_path}")
        print("   This is expected if you haven't set up Google Sheets yet")
    
    # Check if sheet URL is configured
    sheet_url = os.getenv('GOOGLE_SHEET_URL')
    if sheet_url:
        print(f"✅ Google Sheet URL configured: {sheet_url[:50]}...")
    else:
        print("⚠️  Google Sheet URL not configured (GOOGLE_SHEET_URL env var)")
    
    return True

def test_configuration():
    """Test configuration settings"""
    print("\nTesting configuration...")
    
    try:
        from utils.config import DATABASE_SOURCES, EMBEDDING_MODEL, LLM_MODEL
        
        print(f"✅ Database sources configured: {list(DATABASE_SOURCES.keys())}")
        print(f"✅ Embedding model: {EMBEDDING_MODEL}")
        print(f"✅ LLM model: {LLM_MODEL}")
        
        # Check OpenAI API key
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print(f"✅ OpenAI API key configured: {api_key[:10]}...")
        else:
            print("⚠️  OpenAI API key not configured (OPENAI_API_KEY env var)")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Real Estate AI Agent Integration Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_configuration,
        test_sample_data,
        test_google_sheets_setup
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\nNext steps:")
        print("1. Set up Google Sheets integration (see GOOGLE_SHEETS_SETUP.md)")
        print("2. Configure your OpenAI API key")
        print("3. Run: streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
