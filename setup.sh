#!/bin/bash
# Script cài đặt và chạy Captcha OCR API
# Chạy: bash setup.sh

echo "🚀 Captcha OCR API - Setup & Run"
echo "================================="

# Cài đặt
echo "📦 Cài đặt..."
bash bin/install.sh

# Kiểm tra cài đặt
echo ""
echo "🧪 Kiểm tra cài đặt..."
bash bin/test.sh

echo ""
echo "🎉 Hoàn tất! API sẵn sàng sử dụng."
echo ""
echo "📡 Để chạy API: bash bin/run.sh"
echo "🧪 Để test: bash bin/test.sh"
echo "🔑 API Key: captcha_api_2024_secure_key_12345"
