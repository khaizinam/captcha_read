#!/bin/bash
# Script cài đặt nhanh cho máy đã có Python
# Chạy: bash quick_install.sh

set -e

echo "=== Cài đặt nhanh cho OCR/Captcha Reader ==="

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 chưa được cài đặt. Vui lòng chạy install.sh trước."
    exit 1
fi

# Cài đặt system dependencies
echo "📦 Cài đặt system dependencies..."
sudo apt update
sudo apt install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-vie libtesseract-dev

# Cài đặt thêm packages cần thiết cho OpenCV
echo "📦 Cài đặt thêm dependencies..."
sudo apt install -y \
    libopencv-dev \
    python3-opencv \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgcc-s1 \
    libgfortran5 \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev || echo "⚠️ Một số packages không khả dụng, bỏ qua..."

# Tạo virtual environment
echo "🌐 Tạo virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Cài đặt Python packages
echo "📚 Cài đặt Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Cài đặt hoàn tất!"
echo "Kích hoạt: source venv/bin/activate"
