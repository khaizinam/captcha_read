#!/bin/bash
# Script cài đặt nhanh Captcha OCR API cho WSL
# Chạy: bash bin/install.sh

set -e

echo "🚀 Cài đặt nhanh Captcha OCR API cho WSL"
echo "========================================"

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 chưa được cài đặt. Vui lòng cài đặt Python3 trước."
    echo "   sudo apt update && sudo apt install python3 python3-pip"
    exit 1
fi

echo "✅ Python3 đã có sẵn"

# Cài đặt system dependencies (nếu có quyền)
echo "📦 Cài đặt system dependencies..."
if command -v sudo &> /dev/null; then
    echo "🔧 Cài đặt Tesseract và dependencies..."
    sudo apt update -qq
    sudo apt install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-vie libtesseract-dev libopencv-dev python3-opencv || echo "⚠️ Không thể cài đặt system dependencies, bỏ qua..."
else
    echo "⚠️ Không có quyền sudo, bỏ qua system dependencies"
fi

# Tạo virtual environment
echo "🌐 Tạo virtual environment..."
if [ -d "venv_new" ]; then
    echo "📁 Virtual environment đã tồn tại, bỏ qua..."
else
    python3 -m venv venv_new
    echo "✅ Đã tạo virtual environment"
fi

# Kích hoạt virtual environment
echo "🔧 Kích hoạt virtual environment..."
source venv_new/bin/activate

# Upgrade pip
echo "📦 Cập nhật pip..."
pip install --upgrade pip -q

# Cài đặt Python packages
echo "📚 Cài đặt Python packages..."
pip install opencv-python pytesseract Flask Flask-CORS numpy requests -q

echo ""
echo "✅ Cài đặt hoàn tất!"
echo ""
echo "🚀 Để chạy API:"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "🧪 Để test:"
echo "   python test_setup.py"
echo "   python test_api.py"
echo ""
echo "📡 API sẽ chạy tại: http://localhost:5000"
echo "🔑 API Key: captcha_api_2024_secure_key_12345"