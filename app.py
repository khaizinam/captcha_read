#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Captcha OCR API
REST API để đọc captcha từ hình ảnh
"""

import os
import logging
import gc
import psutil
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from captcha_reader import CaptchaReader

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Khởi tạo Flask app
app = Flask(__name__)
CORS(app)

# Cấu hình
API_KEY = os.getenv('API_KEY', 'captcha_api_2024_secure_key_12345')
PORT = int(os.getenv('PORT', 5050))
HOST = os.getenv('HOST', '0.0.0.0')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB

# Khởi tạo CaptchaReader
captcha_reader = CaptchaReader()

def validate_api_key():
    """Kiểm tra API key"""
    api_key = request.headers.get('X-API-Key')
    if not api_key or api_key != API_KEY:
        return False
    return True

@app.route('/api/health', methods=['GET'])
def health_check():
    """Kiểm tra sức khỏe API"""
    try:
        # Lấy thông tin memory
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024
        
        return jsonify({
            'status': 'success',
            'message': 'API is running',
            'version': '1.0.0',
            'memory_usage_mb': round(memory_mb, 2),
            'memory_limit_mb': 3072  # 3GB limit
        })
    except Exception as e:
        return jsonify({
            'status': 'success',
            'message': 'API is running',
            'version': '1.0.0'
        })

@app.route('/api/info', methods=['GET'])
def api_info():
    """Thông tin API"""
    return jsonify({
        'name': 'Captcha OCR API',
        'version': '1.0.0',
        'description': 'API để đọc captcha từ hình ảnh',
        'endpoints': {
            'POST /api/ocr': 'Đọc captcha từ hình ảnh',
            'GET /api/health': 'Kiểm tra sức khỏe API',
            'GET /api/info': 'Thông tin API'
        }
    })

@app.route('/api/ocr', methods=['POST'])
def ocr_captcha():
    """Đọc captcha từ hình ảnh"""
    try:
        # Kiểm tra API key
        if not validate_api_key():
            return jsonify({
                'status': 'error',
                'message': 'Invalid API key'
            }), 401
        
        # Kiểm tra file upload
        if 'image' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No image file provided'
            }), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400
        
        # Kiểm tra kích thước file
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'status': 'error',
                'message': f'File too large. Max size: {MAX_FILE_SIZE} bytes'
            }), 400
        
        # Đọc dữ liệu hình ảnh
        image_data = file.read()
        
        # Xử lý captcha
        result = captcha_reader.process_captcha(image_data=image_data)
        
        # Cleanup memory sau khi xử lý
        gc.collect()
        
        if result['success']:
            return jsonify({
                'status': 'success',
                'text': result['text']
            })
        else:
            return jsonify({
                'status': 'error',
                'message': result['error']
            }), 400
            
    except Exception as e:
        logger.error(f"Lỗi xử lý OCR: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Xử lý lỗi 404"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Xử lý lỗi 500"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("🚀 Khởi động Captcha OCR API...")
    print(f"🔑 API Key: {API_KEY}")
    print("📡 Endpoints:")
    print("  POST /api/ocr - Nhận ảnh và trả về text")
    print("  GET /api/health - Kiểm tra sức khỏe")
    print("  GET /api/info - Thông tin API")
    print(f"🌐 Server đang chạy tại: http://localhost:{PORT}")
    
    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )
