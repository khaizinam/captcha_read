#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ứng dụng giải mã captcha và đọc ký tự từ hình ảnh
Sử dụng OpenCV và Tesseract OCR
"""

import cv2
import pytesseract
import numpy as np
from PIL import Image
import argparse
import os
import sys

class CaptchaReader:
    def __init__(self):
        """Khởi tạo CaptchaReader với cấu hình mặc định"""
        # Cấu hình Tesseract (có thể cần điều chỉnh đường dẫn trên WSL)
        self.tesseract_config = '--oem 3 --psm 6'
        
    def preprocess_image(self, image_path):
        """
        Tiền xử lý hình ảnh để cải thiện độ chính xác OCR
        """
        # Đọc hình ảnh
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Không thể đọc hình ảnh: {image_path}")
        
        # Chuyển đổi sang grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Làm mờ để giảm nhiễu
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # Threshold để tạo ảnh nhị phân
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Loại bỏ nhiễu nhỏ
        kernel = np.ones((2,2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def read_text_from_image(self, image_path, preprocess=True):
        """
        Đọc text từ hình ảnh
        
        Args:
            image_path (str): Đường dẫn đến hình ảnh
            preprocess (bool): Có tiền xử lý hình ảnh hay không
            
        Returns:
            str: Text được nhận dạng
        """
        try:
            if preprocess:
                # Tiền xử lý hình ảnh
                processed_image = self.preprocess_image(image_path)
            else:
                # Đọc trực tiếp
                processed_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            # Sử dụng Tesseract để OCR
            text = pytesseract.image_to_string(
                processed_image, 
                config=self.tesseract_config,
                lang='eng+vie'  # Hỗ trợ tiếng Anh và tiếng Việt
            )
            
            return text.strip()
            
        except Exception as e:
            print(f"Lỗi khi đọc hình ảnh {image_path}: {str(e)}")
            return ""
    
    def read_captcha(self, image_path):
        """
        Chuyên biệt cho việc đọc captcha
        """
        try:
            # Đọc hình ảnh
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Không thể đọc hình ảnh: {image_path}")
            
            # Resize nếu ảnh quá nhỏ
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
            
            # OCR với cấu hình tối ưu cho captcha
            captcha_config = '--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
            text = pytesseract.image_to_string(cleaned, config=captcha_config)
            
            return text.strip()
            
        except Exception as e:
            print(f"Lỗi khi đọc captcha {image_path}: {str(e)}")
            return ""
    
    def batch_process(self, input_dir, output_file=None):
        """
        Xử lý hàng loạt các hình ảnh trong thư mục
        
        Args:
            input_dir (str): Thư mục chứa hình ảnh
            output_file (str): File để lưu kết quả (tùy chọn)
        """
        results = []
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')
        
        if not os.path.exists(input_dir):
            print(f"Thư mục không tồn tại: {input_dir}")
            return
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(supported_formats):
                image_path = os.path.join(input_dir, filename)
                print(f"Đang xử lý: {filename}")
                
                # Thử đọc như captcha trước
                text = self.read_captcha(image_path)
                if not text:
                    # Nếu không được, thử OCR thông thường
                    text = self.read_text_from_image(image_path)
                
                result = {
                    'file': filename,
                    'text': text,
                    'success': bool(text)
                }
                results.append(result)
                
                print(f"Kết quả: {text}")
                print("-" * 50)
        
        # Lưu kết quả
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                for result in results:
                    f.write(f"{result['file']}: {result['text']}\n")
            print(f"Kết quả đã được lưu vào: {output_file}")
        
        return results

def main():
    parser = argparse.ArgumentParser(description='Ứng dụng giải mã captcha và OCR')
    parser.add_argument('input', help='Đường dẫn đến hình ảnh hoặc thư mục')
    parser.add_argument('-o', '--output', help='File output (cho batch processing)')
    parser.add_argument('--captcha', action='store_true', help='Chế độ đọc captcha')
    parser.add_argument('--no-preprocess', action='store_true', help='Không tiền xử lý hình ảnh')
    
    args = parser.parse_args()
    
    # Khởi tạo reader
    reader = CaptchaReader()
    
    # Kiểm tra input là file hay thư mục
    if os.path.isfile(args.input):
        # Xử lý file đơn
        print(f"Đang đọc: {args.input}")
        
        if args.captcha:
            text = reader.read_captcha(args.input)
        else:
            text = reader.read_text_from_image(args.input, not args.no_preprocess)
        
        print(f"Kết quả: {text}")
        
    elif os.path.isdir(args.input):
        # Xử lý hàng loạt
        print(f"Đang xử lý thư mục: {args.input}")
        results = reader.batch_process(args.input, args.output)
        
        # Thống kê
        total = len(results)
        success = sum(1 for r in results if r['success'])
        print(f"\nThống kê: {success}/{total} hình ảnh được xử lý thành công")
        
    else:
        print(f"Đường dẫn không hợp lệ: {args.input}")
        sys.exit(1)

if __name__ == "__main__":
    main()
