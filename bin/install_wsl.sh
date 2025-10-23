#!/bin/bash
# Script cài đặt tối ưu cho WSL Debian
# Chạy với quyền sudo: sudo bash install_wsl.sh

set -e

echo "=== Cài đặt Captcha OCR API cho WSL Debian ==="
echo ""

# Kiểm tra quyền sudo
if [ "$EUID" -ne 0 ]; then
    echo "Vui lòng chạy script này với quyền sudo:"
    echo "sudo bash install_wsl.sh"
    exit 1
fi

# Cập nhật package list
echo "📦 Cập nhật danh sách packages..."
apt update

# Cài đặt Python 3 và pip
echo "🐍 Cài đặt Python 3 và pip..."
apt install -y python3 python3-pip python3-venv python3-dev

# Cài đặt Tesseract (quan trọng nhất)
echo "🔍 Cài đặt Tesseract OCR..."
apt install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-vie libtesseract-dev

# Cài đặt các dependencies cơ bản cho OpenCV
echo "📷 Cài đặt dependencies cho OpenCV..."
apt install -y \
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
    libtiff-dev \
    wget \
    unzip

# Cài đặt thêm packages (bỏ qua lỗi nếu không có)
echo "🔧 Cài đặt thêm packages (bỏ qua lỗi)..."
apt install -y libavcodec-dev libavformat-dev libswscale-dev || echo "⚠️ Bỏ qua packages không khả dụng"
apt install -y libgtk-3-dev || echo "⚠️ Bỏ qua GTK packages"
apt install -y gfortran || echo "⚠️ Bỏ qua gfortran"

# Tạo virtual environment
echo "🌐 Tạo Python virtual environment..."
cd /var/www/py_aptcha_read
python3 -m venv venv

# Kích hoạt virtual environment và cài đặt Python packages
echo "📚 Cài đặt Python packages..."
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Cài đặt các packages từ requirements.txt
pip install -r requirements.txt

# Cài đặt thêm packages hữu ích
echo "📦 Cài đặt thêm packages hữu ích..."
pip install \
    matplotlib \
    scikit-image \
    imutils \
    easyocr || echo "⚠️ Bỏ qua packages không cần thiết"

echo ""
echo "✅ Cài đặt hoàn tất!"
echo ""
echo "=== Hướng dẫn sử dụng ==="
echo "1. Kích hoạt virtual environment:"
echo "   source /var/www/py_aptcha_read/venv/bin/activate"
echo ""
echo "2. Chạy API server:"
echo "   python app.py"
echo ""
echo "3. Test API:"
echo "   python test_api.py"
echo ""
echo "=== Kiểm tra cài đặt ==="

# Kiểm tra Python version
echo "🐍 Python version:"
python3 --version

# Kiểm tra pip version
echo "📦 Pip version:"
pip --version

# Kiểm tra Tesseract
echo "🔍 Tesseract version:"
tesseract --version

# Kiểm tra OpenCV
echo "📷 OpenCV version:"
python3 -c "import cv2; print('OpenCV:', cv2.__version__)" || echo "⚠️ OpenCV chưa hoạt động đúng"

# Kiểm tra pytesseract
echo "🔤 Pytesseract:"
python3 -c "import pytesseract; print('Pytesseract:', pytesseract.__version__)" || echo "⚠️ Pytesseract chưa hoạt động đúng"

echo ""
echo "🎉 Cài đặt hoàn tất! Hãy thử chạy: python app.py"
