# scripts/generate_sample_data.py
import pandas as pd
import random
from faker import Faker
import os

def generate_real_estate_data(num_records=30):
    fake = Faker('vi_VN')
    
    # Real Ho Chi Minh City districts and wards
    district_wards = {
        'Quận 1': ['Phường Bến Nghé', 'Phường Bến Thành', 'Phường Cầu Kho', 'Phường Cầu Ông Lãnh', 
                   'Phường Đa Kao', 'Phường Nguyễn Cư Trinh', 'Phường Nguyễn Thái Bình', 'Phường Phạm Ngũ Lão', 
                   'Phường Tân Định'],
        'Quận 3': ['Phường 1', 'Phường 2', 'Phường 3', 'Phường 4', 'Phường 5', 'Phường 6', 'Phường 7', 'Phường 8', 'Phường 9', 'Phường 10', 'Phường 11', 'Phường 12', 'Phường 13', 'Phường 14'],
        'Quận 7': ['Phường Bình Thuận', 'Phường Phú Mỹ', 'Phường Phú Thuận', 'Phường Tân Hưng', 
                   'Phường Tân Kiểng', 'Phường Tân Phong', 'Phường Tân Phú', 'Phường Tân Quy', 'Phường Tân Thuận Đông', 'Phường Tân Thuận Tây'],
        'Quận Bình Thạnh': ['Phường 1', 'Phường 2', 'Phường 3', 'Phường 5', 'Phường 6', 'Phường 7', 'Phường 11', 'Phường 12', 'Phường 13', 'Phường 14', 'Phường 15', 'Phường 17', 'Phường 19', 'Phường 21', 'Phường 22', 'Phường 24', 'Phường 25', 'Phường 26', 'Phường 27', 'Phường 28'],
        'Quận Gò Vấp': ['Phường 1', 'Phường 3', 'Phường 4', 'Phường 5', 'Phường 6', 'Phường 7', 'Phường 8', 'Phường 9', 'Phường 10', 'Phường 11', 'Phường 12', 'Phường 13', 'Phường 14', 'Phường 15', 'Phường 16', 'Phường 17'],
        'Quận Thủ Đức': ['Phường An Khánh', 'Phường An Lạc', 'Phường An Lạc A', 'Phường An Phú', 'Phường Bình Chiểu', 'Phường Bình Thọ', 'Phường Hiệp Bình Chánh', 'Phường Hiệp Bình Phước', 'Phường Linh Chiểu', 'Phường Linh Đông', 'Phường Linh Tây', 'Phường Linh Trung', 'Phường Linh Xuân', 'Phường Long Bình', 'Phường Long Phước', 'Phường Long Thạnh Mỹ', 'Phường Long Trường', 'Phường Phú Hữu', 'Phường Phước Bình', 'Phường Phước Long A', 'Phường Phước Long B', 'Phường Tam Bình', 'Phường Tam Phú', 'Phường Tăng Nhơn Phú A', 'Phường Tăng Nhơn Phú B', 'Phường Tân Phú', 'Phường Trường Thạnh', 'Phường Trường Thọ']
    }
    
    property_types = ['Căn hộ', 'Nhà phố', 'Biệt thự', 'Shophouse', 'Văn phòng']
    
    # Realistic property descriptions
    descriptions = [
        "Căn hộ cao cấp với thiết kế hiện đại, view đẹp, tiện ích đầy đủ. Vị trí thuận lợi, giao thông thuận tiện.",
        "Nhà phố mặt tiền đường lớn, kinh doanh tốt, phù hợp mở shop hoặc văn phòng. Diện tích sử dụng rộng rãi.",
        "Biệt thự sang trọng với thiết kế độc đáo, sân vườn rộng, không gian sống thoáng đãng. An ninh 24/7.",
        "Shophouse mới xây, thiết kế đẹp, vị trí đắc địa. Phù hợp kinh doanh hoặc cho thuê văn phòng.",
        "Căn hộ trung cấp giá tốt, tiện ích cơ bản đầy đủ. Phù hợp gia đình trẻ, sinh viên.",
        "Nhà phố hẻm xe hơi, yên tĩnh, an ninh tốt. Gần trường học, bệnh viện, siêu thị.",
        "Căn hộ view sông, không khí trong lành. Thiết kế tối ưu, tiết kiệm năng lượng.",
        "Biệt thự mini với sân thượng rộng, view thành phố. Phù hợp gia đình nhỏ.",
        "Văn phòng cho thuê tại tòa nhà văn phòng cao cấp. Vị trí trung tâm, giao thông thuận tiện.",
        "Căn hộ studio giá rẻ, phù hợp người độc thân hoặc sinh viên. Gần trường đại học."
    ]
    
    # Realistic amenities
    amenities_list = [
        "Hồ bơi, Gym, An ninh 24/7",
        "Thang máy, Chỗ đậu xe, Sân chơi trẻ em",
        "Gần trường học, Siêu thị, Bệnh viện",
        "Công viên gần đó, Nhà hàng, Cafe",
        "Trung tâm thương mại, Bến xe buýt, Metro",
        "Sân tennis, BBQ area, Garden",
        "Gym, Spa, Restaurant",
        "Playground, Library, Business center",
        "Swimming pool, Sauna, Conference room",
        "Parking, Security, Maintenance"
    ]
    
    data = []
    for i in range(1, num_records+1):
        prop_type = random.choice(property_types)
        district = random.choice(list(district_wards.keys()))
        ward = random.choice(district_wards[district])
        
        # Generate realistic pricing based on property type and location
        if prop_type == 'Căn hộ':
            if district in ['Quận 1', 'Quận 3']:
                price = random.randint(8, 25) * 1000000000  # 8-25 tỷ
                area = random.randint(60, 120)
            elif district in ['Quận 7', 'Quận Bình Thạnh']:
                price = random.randint(5, 15) * 1000000000  # 5-15 tỷ
                area = random.randint(70, 130)
            else:
                price = random.randint(3, 10) * 1000000000  # 3-10 tỷ
                area = random.randint(65, 110)
            bedrooms = random.randint(1, 3)
            
        elif prop_type == 'Nhà phố':
            if district in ['Quận 1', 'Quận 3']:
                price = random.randint(30, 80) * 1000000000  # 30-80 tỷ
                area = random.randint(100, 200)
            elif district in ['Quận 7', 'Quận Bình Thạnh']:
                price = random.randint(20, 50) * 1000000000  # 20-50 tỷ
                area = random.randint(120, 250)
            else:
                price = random.randint(15, 35) * 1000000000  # 15-35 tỷ
                area = random.randint(100, 200)
            bedrooms = random.randint(3, 5)
            
        elif prop_type == 'Biệt thự':
            price = random.randint(50, 150) * 1000000000  # 50-150 tỷ
            area = random.randint(200, 400)
            bedrooms = random.randint(4, 6)
            
        elif prop_type == 'Shophouse':
            price = random.randint(25, 60) * 1000000000  # 25-60 tỷ
            area = random.randint(150, 300)
            bedrooms = random.randint(2, 4)
            
        else:  # Văn phòng
            price = random.randint(10, 30) * 1000000000  # 10-30 tỷ
            area = random.randint(80, 200)
            bedrooms = 0
        
        # Generate realistic address
        street_names = ['Nguyễn Huệ', 'Lê Lợi', 'Đồng Khởi', 'Pasteur', 'Võ Văn Tần', 
                       'Nguyễn Thị Minh Khai', 'Cách Mạng Tháng 8', '3 Tháng 2', 
                       'Lý Tự Trọng', 'Nam Kỳ Khởi Nghĩa', 'Điện Biên Phủ', 'Võ Thị Sáu']
        street = random.choice(street_names)
        number = random.randint(1, 200)
        address = f"{number} {street}, {ward}, {district}, TP.HCM"
        
        data.append({
            'id': f'SP{i:03d}',
            'type': prop_type,
            'district': district,
            'ward': ward,
            'address': address,
            'price': price,
            'area': area,
            'bedrooms': bedrooms,
            'direction': random.choice(['Đông', 'Tây', 'Nam', 'Bắc', 'Đông Nam', 'Tây Nam', 'Đông Bắc', 'Tây Bắc']),
            'legal_status': random.choice(['Sổ hồng', 'Sổ đỏ', 'Hợp đồng mua bán', 'Đang hoàn thiện pháp lý']),
            'amenities': random.choice(amenities_list),
            'description': random.choice(descriptions),
            'posted_date': fake.date_between(start_date='-6m', end_date='today').strftime('%Y-%m-%d'),
            'status': random.choice(['available', 'pending', 'sold'])
        })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Tạo thư mục data nếu chưa tồn tại
    os.makedirs('data', exist_ok=True)
    
    # Tạo dataset với 30 mẫu
    df = generate_real_estate_data(30)
    
    # Lưu ra file CSV
    df.to_csv('data/sample_real_estate.csv', index=False)
    print("✅ Đã tạo file dữ liệu mẫu: data/sample_real_estate.csv")
    print(f"📊 Số lượng bản ghi: {len(df)}")
    print(f"🏠 Các loại hình: {df['type'].value_counts().to_dict()}")
    print(f"📍 Các quận: {df['district'].value_counts().to_dict()}")
    print(f"💰 Khoảng giá: {df['price'].min():,.0f} - {df['price'].max():,.0f} VND")