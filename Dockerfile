# Dockerfile cho Captcha OCR API
FROM python:3.11-slim

# Cài đặt system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-vie \
    libtesseract-dev \
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
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /app

# Copy requirements và cài đặt Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Tạo thư mục logs
RUN mkdir -p logs

# Expose port
EXPOSE 5050

# Tạo user non-root để chạy ứng dụng
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5050/api/health || exit 1

# Giới hạn tài nguyên Python
ENV PYTHONHASHSEED=random
ENV MALLOC_ARENA_MAX=2
ENV PYTHONMALLOC=malloc

# Chạy ứng dụng với giới hạn memory
CMD ["python", "-O", "app.py"]
