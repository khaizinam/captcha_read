# Captcha OCR API

Ứng dụng REST API để giải mã captcha và đọc ký tự từ hình ảnh sử dụng Python, OpenCV và Tesseract OCR.

## Tính năng

- 🔍 Nhận dạng text từ ảnh captcha (6-10 ký tự)
- 🌐 REST API với Flask
- 🔐 Bảo mật bằng API Key
- 📱 Hỗ trợ nhiều định dạng ảnh (PNG, JPG, JPEG, BMP, TIFF)
- ⚡ Xử lý nhanh với OpenCV và Tesseract
- 🛡️ Xử lý lỗi và validation đầy đủ

## Cài đặt

### 1. Cài đặt siêu nhanh (Khuyến nghị) ⚡

```bash
# Cách 1: Khởi động trực tiếp (tự động cài đặt nếu cần)
bash start.sh

# Cách 2: Cài đặt đầy đủ trước
bash setup.sh
```

### 2. Cài đặt từng bước

```bash
# Cài đặt
bash bin/install.sh

# Chạy API
bash bin/run.sh

# Test
bash bin/test.sh

# Demo
bash bin/demo.sh
```

### 2. Cài đặt đầy đủ (máy chưa có Python)

```bash
sudo bash install.sh
```

### 3. Cài đặt nhanh (máy đã có Python)

```bash
bash quick_install.sh
```

### 4. Cài đặt thủ công

```bash
# Cài đặt system dependencies
sudo apt update
sudo apt install -y python3 python3-pip tesseract-ocr tesseract-ocr-eng tesseract-ocr-vie

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài đặt Python packages
pip install -r requirements.txt
```

### 5. Kiểm tra cài đặt

```bash
# Chạy test kiểm tra
python test_setup.py
```

## Sử dụng

### 1. Chạy API Server

```bash
# Cách 1: Khởi động trực tiếp (tự động cài đặt nếu cần)
bash start.sh

# Cách 2: Script nhanh
bash bin/run.sh

# Cách 3: Thủ công
source venv_new/bin/activate
python app.py

# Cách 4: Thay đổi port
PORT=8080 bash start.sh
```

### 2. Dừng API Server

```bash
# Dừng API
bash stop.sh
```

### 3. Kiểm tra trạng thái

```bash
# Kiểm tra trạng thái API
bash status.sh
```

Server sẽ chạy tại: `http://localhost:5000` (mặc định)

**Thay đổi port:**
```bash
# Sử dụng port 8080
PORT=8080 bash start.sh

# Sử dụng port 3000
PORT=3000 bash start.sh
```

### 2. Sử dụng API

#### Endpoint chính: `POST /api/ocr`

**Headers:**
```
X-API-Key: captcha_api_2024_secure_key_12345
Content-Type: multipart/form-data
```

**Body:**
```
image: [file ảnh]
```

**Response thành công:**
```json
{
    "status": "success",
    "text": "ABC123"
}
```

**Response lỗi:**
```json
{
    "status": "error",
    "message": "Mô tả lỗi"
}
```

### 3. Test API

```bash
# Chạy test tự động
python test_api.py

# Test với curl
curl -X POST http://localhost:5000/api/ocr \
  -H "X-API-Key: captcha_api_2024_secure_key_12345" \
  -F "image=@your_image.png"
```

### 4. Sử dụng script CLI

```bash
# Đọc một ảnh
python captcha_reader.py image.jpg

# Đọc captcha
python captcha_reader.py captcha.png --captcha

# Xử lý hàng loạt
python captcha_reader.py /path/to/images/ -o results.txt
```

## API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/ocr` | Nhận ảnh và trả về text |
| GET | `/api/health` | Kiểm tra sức khỏe API |
| GET | `/api/info` | Thông tin API |

## Cấu hình

### API Key
API Key mặc định: `captcha_api_2024_secure_key_12345`

Để thay đổi, sửa trong file `app.py`:
```python
API_KEY = "your_custom_api_key"
```

### Tesseract
Cấu hình Tesseract có thể được điều chỉnh trong `app.py`:
```python
captcha_config = '--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
```

## Hỗ trợ định dạng

- **Ảnh**: PNG, JPG, JPEG, BMP, TIFF
- **Kích thước tối đa**: 10MB
- **Ký tự**: Chữ cái và số (A-Z, a-z, 0-9)

## Xử lý lỗi

| Status Code | Mô tả |
|-------------|-------|
| 200 | Thành công |
| 400 | Lỗi request (thiếu file, định dạng không hỗ trợ) |
| 401 | API key không hợp lệ |
| 413 | File quá lớn |
| 500 | Lỗi server |

## Docker (Tùy chọn)

Nếu muốn sử dụng Docker:

```bash
# Build image
docker build -t captcha-ocr-api .

# Chạy container
docker run -p 5000:5000 captcha-ocr-api
```

## Troubleshooting

### Lỗi Tesseract
```bash
# Kiểm tra Tesseract
tesseract --version

# Cài đặt thêm ngôn ngữ
sudo apt install tesseract-ocr-vie
```

### Lỗi OpenCV
```bash
# Cài đặt dependencies
sudo apt install libopencv-dev python3-opencv
```

### Lỗi kết nối API
- Kiểm tra server đang chạy: `http://localhost:5000/api/health`
- Kiểm tra API key trong header
- Kiểm tra định dạng file ảnh

## License

MIT License
