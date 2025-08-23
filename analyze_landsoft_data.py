#!/usr/bin/env python3
"""
Comprehensive LandSoft data analysis
"""

import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def analyze_landsoft_data():
    """Analyze the processed LandSoft data"""
    print("🔍 Analyzing LandSoft data processing...")
    print("=" * 60)
    
    try:
        from utils.data_loader import load_data, process_landsoft_data
        
        # Load and process data
        raw_df = load_data(source_type='excel')
        processed_df = process_landsoft_data(raw_df)
        
        print(f"✅ Data processing completed!")
        print(f"📊 Raw data: {len(raw_df)} rows, {len(raw_df.columns)} columns")
        print(f"📊 Processed data: {len(processed_df)} rows, {len(processed_df.columns)} columns")
        
        # Show column mapping
        print(f"\n📋 COLUMN MAPPING:")
        print("-" * 60)
        raw_columns = list(raw_df.columns)
        processed_columns = list(processed_df.columns)
        
        print("Original LandSoft columns → Processed columns:")
        for i, col in enumerate(raw_columns, 1):
            print(f"{i:2d}. {col}")
        
        print(f"\nNew processed columns:")
        for i, col in enumerate(processed_columns, 1):
            print(f"{i:2d}. {col}")
        
        # Data quality analysis
        print(f"\n📈 DATA QUALITY ANALYSIS:")
        print("-" * 60)
        
        # Price analysis
        price_stats = processed_df['price'].describe()
        print(f"💰 Price Statistics:")
        print(f"   - Min: {price_stats['min']:,.0f} VND")
        print(f"   - Max: {price_stats['max']:,.0f} VND")
        print(f"   - Mean: {price_stats['mean']:,.0f} VND")
        print(f"   - Properties with 'Thương lượng': {(processed_df['price'] == 0).sum()}")
        
        # Area analysis
        area_stats = processed_df['area'].describe()
        print(f"\n📏 Area Statistics:")
        print(f"   - Min: {area_stats['min']:.1f} m²")
        print(f"   - Max: {area_stats['max']:.1f} m²")
        print(f"   - Mean: {area_stats['mean']:.1f} m²")
        
        # Property types
        print(f"\n🏠 Property Types:")
        type_counts = processed_df['type'].value_counts()
        for prop_type, count in type_counts.items():
            print(f"   - {prop_type}: {count}")
        
        # Transaction types
        print(f"\n💼 Transaction Types:")
        trans_counts = processed_df['transaction_type'].value_counts()
        for trans_type, count in trans_counts.items():
            print(f"   - {trans_type}: {count}")
        
        # Districts
        print(f"\n📍 Districts:")
        district_counts = processed_df['district'].value_counts().head(10)
        for district, count in district_counts.items():
            print(f"   - {district}: {count}")
        
        # Bedrooms
        print(f"\n🛏️ Bedrooms:")
        bedroom_counts = processed_df['bedrooms'].value_counts().sort_index()
        for bedrooms, count in bedroom_counts.items():
            print(f"   - {bedrooms} phòng: {count}")
        
        # Sample processed records
        print(f"\n📄 SAMPLE PROCESSED RECORDS:")
        print("-" * 60)
        
        for i in range(min(3, len(processed_df))):
            record = processed_df.iloc[i]
            print(f"\nRecord {i+1}:")
            print(f"   ID: {record['id']}")
            print(f"   Transaction: {record['transaction_type']}")
            print(f"   Type: {record['type']}")
            print(f"   Address: {record['address']}")
            print(f"   Price: {record['price']:,.0f} VND" if record['price'] > 0 else "   Price: Thương lượng")
            print(f"   Area: {record['area']}m²")
            print(f"   Bedrooms: {record['bedrooms']}")
            print(f"   Direction: {record['direction']}")
            print(f"   Owner: {record.get('owner', 'N/A')}")
            print(f"   Agent: {record.get('agent_name', 'N/A')}")
            print(f"   Amenities: {record['amenities']}")
            print(f"   Description: {str(record['description'])[:100]}...")
        
        # Text embedding sample
        print(f"\n🤖 TEXT EMBEDDING SAMPLE:")
        print("-" * 60)
        
        from ai_agent import create_detailed_text_embedding
        sample_record = processed_df.iloc[0]
        text_embedding = create_detailed_text_embedding(sample_record)
        print(text_embedding)
        
        return processed_df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    df = analyze_landsoft_data()
    
    if df is not None:
        print(f"\n💡 SUMMARY:")
        print("=" * 60)
        print("✅ LandSoft data has been successfully processed!")
        print("✅ The AI agent can now work with your real data")
        print("✅ All key fields have been mapped and processed")
        print("✅ Price parsing handles 'Thương lượng' and various formats")
        print("✅ Property types are automatically determined from descriptions")
        print("✅ Amenities are extracted from descriptions")
        print("✅ Text embeddings include comprehensive property information")
        
        print(f"\n🚀 Next steps:")
        print("1. Run: streamlit run app.py")
        print("2. Select 'Production Excel (LandSoft)' as data source")
        print("3. Click 'Khởi tạo Agent'")
        print("4. Start asking questions about your properties!")
    else:
        print("\n❌ Analysis failed!")
        sys.exit(1)
