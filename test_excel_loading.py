#!/usr/bin/env python3
"""
Test script for Excel file loading
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_excel_loading():
    """Test loading the Excel file"""
    print("�� Testing Excel file loading...")
    
    try:
        from utils.data_loader import load_data, analyze_data_structure
        
        # Test loading Excel file
        df = load_data(source_type='excel')
        
        print(f"✅ Excel file loaded successfully!")
        print(f"📊 Shape: {df.shape}")
        print(f"📋 Columns: {list(df.columns)}")
        
        # Analyze structure
        missing_columns = analyze_data_structure(df, 'excel')
        
        if missing_columns:
            print(f"\n⚠️ Missing columns: {missing_columns}")
            print("💡 The system will attempt to map columns automatically")
        else:
            print(f"\n✅ All required columns are present!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Missing library: {e}")
        print("💡 Install required library:")
        if "xlrd" in str(e):
            print("   pip install xlrd")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_excel_loading()
    if success:
        print("\n�� Excel loading test passed!")
    else:
        print("\n❌ Excel loading test failed!")
        sys.exit(1)
