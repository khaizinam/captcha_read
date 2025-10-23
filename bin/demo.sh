#!/bin/bash
# Script demo Captcha OCR API
# Chạy: bash bin/demo.sh

echo "🎯 Demo Captcha OCR API"
echo "======================="

# Kiểm tra virtual environment
if [ ! -d "venv_new" ]; then
    echo "❌ Virtual environment chưa được tạo."
    echo "Chạy: bash bin/install.sh"
    exit 1
fi

# Kích hoạt virtual environment
source venv_new/bin/activate

# Tạo ảnh captcha demo
echo "🎨 Tạo ảnh captcha demo..."
python -c "
from PIL import Image, ImageDraw, ImageFont
import random
import string

# Tạo text ngẫu nhiên
text = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
print(f'📝 Text gốc: {text}')

# Tạo ảnh
img = Image.new('RGB', (200, 80), color='white')
draw = ImageDraw.Draw(img)

# Vẽ text
try:
    font = ImageFont.load_default()
except:
    font = None

text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]

x = (200 - text_width) // 2
y = (80 - text_height) // 2

draw.text((x, y), text, fill='black', font=font)

# Thêm nhiễu
for _ in range(30):
    x1 = random.randint(0, 200)
    y1 = random.randint(0, 80)
    x2 = random.randint(0, 200)
    y2 = random.randint(0, 80)
    draw.line([(x1, y1), (x2, y2)], fill='gray', width=1)

# Lưu ảnh
img.save('demo_captcha.png')
print('✅ Đã tạo demo_captcha.png')
"

# Test API với ảnh demo
echo ""
echo "🧪 Test API với ảnh demo..."
python -c "
import requests
import json

# Cấu hình API
API_URL = 'http://localhost:5000/api/ocr'
API_KEY = 'captcha_api_2024_secure_key_12345'
HEADERS = {'X-API-Key': API_KEY}

try:
    with open('demo_captcha.png', 'rb') as f:
        files = {'image': f}
        response = requests.post(API_URL, headers=HEADERS, files=files)
    
    print(f'📡 Status Code: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        print(f'✅ Thành công!')
        print(f'📄 Response: {json.dumps(data, indent=2, ensure_ascii=False)}')
    else:
        print(f'❌ Lỗi: {response.text}')
        
except requests.exceptions.ConnectionError:
    print('❌ Không thể kết nối đến API. Hãy chạy: bash bin/run.sh')
except Exception as e:
    print(f'❌ Lỗi: {str(e)}')
"

# Dọn dẹp
echo ""
echo "🧹 Dọn dẹp..."
rm -f demo_captcha.png

echo ""
echo "🎉 Demo hoàn tất!"
echo ""
echo "💡 Để chạy API: bash bin/run.sh"
echo "🧪 Để test: bash bin/test.sh"
