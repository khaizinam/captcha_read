# Captcha OCR API

Ứng dụng REST API để giải mã captcha và đọc ký tự từ hình ảnh sử dụng Python, OpenCV và Tesseract OCR trong Docker.

## Tính năng

- 🔍 Nhận dạng text từ ảnh captcha (6-10 ký tự)
- 🌐 REST API với Flask
- 🔐 Bảo mật bằng API Key
- 📱 Hỗ trợ nhiều định dạng ảnh (PNG, JPG, JPEG, BMP, TIFF)
- ⚡ Xử lý nhanh với OpenCV và Tesseract
- 🛡️ Xử lý lỗi và validation đầy đủ
- 🐳 Chạy trong Docker với giới hạn tài nguyên (3GB RAM)
- 🔧 Tự động restart và health check

## Yêu cầu hệ thống

- Docker và Docker Compose
- Linux/WSL (đã test trên WSL2 Debian)

## Cài đặt và chạy

### 1. Khởi động API (Khuyến nghị) 🚀

```bash
# Khởi động API trong background
bash docker.sh start

# Kiểm tra trạng thái
bash docker.sh status

# Xem logs
bash docker.sh logs
```

### 2. Quản lý API

```bash
# Dừng API
bash docker.sh stop

# Restart API
bash docker.sh restart

# Test API
bash docker.sh test

# Dọn dẹp
bash docker.sh clean
```

### 3. Test với ảnh captcha

```bash
# Test với ảnh cụ thể
bash docker.sh test-ocr your_captcha.png
```

Server sẽ chạy tại: `http://localhost:8086`

## Sử dụng API

### Endpoint chính: `POST /api/ocr`

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
    "text": "kfwbyz"
}
```

**Response lỗi:**
```json
{
    "status": "error",
    "message": "Mô tả lỗi"
}
```

### Test API

```bash
# Test health check
curl -X GET http://localhost:8086/api/health

# Test OCR với curl
curl -X POST http://localhost:8086/api/ocr \
  -H "X-API-Key: captcha_api_2024_secure_key_12345" \
  -F "image=@your_captcha.png"

# Test với script
bash docker.sh test-ocr your_captcha.png
```

## API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/ocr` | Nhận ảnh và trả về text |
| GET | `/api/health` | Kiểm tra sức khỏe API |
| GET | `/api/info` | Thông tin API |

## Cấu hình

### Environment Variables
Tất cả cấu hình được quản lý trong `docker-compose.yml`:

```yaml
environment:
  - PORT=5050
  - API_KEY=captcha_api_2024_secure_key_12345
  - DEBUG=True
  - HOST=0.0.0.0
  - FLASK_ENV=development
  - FLASK_DEBUG=True
  - TESSERACT_CONFIG=--oem 3 --psm 6
  - MAX_FILE_SIZE=10485760
  - PYTHONHASHSEED=random
  - MALLOC_ARENA_MAX=2
```

### Giới hạn tài nguyên
- **RAM**: Tối đa 3GB, dự trữ 1GB
- **CPU**: Tối đa 2 cores, dự trữ 0.5 cores
- **File size**: Tối đa 10MB

## Hỗ trợ định dạng

- **Ảnh**: PNG, JPG, JPEG, BMP, TIFF
- **Kích thước tối đa**: 10MB
- **Ký tự**: Chữ cái và số (A-Z, a-z, 0-9)
- **Độ dài text**: 6-10 ký tự

## Xử lý lỗi

| Status Code | Mô tả |
|-------------|-------|
| 200 | Thành công |
| 400 | Lỗi request (thiếu file, định dạng không hỗ trợ) |
| 401 | API key không hợp lệ |
| 413 | File quá lớn |
| 500 | Lỗi server |

## Cải thiện OCR

### Model đã được tối ưu:
- **Preprocessing**: Resize, blur, threshold, morphological operations
- **Multiple configs**: Thử 8 cấu hình Tesseract khác nhau
- **Character correction**: Sửa các ký tự dễ nhầm lẫn (0→O, 1→I, 5→S, 6→G, 8→B, 9→g)
- **Debug images**: Lưu ảnh đã xử lý tại `/app/logs/debug/`

### Troubleshooting

```bash
# Kiểm tra logs
bash docker.sh logs

# Kiểm tra trạng thái
bash docker.sh status

# Test API
bash docker.sh test

# Xem debug images
ls logs/debug/
```

### Lỗi thường gặp:
- **Port 8086 đã được sử dụng**: `bash docker.sh stop` rồi `bash docker.sh start`
- **Out of memory**: Container tự động restart khi vượt quá 3GB RAM
- **OCR không chính xác**: Kiểm tra debug images trong `logs/debug/`

## License

MIT License
