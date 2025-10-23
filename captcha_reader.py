#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Captcha OCR Reader Module
Xử lý hình ảnh captcha và trích xuất text
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
import os
import logging
import gc

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CaptchaReader:
    def __init__(self):
        """Khởi tạo CaptchaReader"""
        self.tesseract_config = os.getenv('TESSERACT_CONFIG', '--oem 3 --psm 6')
        
    def preprocess_image(self, image):
        """
        Tiền xử lý hình ảnh để cải thiện độ chính xác OCR
        
        Args:
            image: Hình ảnh đầu vào (numpy array hoặc PIL Image)
            
        Returns:
            numpy array: Hình ảnh đã được xử lý
        """
        try:
            # Chuyển đổi sang numpy array nếu cần
            if isinstance(image, Image.Image):
                image = np.array(image)
            
            # Chuyển đổi sang grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image.copy()
            
            # Resize ảnh để tăng độ phân giải (tối thiểu 300px height)
            height, width = gray.shape
            if height < 300:
                scale = 300 / height
                new_width = int(width * scale)
                gray = cv2.resize(gray, (new_width, 300), interpolation=cv2.INTER_CUBIC)
            
            # Làm mờ nhẹ để giảm noise
            blurred = cv2.GaussianBlur(gray, (1, 1), 0)
            
            # Thử nhiều phương pháp threshold khác nhau
            methods = []
            
            # Method 1: OTSU
            _, thresh1 = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            methods.append(thresh1)
            
            # Method 2: Adaptive threshold
            thresh2 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            methods.append(thresh2)
            
            # Method 3: Manual threshold
            _, thresh3 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
            methods.append(thresh3)
            
            # Method 4: Invert colors (cho captcha có nền tối)
            thresh4 = cv2.bitwise_not(thresh1)
            methods.append(thresh4)
            
            # Chọn phương pháp tốt nhất (có thể cải thiện logic này)
            # Tạm thời dùng OTSU
            best_thresh = thresh1
            
            # Morphological operations để làm sạch
            kernel = np.ones((1, 1), np.uint8)
            cleaned = cv2.morphologyEx(best_thresh, cv2.MORPH_CLOSE, kernel)
            
            # Loại bỏ noise nhỏ
            kernel = np.ones((2, 2), np.uint8)
            cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Lỗi tiền xử lý hình ảnh: {e}")
            return image
    
    def extract_text(self, image):
        """
        Trích xuất text từ hình ảnh captcha
        
        Args:
            image: Hình ảnh đầu vào
            
        Returns:
            str: Text được trích xuất
        """
        try:
            # Tiền xử lý hình ảnh
            processed_image = self.preprocess_image(image)
            
            # Thử nhiều cấu hình Tesseract khác nhau
            configs = [
                '--oem 3 --psm 6',  # Single text line
                '--oem 3 --psm 7',  # Single text word
                '--oem 3 --psm 8',  # Single word
                '--oem 3 --psm 13', # Raw line
                '--oem 1 --psm 6',  # LSTM + Single text line
                '--oem 1 --psm 7',  # LSTM + Single text word
                '--oem 1 --psm 8',  # LSTM + Single word
                '--oem 1 --psm 13', # LSTM + Raw line
            ]
            
            best_text = ""
            best_confidence = 0
            
            for config in configs:
                try:
                    # Trích xuất text với cấu hình hiện tại
                    text = pytesseract.image_to_string(
                        processed_image, 
                        config=config
                    ).strip()
                    
                    # Làm sạch text
                    cleaned_text = self.clean_text(text)
                    
                    # Tính confidence (đơn giản: độ dài text hợp lý)
                    if cleaned_text and 4 <= len(cleaned_text) <= 12:
                        confidence = len(cleaned_text) / 10.0
                        
                        # Ưu tiên text có độ dài 6-10 ký tự
                        if 6 <= len(cleaned_text) <= 10:
                            confidence += 0.3
                        
                        if confidence > best_confidence:
                            best_confidence = confidence
                            best_text = cleaned_text
                            
                        logger.info(f"Config '{config}': '{cleaned_text}' (confidence: {confidence:.2f})")
                    
                except Exception as e:
                    logger.warning(f"Lỗi với config '{config}': {e}")
                    continue
            
            # Nếu không có kết quả tốt, thử với cấu hình mặc định
            if not best_text:
                try:
                    text = pytesseract.image_to_string(
                        processed_image, 
                        config=self.tesseract_config
                    ).strip()
                    best_text = self.clean_text(text)
                except:
                    pass
            
            # Debug: Lưu ảnh đã xử lý để kiểm tra
            try:
                import os
                debug_dir = "/app/logs/debug"
                os.makedirs(debug_dir, exist_ok=True)
                import time
                timestamp = int(time.time() * 1000)
                debug_path = f"{debug_dir}/processed_{timestamp}.png"
                cv2.imwrite(debug_path, processed_image)
                logger.info(f"Debug: Đã lưu ảnh xử lý tại {debug_path}")
            except Exception as e:
                logger.warning(f"Không thể lưu debug image: {e}")
            
            # Cleanup memory
            gc.collect()
            
            logger.info(f"Text được trích xuất: '{best_text}' (confidence: {best_confidence:.2f})")
            return best_text
            
        except Exception as e:
            logger.error(f"Lỗi trích xuất text: {e}")
            return ""
    
    def clean_text(self, text):
        """
        Làm sạch text được trích xuất
        
        Args:
            text: Text thô từ OCR
            
        Returns:
            str: Text đã được làm sạch
        """
        if not text:
            return ""
        
        # Loại bỏ ký tự không mong muốn
        cleaned = ''.join(c for c in text if c.isalnum())
        
        # Sửa các ký tự dễ nhầm lẫn
        char_replacements = {
            '0': 'O',  # Số 0 -> chữ O
            '1': 'I',  # Số 1 -> chữ I
            '5': 'S',  # Số 5 -> chữ S
            '6': 'G',  # Số 6 -> chữ G
            '8': 'B',  # Số 8 -> chữ B
            '9': 'g',  # Số 9 -> chữ g
        }
        
        # Thử thay thế các ký tự có thể nhầm lẫn
        for digit, letter in char_replacements.items():
            if digit in cleaned:
                # Tạo version với thay thế
                replaced = cleaned.replace(digit, letter)
                # Nếu version thay thế có độ dài hợp lý hơn, dùng nó
                if 6 <= len(replaced) <= 10 and len(replaced) >= len(cleaned):
                    cleaned = replaced
        
        # Giới hạn độ dài (6-10 ký tự như yêu cầu)
        if len(cleaned) > 10:
            cleaned = cleaned[:10]
        
        return cleaned
    
    def process_captcha(self, image_path=None, image_data=None):
        """
        Xử lý captcha từ file hoặc dữ liệu hình ảnh
        
        Args:
            image_path: Đường dẫn đến file hình ảnh
            image_data: Dữ liệu hình ảnh (bytes)
            
        Returns:
            dict: Kết quả xử lý
        """
        try:
            # Đọc hình ảnh
            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)
            elif image_data:
                from io import BytesIO
                image = Image.open(BytesIO(image_data))
            else:
                return {
                    'success': False,
                    'error': 'Không có dữ liệu hình ảnh'
                }
            
            # Trích xuất text
            text = self.extract_text(image)
            
            if text:
                return {
                    'success': True,
                    'text': text,
                    'confidence': 0.8  # Có thể tính confidence thực tế
                }
            else:
                return {
                    'success': False,
                    'error': 'Không thể trích xuất text'
                }
                
        except Exception as e:
            logger.error(f"Lỗi xử lý captcha: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# Hàm tiện ích để sử dụng trực tiếp
def read_captcha(image_path=None, image_data=None):
    """
    Hàm tiện ích để đọc captcha
    
    Args:
        image_path: Đường dẫn đến file hình ảnh
        image_data: Dữ liệu hình ảnh (bytes)
        
    Returns:
        str: Text được trích xuất
    """
    reader = CaptchaReader()
    result = reader.process_captcha(image_path, image_data)
    
    if result['success']:
        return result['text']
    else:
        return ""

if __name__ == "__main__":
    # Test với file hình ảnh
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        text = read_captcha(image_path=image_path)
        print(f"Text được trích xuất: {text}")
    else:
        print("Sử dụng: python captcha_reader.py <đường_dẫn_hình_ảnh>")
