#!/usr/bin/env python3
"""
Test script for Excel file loading and LandSoft data processing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_excel_loading():
    """Test loading the Excel file"""
    print("🔍 Testing Excel file loading...")
    
    try:
        from utils.data_loader import load_data, analyze_data_structure, process_landsoft_data
        
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

def test_landsoft_processing():
    """Test LandSoft data processing"""
    print("\n🔄 Testing LandSoft data processing...")
    
    try:
        from utils.data_loader import load_data, process_landsoft_data
        
        # Load raw Excel data
        raw_df = load_data(source_type='excel')
        
        # Process LandSoft data
        processed_df = process_landsoft_data(raw_df)
        
        print(f"✅ LandSoft data processing successful!")
        print(f"📊 Processed shape: {processed_df.shape}")
        print(f"📋 Processed columns: {list(processed_df.columns)}")
        
        # Check key processed fields
        print(f"\n🔍 Key processed fields:")
        print(f"   - ID format: {processed_df['id'].iloc[0] if len(processed_df) > 0 else 'N/A'}")
        print(f"   - Price range: {processed_df['price'].min():,.0f} - {processed_df['price'].max():,.0f} VND")
        print(f"   - Property types: {processed_df['type'].value_counts().to_dict()}")
        print(f"   - Transaction types: {processed_df['transaction_type'].value_counts().to_dict()}")
        
        # Show sample processed record
        if len(processed_df) > 0:
            print(f"\n📄 Sample processed record:")
            sample = processed_df.iloc[0]
            print(f"   ID: {sample['id']}")
            print(f"   Type: {sample['type']}")
            print(f"   Transaction: {sample['transaction_type']}")
            print(f"   Address: {sample['address']}")
            print(f"   Price: {sample['price']:,.0f} VND")
            print(f"   Area: {sample['area']}m²")
        
        return True
        
    except Exception as e:
        print(f"❌ LandSoft processing error: {e}")
        return False

def test_ai_agent_integration():
    """Test AI agent with LandSoft data"""
    print("\n🤖 Testing AI agent integration...")
    
    try:
        from ai_agent import create_agent
        
        # Create agent with Excel data
        agent, df = create_agent(source_type='excel')
        
        print(f"✅ AI agent created successfully!")
        print(f"📊 Agent loaded {len(df)} records")
        
        # Test a simple query
        test_query = "Tìm căn hộ cho thuê ở Quận 1"
        print(f"\n🧪 Testing query: '{test_query}'")
        
        response = agent.invoke(test_query)
        print(f"✅ Agent response received (length: {len(response)} characters)")
        
        return True
        
    except Exception as e:
        print(f"❌ AI agent integration error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running comprehensive Excel and LandSoft tests...")
    print("=" * 60)
    
    # Test 1: Basic Excel loading
    test1_success = test_excel_loading()
    
    # Test 2: LandSoft processing
    test2_success = test_landsoft_processing()
    
    # Test 3: AI agent integration
    test3_success = test_ai_agent_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print(f"   Excel Loading: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"   LandSoft Processing: {'✅ PASS' if test2_success else '❌ FAIL'}")
    print(f"   AI Agent Integration: {'✅ PASS' if test3_success else '❌ FAIL'}")
    
    if all([test1_success, test2_success, test3_success]):
        print("\n🎉 All tests passed! LandSoft integration is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        sys.exit(1)
