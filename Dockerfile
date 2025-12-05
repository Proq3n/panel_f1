FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/models/f1.pt

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Önce requirements.txt'yi kopyala
COPY requirements.txt /app/requirements.txt

# pip'i güncelle
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# numpy'yi önce yükle ve versiyonunu kontrol et
# PyTorch 2.0.0 ile uyumlu numpy versiyonu
RUN pip install --no-cache-dir --force-reinstall numpy==1.24.3

# pycares için build dependencies
RUN pip install --no-cache-dir cffi

# Diğer paketleri yükle
RUN pip install --no-cache-dir -r /app/requirements.txt

# numpy'nin düzgün yüklendiğini kontrol et
RUN python -c "import numpy; print(f'numpy version: {numpy.__version__}')" && \
    python -c "import torch; print(f'torch version: {torch.__version__}')" && \
    python -c "import numpy; import torch; x = torch.from_numpy(numpy.array([1,2,3])); print('numpy-torch uyumluluk testi: OK')"

COPY handler.py model.py utils.py /app/
COPY models /app/models

CMD ["python", "handler.py"]


