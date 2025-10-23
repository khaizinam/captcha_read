#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REST API cho ứng dụng giải mã captcha và OCR
Sử dụng Flask framework
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import pytesseract
import numpy as np
from PIL import Image
import io
import os
import logging
from dotenv import load_dotenv
from captcha_reader import CaptchaReader

# Load environment variables
load_dotenv()

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Khởi tạo Flask app
app = Flask(__name__)
CORS(app)  # Cho phép CORS

# API Key từ environment variable
API_KEY = os.getenv('API_KEY', 'captcha_api_2024_secure_key_12345')

# Khởi tạo CaptchaReader
captcha_reader = CaptchaReader()

def validate_api_key(api_key):
    """Kiểm tra API key"""
    return api_key == API_KEY

def process_image_from_bytes(image_bytes):
    """
    Xử lý ảnh từ bytes data
    """
    try:
        # Chuyển đổi bytes thành numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        
        # Decode ảnh
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("Không thể decode ảnh")
        
        # Resize nếu ảnh quá nhỏ (tối thiểu 100x50)
        height, width = image.shape[:2]
        if height < 50 or width < 100:
            scale_factor = max(50/height, 100/width)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        # Chuyển sang grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Tăng độ tương phản
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Threshold
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Loại bỏ nhiễu
        kernel = np.ones((1,1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # OCR với cấu hình tối ưu cho captcha 6-10 ký tự
        captcha_config = '--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        text = pytesseract.image_to_string(cleaned, config=captcha_config)
        
        # Làm sạch text (loại bỏ ký tự không mong muốn)
        cleaned_text = ''.join(c for c in text.strip() if c.isalnum())
        
        return cleaned_text
        
    except Exception as e:
        logger.error(f"Lỗi xử lý ảnh: {str(e)}")
        raise

@app.route('/api/ocr', methods=['POST'])
def ocr_endpoint():
    """
    Endpoint chính để nhận ảnh và trả về text
    """
    try:
        # Kiểm tra API key
        api_key = request.headers.get('X-API-Key')
        if not api_key or not validate_api_key(api_key):
            return jsonify({
                'status': 'error',
                'message': 'API key không hợp lệ'
            }), 401
        
        # Kiểm tra có file ảnh không
        if 'image' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'Không tìm thấy file ảnh'
            }), 400
        
        file = request.files['image']
        
        # Kiểm tra file có tồn tại và có tên không
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'File ảnh không có tên'
            }), 400
        
        # Kiểm tra định dạng file
        allowed_extensions = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}
        if not ('.' in file.filename and 
                file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({
                'status': 'error',
                'message': 'Định dạng file không được hỗ trợ'
            }), 400
        
        # Đọc dữ liệu ảnh
        image_bytes = file.read()
        
        if len(image_bytes) == 0:
            return jsonify({
                'status': 'error',
                'message': 'File ảnh rỗng'
            }), 400
        
        # Xử lý ảnh
        logger.info(f"Đang xử lý ảnh: {file.filename}")
        text = process_image_from_bytes(image_bytes)
        
        # Kiểm tra kết quả
        if not text:
            return jsonify({
                'status': 'error',
                'message': 'Không thể nhận dạng text từ ảnh'
            }), 400
        
        # Trả về kết quả thành công
        return jsonify({
            'status': 'success',
            'text': text
        }), 200
        
    except Exception as e:
        logger.error(f"Lỗi xử lý request: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Lỗi server: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Endpoint kiểm tra sức khỏe API
    """
    return jsonify({
        'status': 'success',
        'message': 'API đang hoạt động bình thường',
        'version': '1.0.0'
    }), 200

@app.route('/api/info', methods=['GET'])
def api_info():
    """
    Thông tin về API
    """
    return jsonify({
        'name': 'Captcha OCR API',
        'version': '1.0.0',
        'description': 'API để nhận dạng text từ ảnh captcha',
        'endpoints': {
            'POST /api/ocr': 'Nhận ảnh và trả về text',
            'GET /api/health': 'Kiểm tra sức khỏe API',
            'GET /api/info': 'Thông tin API'
        },
        'supported_formats': ['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
        'max_file_size': '10MB'
    }), 200

@app.errorhandler(413)
def too_large(e):
    """
    Xử lý lỗi file quá lớn
    """
    return jsonify({
        'status': 'error',
        'message': 'File ảnh quá lớn'
    }), 413

@app.errorhandler(404)
def not_found(e):
    """
    Xử lý lỗi 404
    """
    return jsonify({
        'status': 'error',
        'message': 'Endpoint không tồn tại'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """
    Xử lý lỗi server
    """
    return jsonify({
        'status': 'error',
        'message': 'Lỗi server nội bộ'
    }), 500

if __name__ == '__main__':
    # Cấu hình Flask
    max_file_size = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB default
    app.config['MAX_CONTENT_LENGTH'] = max_file_size
    
    # Lấy port từ biến môi trường, mặc định là 5000
    port = int(os.environ.get('PORT', 8085))
    
    # Chạy server
    print("🚀 Khởi động Captcha OCR API...")
    print(f"🔑 API Key: {API_KEY}")
    print("📡 Endpoints:")
    print("  POST /api/ocr - Nhận ảnh và trả về text")
    print("  GET /api/health - Kiểm tra sức khỏe")
    print("  GET /api/info - Thông tin API")
    print(f"\n🌐 Server đang chạy tại: http://localhost:{port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
